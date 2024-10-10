from flask import Flask, request, jsonify   # import the Flask class from the flask module
from flask_cors import CORS
import os
import hashlib
import pandas as pd
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ['DATABASE_URL']

app = Flask(__name__) 
CORS(app) # enable CORS on the app

class InvalidFileError(Exception):
    pass

def is_my_enrolled_courses(df):
    ''' returns true if the first cell of the dataframe is "Enrolled Sections" and the first row has "My Enrolled Courses" '''
    criteria = (bool(df.head(1).isin(["Enrolled Sections"]).any().any())) and (df.columns[0] == 'My Enrolled Courses')
    return criteria

def process_upload(file):
    '''Process the files uploaded, check if the file is indeed enrollment schedule, 
    hash the student id and save the student contact info and course info to the SQL data base'''

    # process the uploaded file 
    df = pd.read_excel(file) 
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
            'Course Listing': row['Course Listing'],
            'Section': row['Section'],
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
  

def store_student_info():
    '''Insert the student info and course info to the SQL database'''
  # https://www.postgresqltutorial.com/postgresql-python/update/
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')

    # Create a cursor object
    cur = conn.cursor()

    # Execute queries, e.g., select or insert data
    cur.execute("SELECT * FROM Students;")
    rows = cur.fetchall()

    # Don't forget to close the cursor and connection
    cur.close()
    conn.close()

    # insert student to Student table 

    # insert courses to course table

    # insert enrollment to enrollment table

    pass


@app.route('/')
def home():
    return "this is the backend :)"


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
            return jsonify({"error": "Error processingthe uploaded file."}), 400
        
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


