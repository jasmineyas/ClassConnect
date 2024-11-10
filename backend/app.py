from flask import Flask, request, jsonify   # import the Flask class from the flask module
from flask_cors import CORS
import os
import hashlib
import pandas as pd
import psycopg2
import logging 
from dotenv import load_dotenv
import re
import warnings

load_dotenv()
DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL)

app = Flask(__name__) 
CORS(app, origins=["http://localhost:3000"])
logging.basicConfig(level=logging.DEBUG)

handler = logging.StreamHandler()  # Output to terminal
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
handler.setFormatter(formatter)
app.logger.addHandler(handler)
app.logger.setLevel(logging.DEBUG)  # Ensure app logger is at DEBUG level

class InvalidFileError(Exception):
    pass

def is_my_enrolled_courses(df):
    ''' returns true if the first cell of the dataframe is "Enrolled Sections" and the first row has "My Enrolled Courses" '''
    criteria = (bool(df.head(1).isin(["Enrolled Sections"]).any().any())) and (df.columns[0] == 'My Enrolled Courses')
    return criteria

def get_section_id(section):
    '''Extract the section id from the section string'''
    return section.split(' - ')[0]

def process_upload(file):
    '''Process the files uploaded, check if the file is indeed enrollment schedule, 
    hash the student id and save the student contact info and course info to the SQL data base'''

    # process the uploaded file &  surprsess openpyxl warning: 
    # https://stackoverflow.com/questions/66214951/deal-with-openpyxl-warning-workbook-contains-no-default-style-apply-openpyxl/66749978#66749978
    with warnings.catch_warnings(): 
        warnings.filterwarnings("ignore", category=UserWarning, module=re.escape('openpyxl.styles.stylesheet'))
        df = pd.read_excel(file, engine='openpyxl') 
    if is_my_enrolled_courses(df):
        df.columns = df.iloc[1]
        df = df.drop([0,1])
        df = df.reset_index(drop=True)
        df.drop(columns=['Restrictions Bypassed by Tokens'], inplace=True) # get rid of info we don't use 
        student_raw_id = df.iloc[2,0].split(' ')[2][1:-1]
        hashed_student_id = hashlib.md5(student_raw_id.encode()).hexdigest()
        df.rename(columns={df.columns[0]:'Hashed_student_id'}, inplace=True)
        df['Hashed_student_id'] = hashed_student_id
        course_dict = df.apply(lambda row: {
            'Course Code': row['Course Listing'].split(' - ')[0],
            'Course Name': row['Course Listing'].split(' - ')[1],
            'Section_id': get_section_id(row['Section']),
            'Instructional Format': row['Instructional Format'],
            'Meeting Patterns': row['Meeting Patterns'],
            'Delivery Mode': row['Delivery Mode'],
            'Registration Status': row['Registration Status'],
            'Start Date': row['Start Date'],
            'End Date': row['End Date']
        }, axis=1).to_list()
        return(hashed_student_id, course_dict)
    else: 
        raise InvalidFileError('ERROR - This is not a valid My Enrolled Courses file. Please upload the correct file.')


def insert_new_student(conn, 
                       hashed_student_id, 
                       student_email,
                    #    phone_number, 
                       whatsapp, 
                       first_name, 
                       last_name,
                       course_dict):
    logging.warning(hashed_student_id)
    try:
        with conn.cursor() as cursor:
            if check_student_exists(conn, hashed_student_id):
                # Student already exists in the database
                app.logger.info(f"Student {hashed_student_id} already exists in the database.")
            else:
                # Insert into Students table
                insert_student_query = """
                INSERT INTO Students (hashed_student_id, email, whatsapp, first_name, last_name)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT DO NOTHING;
                """
                cursor.execute(insert_student_query, 
                            (hashed_student_id, 
                                student_email, 
                                # phone_number,
                                whatsapp, 
                                first_name,
                                last_name))
                app.logger.info(f"Inserted new student: {hashed_student_id}")
    
            # Insert into course_sections table, but first check if the course is already in the table
            for course in course_dict:
                if check_course_exists(conn, course['Course Code'], (course['Section_id']), course['Start Date']):
                    # Course already exists in the database
                    app.logger.info(f"Course {course['Course Code']} section {course['Section_id']} already exists in the database.")
                    continue
                else: 
                    insert_course_query = """
                    INSERT INTO course_sections (course_code, section_id, course_name, instructional_format, delivery_mode, meeting_patterns, start_date, end_date)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT DO NOTHING;
                    """
                    cursor.execute(insert_course_query, (
                        course['Course Code'],
                        course['Section_id'],
                        course['Course Name'],
                        course['Instructional Format'],
                        course['Delivery Mode'],
                        course['Meeting Patterns'],
                        course['Start Date'],
                        course['End Date']))
                app.logger.info(f"Inserted new course: {course['Course Code']} section {course['Section_id']}")
                                                
            # Insert into Enrollments table
            for course in course_dict:
                course_code = course['Course Code']
                section_id = course['Section_id']
                start_date = course['Start Date']
                registration_status = course['Registration Status']
                insert_enrollment_query = """
                INSERT INTO Enrollments (hashed_student_id, course_code, section_id, start_date, registration_status)
                VALUES (%s, %s, %s, %s, %s);
                """
                cursor.execute(insert_enrollment_query, (hashed_student_id, 
                                                            course_code, 
                                                            section_id, 
                                                            start_date, 
                                                            registration_status))
                app.logger.info(f"""Inserted new enrollment for student: {hashed_student_id} 
                                in course {course_code}, 
                                section {section_id}, 
                                start_date {start_date}""")

        conn.commit()
        app.logger.info(f"New student {hashed_student_id} and enrollment successfully inserted.")
    
    except psycopg2.IntegrityError as ie:
        conn.rollback()
        app.logger.error(f"Integrity error while inserting student {hashed_student_id}: {ie}")
        return jsonify({"error": "A database integrity error occurred, possibly due to duplicate or invalid data."}), 400

    except psycopg2.DatabaseError as db_err:
        conn.rollback()
        app.logger.error(f"Database error occurred for student {hashed_student_id}: {db_err}")
    except Exception as e:
        conn.rollback()
        app.logger.error(f"An unexpected error occurred for student {hashed_student_id}: {e}", exc_info=True)

def update_student_info():
    '''Insert the student info and course info to the SQL database'''
  # https://www.postgresqltutorial.com/postgresql-python/update/
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')

    # Create a cursor object
    cur = conn.cursor()

    # Execute queries, e.g., select or insert data
    cur.execute("SELECT * FROM Students;")
    rows = cur.fetchall()

     # insert student to Student table 

    # insert courses to course table

    # insert enrollment to enrollment table


    # Don't forget to close the cursor and connection
    cur.close()
    conn.close()

    pass

def check_student_exists(conn, hashed_student_id):
    with conn.cursor() as cursor:
        cursor.execute("SELECT EXISTS (SELECT 1 FROM Students WHERE hashed_student_id = %s);", (hashed_student_id,))
        # True if the student exists, False otherwise
        result = cursor.fetchone()[0]
        return result
    
def check_course_exists(conn, course_code, section_id, start_date):
    with conn.cursor() as cursor:
        query = """
        SELECT EXISTS (
            SELECT 1 FROM course_sections 
            WHERE course_code = %s AND section_id = %s AND start_date = %s
        );
        """
        cursor.execute(query, (course_code, section_id, start_date))
        result = cursor.fetchone()[0]  # True if course exists, False otherwise
        return result
    
def fetch_student_info(conn, hashed_student_id):
    with conn.cursor() as cursor:
        cursor.execute("SELECT email, phone_number FROM Students WHERE hashed_student_id = %s;", (hashed_student_id,))
        return cursor.fetchone()  # Returns the result or None if no record is found

def fetch_enrollment_info(conn, hashed_student_id, course_code, section_id, start_date):
    with conn.cursor() as cursor:
        cursor.execute(
            """
            SELECT registration_status FROM Enrollments 
            WHERE hashed_student_id = %s AND course_code = %s AND section_id = %s AND start_date = %s;
            """, (hashed_student_id, course_code, section_id, start_date))
        return cursor.fetchone()  # Returns the result or None if no record is found
    
def update_student(conn, hashed_student_id, student_email, phone_number):
    with conn.cursor() as cursor:
        update_student_query = """
        UPDATE Students
        SET email = %s, phone_number = %s
        WHERE hashed_student_id = %s;
        """
        cursor.execute(update_student_query, (student_email, phone_number, hashed_student_id))

def update_course(conn, course_code, section_id, start_date):
    with conn.cursor() as cursor:
        update_course_query = """
        UPDATE course_sections
        SET start_date = %s
        WHERE course_code = %s AND section_id = %s;
        """
        cursor.execute(update_course_query, (start_date, course_code, section_id))

def update_enrollment(conn, hashed_student_id, course_code, section_id, start_date, registration_status):
    with conn.cursor() as cursor:
        update_enrollment_query = """
        UPDATE Enrollments
        SET registration_status = %s
        WHERE hashed_student_id = %s AND course_code = %s AND section_id = %s AND start_date = %s;
        """
        cursor.execute(update_enrollment_query, (registration_status, hashed_student_id, course_code, section_id, start_date))


def update_student_course_enrollment(conn, hashed_student_id, new_email, new_phone_number, course_code, section_id, start_date, new_registration_status):
    try:
        with conn.cursor() as cursor:
            # Fetch current student info
            cursor.execute("SELECT email, phone_number FROM Students WHERE hashed_student_id = %s;", (hashed_student_id,))
            student_info = cursor.fetchone()

            # Fetch current enrollment info
            cursor.execute("""
            SELECT registration_status FROM Enrollments 
            WHERE hashed_student_id = %s AND course_code = %s AND section_id = %s AND start_date = %s;
            """, (hashed_student_id, course_code, section_id, start_date))
            enrollment_info = cursor.fetchone()

            # 1. Update student info if it has changed
            if student_info and (student_info[0] != new_email or student_info[1] != new_phone_number):
                update_student(conn, hashed_student_id, new_email, new_phone_number)

            # 2. Update course and enrollment if registration status has changed
            if enrollment_info and enrollment_info[0] != new_registration_status:
                update_course(conn, course_code, section_id, start_date)
                update_enrollment(conn, hashed_student_id, course_code, section_id, start_date, new_registration_status)
        
        conn.commit()
        print("Update successful!")

    except Exception as e:
        conn.rollback()
        print(f"An error occurred: {e}")

@app.route('/')
def home():
    app.logger.debug('This is a debug message from the index route.')
    return "this is the backend :)"

@app.route("/error")
def error_route():
    raise ValueError("This is a test error.")

@app.route('/upload', methods=['GET','POST']) 
def test_contact_info_upload():
    if request.method == 'POST':
        #for testing 
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        email = request.form.get('email')
        whatsapp = request.form.get('whatsapp')
        file = request.files.get('file')

        #process the uploaded file
        try:
            hashed_student_id, course_dict = process_upload(file)
        except InvalidFileError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": e}), 400
            #change back to this line when done testing
            #return jsonify({"error": "Error processingthe uploaded file."}), 400
        try: 
            result = insert_new_student(conn, hashed_student_id, email, whatsapp, first_name, last_name, course_dict)  
            if result is not None:
             return result   
        except Exception as e:
            app.logger.error(f"Error inserting new student record to the database: {e}")
            return jsonify({"error": "Error inserting new student record to the database."}), 400

        return jsonify({
            "message": "Form submitted successfully!",
            "firstName": first_name,
            "lastName": last_name,
            "email": email,
            "whatsapp": whatsapp,
            "hashed_student_id": hashed_student_id,
            "course_dict": course_dict
        }), 200

        

    elif request.method == 'GET':
        return jsonify({"message": "Please use a POST request to submit the form data."
                        }), 200

def notifiy_student():
    '''Notify the student that the a new student has been added to their course'''


if __name__ == "__main__":
    app.run(debug=True)


