import csv
import pandas as pd
from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt

app = Flask(__name__)

# Set up the SQLlite database config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'secretkey'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

class RegistrationForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "ChimpMagnet"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "password"})
    submit =SubmitField("Register")

    def validate_username(self, username):
        existing_user_name = User.query.filter_by(username=username.data).first()

        if existing_user_name:
            raise ValidationError("That username already exists.")
       
class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "ChimpMagnet"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "password"})
    submit =SubmitField("Sign In")

def get_questions():
    recorded = []
    questions = []
    with open('data.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            recorded.append(row[0])
            questions.append(row[1])
        recorded.pop(0)
        questions.pop(0)
    return recorded, questions

def update_question(index,flag):
    # Read the CSV file into a DataFrame
    df = pd.read_csv('data.csv')

    if flag == 1: 
        # Update the specific cell indicating it is being flagged for removal
        df.at[index, 'recorded'] = 2 # Replace 'column_name' with the name of the column you want to modify
    else:
        # Update the specific cell
        df.at[index, 'recorded'] = 1 # Replace 'column_name' with the name of the column you want to modify
    # Write the DataFrame back to the CSV file
    df.to_csv('data.csv', index=False)

# Sign in screen, asks for username and password or allows new users to make an account
@app.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    return render_template('index.html', form=form)

# Registers a new user, then sends them back to the login screen
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('signup.html', form=form)

# Loads user page. Allows user to access their questionnare and access other apps as they are developed
@app.route('/dashboard')
def user_page():
    return render_template('dashboard.html')

# Questionnaire that is run when user clicks this app from their user_page
@app.route('/questionnaire')
def questionnaire():
    recorded, questions = get_questions()
    return render_template('questionnaire.html', recorded=recorded, questions=questions)

# 
@app.route('/update_question', methods=['POST'])
def update():
    index = request.json['index']
    flag = request.json['flag']
    update_question(index, flag)
    return jsonify(success=True)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username in users and users[username] == password:
            # Successful login
            return redirect(url_for('dashboard'))  # Redirect to the dashboard page
        else:
            error_message = "Invalid credentials. Please try again."
            return render_template('login.html', error=error_message)

    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
