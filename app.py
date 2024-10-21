from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="ABC123000$$$",
    database="Customer_and_Employee_Information"
)
<<<<<<< HEAD


@app.route('/')
def home():
    return render_template('client/index.html')

@app.route('/about')
def about():
    return render_template('client/about.html')

@app.route('/services')
def services():
    return render_template('client/services.html')
=======
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
        keyboard.execute = ('INSERT INTO users (UserName, passcode, Email, Phone, User_type) VALUE (%s, %s, %s, %s, %s)', (UserName, passcode, Email, Phone, User_type))
        db.commit()
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''  # Output message if something goes wrong
    if request.method == 'POST' and 'UserName' in request.form and 'passcode' in request.form:
        # Create variables for easy access
        UserName = request.form['UserName']
        passcode = request.form['passcode']

        # Check if account exists using MySQL connector
        cursor = db.cursor(dictionary=True)
        cursor.execute('SELECT * FROM users WHERE UserName = %s AND passcode = %s', (UserName, passcode,))
        account = cursor.fetchone()

        # If account exists in users table in our database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['CustomerID'] = account['CustomerID']
            session['UserName'] = account['UserName']
            session['Email'] = account['Email']
            session['User_type'] = account['User_type']

            # Redirect to profile page
            return render_template('profile.html', msg=msg)
        else:
            # Account doesn't exist or username/password incorrect
            msg = 'Incorrect username/password!'

    return render_template('index.html', msg=msg)

#Schedule Appointment
>>>>>>> 84ab877fe81ae7af0f250486c83ee75b4bc3a5b7

@app.route('/login')
def login():
    return render_template('client/login.html')

@app.route('/nailcare')
def nailcare():
    return render_template('client/nailcare.html')

@app.route('/contact')
def contact():
    return render_template('client/contact.html')

if __name__ == "__main__":
<<<<<<< HEAD
    app.run(host='0.0.0.0', port=8000, debug=True)
=======
    app.run(debug=True)
>>>>>>> 84ab877fe81ae7af0f250486c83ee75b4bc3a5b7
