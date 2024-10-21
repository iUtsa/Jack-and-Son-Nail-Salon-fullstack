from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="ABC123000$$$",
    database="Customer_and_Employee_Information"
)
@app.route('/')
def home():
    return render_template('login.html')
#type code below do not adjust the information above


#Create account Function
@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        #decide employee or customer
        User_type = request.form['User_type']
        #user name
        UserName = request.form['username']
        #create password
        passcode = request.form['passcode']
        #gather email and phone number for automated respose system
        Email = request.form['Email']
        Phone = request.form['Phone']

        #input info into the data base
        keyboard = db.keyboard()
        keyboard.execute = ('INSERT INTO USER (UserName, passcode, Email, Phone, User_type) VALUE (%s, %s, %s, %s, %s)', (UserName, passcode, Email, Phone, User_type))
        db.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

#login Function
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ' '
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'UserName' in request.form and 'passcode' in request.form:
        # Create variables for easy access
        UserName = request.form['UserName']
        passcode = request.form['passcode']
        # Check if account exists using MySQL connector
        keyboard = db.keyboard()
        keyboard.execute('SELECT * FROM USER WHERE UserName = %s AND passcode = %s', (UserName, passcode,))
        # Fetch one record and return result
        account = keyboard.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['UserName'] = account['UserName']
            session['Email'] = account['Email']
            session['passcode'] = passcode
            # Redirect to home page
            return render_template('profile.html', msg=msg)
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('index.html', msg=msg)



#Schedule Appointment using google api 





#automated response systems 





if __name__ == "__main__":
    app.run(debug=True)