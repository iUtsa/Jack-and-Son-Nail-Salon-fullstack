from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session handling

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="ABC123000$$$",
    database="Customer_and_Employee_Information"
)

# Home route
@app.route('/')
def home():
    return render_template('client/index.html')

# About page
@app.route('/about')
def about():
    return render_template('client/about.html')

# Services page
@app.route('/services')
def services():
    return render_template('client/services.html')

# Nailcare service page
@app.route('/nailcare')
def nailcare():
    return render_template('client/nailcare.html')

# Contact page
@app.route('/contact')
def contact():
    return render_template('client/contact.html')

# Profile page
@app.route('/profile')
def profile():
    # Render the profile template
    return render_template('client/profile.html')


# Login page
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

    return render_template('client/login.html', msg=msg)

# Create account function
@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        # Decide employee or customer
        User_type = request.form['User_type']
        # User name
        UserName = request.form['username']
        # Create password
        passcode = request.form['passcode']
        # Gather email and phone number for automated response system
        Email = request.form['Email']
        Phone = request.form['Phone']

        # Input info into the database
        cursor = db.cursor()
        cursor.execute(
            'INSERT INTO users (UserName, passcode, Email, Phone, User_type) VALUES (%s, %s, %s, %s, %s)',
            (UserName, passcode, Email, Phone, User_type)
        )
        db.commit()
        return redirect(url_for('login'))
    return render_template('client/register.html')

# Run the app
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
