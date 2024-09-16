from flask import Flask, request, jsonify   # import the Flask class from the flask module

app = Flask(__name__) # create an instance of this class 

@app.route('/') # 
def home():
    return "Welcome to ClassConnect!"
    # data = request.get_json()
    # return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)


