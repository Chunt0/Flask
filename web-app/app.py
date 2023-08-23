import csv
import pandas as pd
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

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
@app.route('/')
def index():
    return render_template('index.html')

# Registers a new user, then sends them back to the login screen
@app.route('/signup')
def new_user():
    return render_template('signup.html')

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
