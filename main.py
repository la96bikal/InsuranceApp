from flask import Flask, render_template, request
from pymongo import MongoClient

app = Flask(__name__)

Client = MongoClient()
db = Client["Website"]
collection = db["User"]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    User = {}
    FirstName = request.form['FirstName']
    LastName = request.form['LastName']
    email = request.form['email']
    MobNum = request.form['MobNum']
    password = request.form['password']
    bday = request.form['bday']
    User["FirstName"] = FirstName
    User["LastName"] = LastName
    User["email"] = email
    User["MobNum"] = MobNum
    User["password"] = password
    User["bday"]= bday
    collection.insert(User, check_keys=False)
    return render_template('index.html')


@app.route('/signup')
def signup():
    return render_template('SignUp.html')

@app.route('/profile', methods=['POST'])
def profile():
    email = request.form['email']
    password = request.form['password']
    ee=collection.find()
    for i in ee:
        if(i["email"]==email and i["password"]==password):
            return render_template('Project.html', i=i)
    return render_template("index.html", var='Email/Username not found')

if __name__=='__main__':
    app.run(debug=True)
