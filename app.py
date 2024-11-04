from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Mail, Message
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta, time, date

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session handling
# Define the secret key for token generation

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Utsh@das2001",
    database="test1"
)


## Add function to create account to check for existed username!!!!!









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


@app.route('/resetpass')
def resetpass():
    return render_template('client/resetpass.html')


@app.route('/req_password')
def req_password():
    return render_template('client/req_password.html')


@app.route('/logout', methods=['POST'])
@app.route('/logout')
def logout():
    # Clear the session data to log the user out
    session.clear()

    # Redirect to the login page after logging out
    # Redirect to the home page after logging out
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('home'))


@app.route('/reservation')
def reservation():
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    return render_template('client/reservation.html')


# Profile page
@app.route('/profile', methods=['POST'])
@app.route('/profile')
def profile():
    # Render the profile template
    # Check if user is logged in
    appt_list = []
    current_date = datetime.now().date()
    if 'loggedin' not in session:
        flash('Please log in to view your profile.', 'warning')
        return redirect(url_for('login'))
    customer_id = session['CustomerID']
    cursor = db.cursor(dictionary=True)
    cursor.execute('SELECT service_type, appointment_date, appointment_start_time, booking_number FROM appointments WHERE customer_id = %s ORDER BY appointment_date ASC, appointment_start_time DESC', (customer_id,))
    appt_avail = cursor.fetchall()

    if appt_avail:
        for appt in appt_avail:
            # Get the 24-hour format appointment time
            time_hour_24 = appt['appointment_start_time']
            
            # Update the appointment dictionary with the new time format
            time_hour_12 = timedelta_to_time(time_hour_24)  # Format as 12-hour time

            appt['appointment_start_time'] = time_hour_12 # reassigning 12-hours cycle into each appointment_time
            
            
            #Filter out any appointments with a None service_type
        appt_avail = [appt for appt in appt_avail if appt['service_type'] is not None]
        appt_list = appt_avail
    # Fetch the user information from the database
    cursor.execute('SELECT * FROM users WHERE CustomerID = %s', (customer_id,))
    user = cursor.fetchone()
    avatar_url = 'https://via.placeholder.com/150?text=Female+Avatar'
    cursor.close()
    return render_template('client/profile.html', user=user, avatar_url=avatar_url,appt_list=appt_list, current_date=current_date)


@app.route('/final-confirm', methods=['POST'])
def final_confirm():
    # Get the JSON data sent from the frontend
    data = request.get_json()

    # Extract details from the JSON data
    selected_services = data.get('services')
    booking_number = data.get('bookingNumber')
    start_date_str = data.get('date')

    # Store in the session
    if 'reservations' not in session:
        session['reservations'] = []

    session['reservations'].append({
        'booking_number': booking_number,
        'start_date': start_date_str,
        'services': selected_services
    })

    # Insert data into the database
    cursor = db.cursor()
    for service in selected_services:
        # Access `service` and `timeSlot` properties from each entry
        service_type = service['service']
        time_slot = service['timeSlot']
        
        # Ensure the format of time_slot is correct
        start_date = datetime.strptime(time_slot, "%m/%d/%Y %I:%M:%S %p")  # Adjust format as necessary

        # Extract the time component
        appt_date = start_date.date()
        start_time = start_date.time()
        
        # Add 30 minutes to start_date for end time
        end_date = start_date + timedelta(minutes=30)
        end_time = end_date.time()

        # Insert each service individually into the database
        cursor.execute(
            'INSERT INTO appointments (booking_number, customer_id, employee_id, service_type, appointment_date, appointment_start_time, appointment_end_time) VALUES (%s, %s, %s, %s, %s, %s, %s)',
            (booking_number, session['CustomerID'], 5, service_type, appt_date, start_time, end_time)
        )

    db.commit()

    # Return a JSON response to confirm the booking
    return jsonify({"status": "success", "bookingNumber": booking_number})


# login
# Login page route
# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''  # Output message if something goes wrong
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


# create ac
@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        UserName = request.form['username']
        passcode = request.form['password']
        Email = request.form['email']
        Phone = request.form['phone']

        # Hash the password before saving it
        hashed_password = generate_password_hash(passcode)
        if check_user(UserName):
            flash('Username is already in use', 'danger')
        else:
            if not db.is_connected():
                db.reconnect(attempts=3, delay=5)
            cursor = db.cursor()
            cursor.execute(
                'INSERT INTO test1.users (UserName, passcode, Email, Phone, User_type) VALUES (%s, %s, %s, %s, %s)',
                (UserName, hashed_password, Email, Phone, 'customer')
            )
            db.commit()
            cursor.close()
            flash('Account created successfully! Please log in.', 'success')
            return redirect(url_for('login'))
    return render_template('client/createac.html')


def check_user(name: str) -> bool:
    cursor = db.cursor()
    cursor.execute('SELECT * FROM users WHERE UserName = %s', (name,))
    have_name = cursor.fetchone()
    db.close()
    if have_name:
        return True
    else:
        return False

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

def timedelta_to_time(td):
    # Extract total seconds from timedelta
    total_seconds = int(td.total_seconds())
    
    # Calculate hours, minutes, and seconds
    hours, remainder = divmod(total_seconds, 3600)  # 3600 seconds in an hour
    minutes, seconds = divmod(remainder, 60)        # 60 seconds in a minute

    # Create a time object
    t = time(hour=hours % 24, minute=minutes, second=seconds)
    
    # Format the time in 12-hour format
    hour_12 = t.hour % 12 or 12  # Convert to 12-hour format
    am_pm = "AM" if t.hour < 12 else "PM"
    
    return f"{hour_12:02}:{t.minute:02}:{t.second:02} {am_pm}"



# Run the app
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
