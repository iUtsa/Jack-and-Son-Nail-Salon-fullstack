from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, make_response
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Mail, Message
import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta, time, date
import background


app = Flask(__name__)
app.register_blueprint(background.background_bp) 
app.secret_key = 'your_secret_key'  # Required for session handling
# Define the secret key for token generation

app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'  # Store session data in the filesystem
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Utsh@das2001",
    database="test1"
)

def get_db_connection():
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Utsh@das2001",
            database="test1"
        )
        if db.is_connected():
            return db
    except Error as e:
        print("Error connecting to MySQL database:", e)
        return None


# Home route
@app.route('/')
@app.route('/index')
def home():
    return render_template('client/index.html')

@app.route('/employee-login')
def seller_login():
    return render_template('seller/sellerlogin.html')

@app.route('/employee-editor')
def employee_editor():
    return render_template('seller/employeeeditor.html')

@app.route('/employee-info')
def employee_info():
    return render_template('seller/employeeinfo.html')

@app.route('/seller-homepage')
def seller_homepage():
    return render_template('seller/index.html')

@app.route('/add-manager')
def add_manager():
    return render_template('seller/addowner.html')

@app.route('/price-management')
def price_manage():
    return render_template('seller/priceeditor.html')

@app.route('/schedule')
def schedule():
    return render_template('seller/schedule.html')

@app.route('/store-schedule')
def store_schedule():
    return render_template('seller/storetime.html')

@app.route('/appt-manage')
def manage_appt():
    return render_template('seller/viewappt.html')


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


@app.route('/resetpass')
def resetpass():
    return render_template('client/resetpass.html')


@app.route('/req_password')
def req_password():
    return render_template('client/req_password.html')


@app.route('/logout', methods=['POST'])
@app.route('/logout')
def logout():

    session.clear()

    return redirect(url_for('home'))

@app.route('/seller/index.html')

@app.route('/reservation')
def reservation():
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    return render_template('client/reservation.html')


# Profile page
@app.route('/profile', methods=['POST', 'GET'])
@app.route('/profile')
def profile():
    msg = ''
    # Check if user is logged in
    if 'loggedin' not in session:
        msg = 'Please log in to view your profile.'
        return render_template('client/login.html', msg=msg)

    # Initialize variables
    appt_list = []
    current_date = datetime.now().date()
    customer_id = session['CustomerID']
    
    # Fetch appointments for the logged-in user
    db = get_db_connection()  # Ensure you get a fresh connection here
    cursor = db.cursor(dictionary=True)
    
    cursor.execute(
    '''
    SELECT 
        a.appt_id,
        a.customer_id, 
        a.service_id, 
        s.service_type,
        s.service_name, 
        a.appointment_date, 
        a.appointment_start_time, 
        a.booking_number 
    FROM 
        appointments a
    JOIN 
        services s ON a.service_id = s.service_id
    WHERE 
        a.customer_id = %s
    ORDER BY 
        a.appointment_date ASC, 
        a.appointment_start_time DESC
    ''',
    (customer_id,)
    )
    appt_avail = cursor.fetchall()

    # Process appointments to convert time format and filter out None service types
    if appt_avail:
        for appt in appt_avail:
            time_hour_24 = appt['appointment_start_time']
            time_hour_12 = background.timedelta_to_time(time_hour_24)  # Convert to 12-hour format
            appt['appointment_start_time'] = time_hour_12

        appt_list = [appt for appt in appt_avail if appt['service_id'] is not None]

    # Fetch user information
    cursor.execute('SELECT * FROM users WHERE CustomerID = %s', (customer_id,))
    user = cursor.fetchone()
    avatar_url = 'https://via.placeholder.com/150?text=Female+Avatar'
    
    cursor.close()
    db.close()
    
    # Render the profile page with a no-cache header
    response = make_response(render_template(
        'client/profile.html', user=user, avatar_url=avatar_url, appt_list=appt_list, current_date=current_date
    ))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    
    return response



@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = '' 
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        UserName = request.form['username']
        password = request.form['password']

        # Check if account exists using MySQL connector
        cursor = db.cursor(dictionary=True)
        cursor.execute('SELECT * FROM users WHERE UserName = %s', (UserName,))
        account = cursor.fetchone()

        # If account exists and password matches (no hashing used)
        if account and check_password_hash(account['passcode'], password):
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['CustomerID'] = account['CustomerID']
            session['UserName'] = account['UserName']
            session['Email'] = account['Email']
            session['User_type'] = account['User_type']

            # Redirect to the home page after successful login
            return redirect(url_for('home'))
        else:
            # Account doesn't exist or username/password incorrect
            msg = 'Incorrect username/password'

    # If login fails, render the login page again with the error message
    return render_template('client/login.html', msg=msg)



# create account
@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        UserName = request.form['username']
        passcode = request.form['password']
        Email = request.form['email']
        Phone = request.form['phone']

        # Hash the password before saving it
        hashed_password = generate_password_hash(passcode)
        if background.check_user(UserName):
            msg = 'Username is already in use!!!'
            return render_template('client/createac.html', msg=msg)
        else:
            if not db.is_connected():
                db.reconnect(attempts=3, delay=5)
            cursor = db.cursor()
            cursor.execute(
                'INSERT INTO users (UserName, passcode, Email, Phone, User_type) VALUES (%s, %s, %s, %s, %s)',
                (UserName, hashed_password, Email, Phone, 'customer')
            )
            db.commit()
            cursor.close()
            flash('Account created successfully! Please log in.', 'success')
            return redirect(url_for('login'))
    return render_template('client/createac.html')



# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.example.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your-email@example.com'
app.config['MAIL_PASSWORD'] = 'your-email-password'
mail = Mail(app)

# Serializer for generating tokens
s = URLSafeTimedSerializer(app.config['SECRET_KEY'])


@app.route('/req_password', methods=['GET', 'POST'])
def request_reset():
    if request.method == 'POST':
        email = request.form['email']

        # user = get_user_by_email(email)
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()  # Implement function to get user by email from the database
        if user:
            token = s.dumps(user[3], salt='password-reset-salt')
            reset_link = url_for('reset_password', token=token, _external=True)
            send_reset_email(user[3], reset_link)
            flash('A password reset email has been sent.', 'info')
            return redirect(url_for('login'))
        print('GET request received')
    return render_template('client/resetpass.html')


def send_reset_email(to_email, reset_link):
    msg = Message('Password Reset Request', sender='noreply@example.com', recipients=[to_email])
    msg.body = f'Click the following link to reset your password: {reset_link}'
    mail.send(msg)


def update_user_password(user, hashed_password):
    cursor = db.cursor()
    cursor.execute('SELECT * FROM users WHERE user = %s', user)
    username = cursor.fetchone()
    if username:
        cursor.execute('UPDATE users SET passcode = %s WHERE UserName = %s', (hashed_password, user))
        db.commit()
        db.close()


@app.route('/resetpass/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        email = s.loads(token, salt='password-reset-salt', max_age=3600)  # Token valid for 1 hour
    except:
        flash('The reset link is invalid or has expired.', 'danger')
        return redirect(url_for('request_reset'))

    if request.method == 'POST':
        password = request.form['password']

        cursor = db.cursor()
        cursor.execute('SELECT * FROM users WHERE email = %s', email)
        user = cursor.fetchone()
        # user = get_user_by_email(email)  # Implement function to get user by email from the database
        if user:
            # Hash and update the user's password in the database
            hashed_password = generate_password_hash(password)
            update_user_password(user, hashed_password)  # Implement this function to save new password
            flash('Your password has been updated!', 'success')
            return redirect(url_for('login'))
    return render_template('client/reset_password.html', token=token)



# Run the app
if __name__ == "__main__":
    print("Starting server at http://127.0.0.1:8000/")
    app.run(host='0.0.0.0', port=8000, debug=True)
    # db = get_db_connection()
    # cursor = db.cursor(dictionary=True)
    # cursor.execute('SELECT appt_id FROM appointments')
    # results = cursor.fetchall();
    # print(results)
    
