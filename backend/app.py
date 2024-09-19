from flask import Flask, request, jsonify   # import the Flask class from the flask module
import os
import hashlib
import pandas as pd

app = Flask(__name__) # create an instance of this class 

def generate_hashed_id(student_id):
    return hashlib.md5(student_id.encode()).hexdigest()

@app.route('/upload', methods=['POST']) # 
def process_upload():



if __name__ == "__main__":
    app.run(debug=True)


