from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user-signup:wamp1234@localhost:3306/user-signup'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)
app.secret_key = 'wamp1234'

class User(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

form = """
<!DOCTYPE html>
<html>
    <head>
        <style>
form {{
    background-color: #eee;
    padding: 20px;
    margin: 0 auto;
    width: 540px;
    font: 16px sans-serif;
    border-radius: 10px;
    }}

 ::placeholder {{
    font-style: italic;
    text-align: left;
    opacity: 0.5;
    }}   

input[type="text"],
input[type="email"],
input[type="password"] {{ 
    background: #e8eeefd3;    
    background-color: #e8eeefd3;
    font-size: 16px;
    height: auto;
    padding: 15px;
    color: black;    
    margin-bottom: 17px;
    margin-top: 10px;
    border-radius: 5px;
    box-shadow:none;
    border-color:transparent;
    }}



button[type="submit"] {{
    font-size: 1.5em;
    padding: 20px 20px;
    cursor: pointer;
    background-color: #52bab3;
    color: white;
    width: 95%;
    border-radius: 5px;
    border: none;
    margin-top: 10px; 
    margin-bottom: 20px; 
    outline: none;
    }}

        </style>
    </head>
    <body>
        <form action="/register" method="POST">
        <h1>Signup</h1>
        <div>
        <label for="username">Username</label>
        <input type="text"  name="username" placeholder="ie MrDatabase327" pattern="[a-zA-Z][a-zA-Z0-9-_-.]{{3,20}}" title="No spaces!!!"  required>
        </div> 

        <div>
        <label for="password">Password</label>
    <input type="password" name="password" id="password" placeholder="You can use letters and #'s" pattern="[^' ']{{3,20}}" title="Min of 3 letters. No spaces!!!" required>
        </div>

        <div>
        <label for="verify">Verify Password</label>
        <input type="password" name="verify" id="confirm_password" placeholder="Type it again!!!" pattern="[^' ']{{3,20}}" title="Min of 3 letters. No spaces!!!"  required>
        </div>

        <div>
        <label for="email">Email</label>
        <input type="email" id="email" name="email" placeholder="(optional)"  title="Min of 3 letters. No spaces!!!" >
        </div>
               
        <button type="submit">Submit</button>
    </body>
</html>
"""

@app.route("/")
def index():
    return form.format('')

@app.route('/register', methods=['POST', 'GET'])
def register():

    if request.method == 'POST':
        username = request.form['username']        
        password = request.form['password']
        verify = request.form['verify']
        email = request.form['email']
        existing_user = User.query.filter_by(username=username).first()

        if not existing_user:
            new_user= User(username, password, email)
            db.session.add(new_user)
            db.session.commit()

        if password == verify:
            session['username'] = username
            return "<h1>Welcome, {0}!</h1>".format(username)
        elif password != verify:            
            return '<h1>Passwords did not match. Please try again.</h1>'
        else:    
            return "<h1>Welcome, {0}!</h1>".format(username)
        if not existing_user == False:
            return "<h1>An account already exists with username [{0}]</h1>".format(username)
        


    return "<h1>Nope!</h1>"

if __name__ == '__main__':
    app.run()