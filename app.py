from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Mail, Message
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session handling
# Define the secret key for token generation

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Utsh@das2001",
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
    if 'loggedin' not in session:
        flash('Please log in to view your profile.', 'warning')
        return redirect(url_for('login'))

    # Fetch the user information from the database
    cursor = db.cursor(dictionary=True)
    cursor.execute('SELECT * FROM users WHERE CustomerID = %s', (session['CustomerID'],))
    user = cursor.fetchone()
    avatar_url = 'https://via.placeholder.com/150?text=Female+Avatar'

    return render_template('client/profile.html', user=user, avatar_url=avatar_url)


@app.route('/final-confirm', methods=['POST'])
def final_confirm():
    # Get the JSON data sent from the frontend
    data = request.get_json()

    # Extract details from the JSON data
    selected_services = data.get('services')
    booking_number = data.get('bookingNumber')
    date = data.get('date')

    # You can store this in a database, or append it to the session
    # Example of storing it in a session
    if 'reservations' not in session:
        session['reservations'] = []

    session['reservations'].append({
        'booking_number': booking_number,
        'date': date,
        'services': selected_services
    })

    # Or you can insert this data into your database directly
    # Assuming you have a `reservations` table
    cursor = db.cursor()
    for service in selected_services:
        cursor.execute('INSERT INTO reservations (service, date, time) VALUES (%s, %s, %s)',
                       (service['service'], service['timeSlot'].split()[0], service['timeSlot'].split()[1]))
    db.commit()

    # Return a JSON response to acknowledge the booking confirmation
    return jsonify({'status': 'success', 'message': 'Booking confirmed!'})


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

        cursor = db.cursor()
        cursor.execute(
            'INSERT INTO users (UserName, passcode, Email, Phone, User_type) VALUES (%s, %s, %s, %s, %s)',
            (UserName, hashed_password, Email, Phone, 'customer')  # You can adjust 'customer' as needed
        )
        db.commit()
        cursor.close()
        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('login'))  # Redirect to login page after successful registration

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
    app.run(host='0.0.0.0', port=8000, debug=True)
