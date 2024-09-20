from flask import Flask, request, jsonify   # import the Flask class from the flask module
from flask_cors import CORS
import os
import hashlib
import pandas as pd

app = Flask(__name__) 
CORS(app) # enable CORS on the app

def is_my_enrolled_courses(df):
    ''' returns true if the first cell of the dataframe is "Enrolled Sections" and the first row has "My Enrolled Courses" '''
    criteria = (bool(df.head(1).isin(["Enrolled Sections"]).any().any())) and (df.columns[0] == 'My Enrolled Courses')
    return criteria

@app.route('/')
def home():
    return "this is the backend"


@app.route('/upload', methods=['GET','POST']) # 
def test_contact_info_upload():
    '''Test displaying the contact info sent by the student'''
    first_name = request.form.get('first_name')
    last_name = request.form.get('first_name')
    email = request.form.get('email')
    whatsapp = request.form.get('whatsapp')
    file = request.files.get('file')

    if not all([first_name, last_name, email, whatsapp, file]):
        return jsonify({"error": "Missing form fields"}), 400

    # Save or process the file here
    file.save(f'./uploads/{file.filename}')

    return jsonify({
        "message": "Form submitted successfully!",
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "whatsapp": whatsapp
    }), 200


def process_upload():
    '''Process the files uploaded, check if the file is indeed enrollment schedule, 
    hash the student id and save the student contact info and course info to the SQL data base'''

    # process the uploaded file 
    df = pd.read_excel('View_My_Courses.xlsx') # !!! need to replace the file here 
    if is_my_enrolled_courses(df):
        df.columns = df.iloc[1]
        df = df.drop([0,1])
        df = df.reset_index(drop=True)
        df.drop(columns=['Restrictions Bypassed by Tokens'], inplace=True) # get rid of info we don't use 
        student_raw_id = df.iloc[2,0].split(' ')[2][1:-1]
        hashed_student_id = hashlib.md5(student_raw_id.encode()).hexdigest()
        df.rename(columns={df.columns[0]:'Hashed_student_id'}, inplace=True)
        df['Hashed_student_id'] = hashed_student_id
    else: 
        print('ERROR - This is not a valid My Enrolled Courses file. Please upload the correct file.') # !!! this need to be in the response 
  


def notifiy_student():
    '''Notify the student that the a new student has been added to their course'''


if __name__ == "__main__":
    app.run(debug=True)


