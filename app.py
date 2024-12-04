from flask import Flask, render_template, request, redirect, url_for, session, flash, make_response
from flask_mail import Mail, Message
import mysql.connector, background, os
from mysql.connector import Error
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from itsdangerous import SignatureExpired, BadSignature, URLSafeTimedSerializer
import background
from config import Config



app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/photos'
app.register_blueprint(background.background_bp)
app.config.from_object(Config)
app.secret_key = Config.SECRET_KEY


app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

mail = Mail(app)

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1349U3of1393ND$",
    database="test1"
)

def get_db_connection():
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1349U3of1393ND$",
            database="test1"
        )
        if db.is_connected():
            return db
    except Error as e:
        print("Error connecting to MySQL database:", e)
        return None

def close_db_connection(db, cursor):
    if db:
        db.close()
    if cursor:
        cursor.close()

# client home page
@app.route('/')
@app.route('/index')
def home():

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute('SELECT * FROM business_hours')
    results = cursor.fetchall()
    for result in results:
        result['open_hour'] = background.to_12_hour_no_second(result['open_hour'])
        result['close_hour'] = background.to_12_hour_no_second(result['close_hour'])
    close_db_connection(db, cursor)
    return render_template('client/index.html', results=results)

# About page
@app.route('/about')
def about():
    return render_template('client/about.html')


# Services page
@app.route('/services')
def services():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute('SELECT service_type FROM services GROUP BY service_type')
    categories = cursor.fetchall()
    cursor.execute('SELECT * FROM services')
    results = cursor.fetchall()
    close_db_connection(db, cursor)
    
    return render_template('client/services.html', results=results, categories=categories)


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
    msg = request.args.get('msg', '')
    usertype = request.args.get('usertype', '')
    return render_template('client/req_password.html', usertype=usertype, msg=msg)


@app.route('/logout', methods=['POST'])
@app.route('/logout')
def logout():

    session.clear()

    return redirect(url_for('home'))


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
            time_hour_12 = background.to_12_hour(time_hour_24)  # Convert to 12-hour format
            appt['appointment_start_time'] = time_hour_12

        appt_list = [appt for appt in appt_avail if appt['service_id'] is not None]

    # Fetch user information
    cursor.execute('SELECT * FROM users WHERE CustomerID = %s', (customer_id,))
    user = cursor.fetchone()
    avatar_url = 'https://via.placeholder.com/150?text=Female+Avatar'
    
    close_db_connection(db, cursor)
    
    
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

        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute('SELECT * FROM users WHERE UserName = %s', (UserName,))
        account = cursor.fetchone() 
        close_db_connection(db, cursor)

        # Process the account data after closing the connection
        if account and check_password_hash(account['passcode'], password):
            # Create session data
            session['loggedin'] = True
            session['CustomerID'] = account['CustomerID']
            session['UserName'] = account['UserName']
            session['Email'] = account['Email']
            return redirect(url_for('home'))
        else:
            msg = 'Incorrect username/password'

    return render_template('client/login.html', msg=msg)



# create account
@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    msg = ''
    if request.method == 'POST':
        UserName = request.form.get('username')
        passcode = request.form.get('password')
        Email = request.form.get('email')
        Phone = request.form.get('phone')
        name = request.form.get('user_name')
        # Hash the password before saving it
        hashed_password = generate_password_hash(passcode)
        if background.check_user(UserName):
            msg = 'Username is already in use!!!'
            return render_template('client/createac.html', msg=msg)
        if background.check_email(Email):
            msg = 'Email is already in use!!!'
            return render_template('client/createac.html', msg=msg)
        else:
            db = get_db_connection()
            cursor = db.cursor()
            cursor.execute(
                'INSERT INTO users (UserName, passcode, Email, Phone, Name) VALUES (%s, %s, %s, %s, %s)',
                (UserName, hashed_password, Email, Phone, name)
            )
            db.commit()
            close_db_connection(db, cursor)
            
            return redirect(url_for('login'))
    return render_template('client/createac.html', msg=msg)


# SELLER SIDE
# 
# 
# 

@app.route('/manager-reset-password')
def manager_req_password():
    msg = request.args.get('msg', '')
    usertype = request.args.get('usertype', '')
    return render_template('seller/req_password.html', usertype=usertype, msg=msg)


# log in page for employee
@app.route('/employee-login', methods = ['POST', 'GET'])
def employee_login():
    msg = ''
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        managerID = int(request.form['manager_id'])
        # current_date = datetime.now()
        # formatted_date = current_date.strftime('%A %m/%d/%Y')

        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute('SELECT * FROM managers WHERE UserName = %s', (username,))
        result = cursor.fetchone()
        
        close_db_connection(db, cursor)

        if result:
            if check_password_hash(result['password'], password) and result['managerID'] == managerID:
                session['manager_loggedin'] = True
                session['ManagerID'] = result['managerID']
                session['Name'] = result['Name']
                session['UserName'] = result['UserName']
                session['Email'] = result['email']
                return redirect(url_for('seller_homepage'))
        else:
            msg = 'Incorrect username/password/manager ID'
            return render_template('seller/sellerlogin.html', msg=msg)
    return render_template('seller/sellerlogin.html', msg=msg)

# view and add employee
@app.route('/employee-editor')
def employee_editor():
    if('manager_loggedin' not in session):
        return redirect(url_for('employee_login'))
    else:
        manager_results = []
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute('SELECT * FROM employee order by EmployeeID ASC')
        employee_results = cursor.fetchall()
        if(session['ManagerID'] == 101123):
            cursor.execute('SELECT * FROM managers')
            manager_results = cursor.fetchall()
        close_db_connection(db, cursor)
        return render_template('seller/employeeeditor.html',employee_results=employee_results, manager_results=manager_results)


@app.route('/employee-info')
def employee_info():
    if 'manager_loggedin' not in session:
        return redirect(url_for('employee_login'))
    else:
        # Connect to the database
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        
        # Pagination logic
        per_page = 5
        page = request.args.get('page', 1, type=int)
        offset = (page - 1) * per_page
        
        # Query with LIMIT and OFFSET for pagination
        cursor.execute('SELECT * FROM employee LIMIT %s OFFSET %s', (per_page, offset))
        results = cursor.fetchall()
        
        # Get the total number of employees
        cursor.execute('SELECT COUNT(*) AS total FROM employee')
        total = cursor.fetchone()['total']
        
        close_db_connection(db, cursor)
        
        return render_template('seller/employeeinfo.html', results=results, page=page, total=total, per_page=per_page)

# profile page for seller side
@app.route('/seller-homepage')
def seller_homepage():
    if('manager_loggedin' in session):
        current_date = datetime.now()
        formatted_date = current_date.strftime('%A %m/%d/%Y')
        return render_template('seller/index.html', formatted_date=formatted_date)
    else:
        return render_template('seller/sellerlogin.html')


# Add a manager
@app.route('/add-manager', methods=['POST', 'GET'])
def add_manager1():
    msg = ''
    if('manager_loggedin' not in session):
        return redirect(url_for('employee_login'))
    else:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            phone = request.form['phone']
            name = request.form['name']
            managerID = request.form['manager-id']

            valid, msg = background.check_manager(username, email, managerID, phone)
            if not valid:
                return render_template('seller/addowner.html', msg=msg)
            
            hashed_pass = generate_password_hash(password)
            db = get_db_connection()
            cursor = db.cursor(dictionary=True)
            cursor.execute('INSERT INTO managers (managerID, UserName, password, Name, phone, email) VALUES (%s, %s,%s, %s, %s, %s)', (managerID, username, hashed_pass, name, phone, email))
            msg = f'Account successfully created <br> Username {username} <br> Password: {password} <br> managerID: {managerID}'
            db.commit()
            close_db_connection(db, cursor)
            
            return render_template('seller/sellerlogin.html')
            

            

        return render_template('seller/addowner.html')


# Adjust prices and services
@app.route('/price-management')
def price_manage():
    if('manager_loggedin' not in session):
        return redirect(url_for('employee_login'))
    else:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute('SELECT service_type FROM services GROUP BY service_type')
        categories = cursor.fetchall()
        cursor.execute('SELECT * FROM services')
        results = cursor.fetchall()

        close_db_connection(db, cursor)

        return render_template('seller/priceeditor.html', categories=categories, results=results)


# To make weekly schedule
@app.route('/schedule')
def schedule():
    if('manager_loggedin' not in session):
        return redirect(url_for('employee_login'))
    else:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            '''
                SELECT 
                ws.managerID,
                ws.time_slot,
                ws.monday,
                ws.tuesday,
                ws.wednesday,
                ws.thursday,
                ws.friday,
                ws.saturday,
                ws.sunday,
                m.Name
                FROM 
                week_schedule AS ws
                JOIN 
                managers AS m ON ws.managerID = m.managerID
                ORDER BY ws.id ASC;
                '''
                )
        schedule = cursor.fetchall()
        cursor.close()
        db.close()
        
        return render_template('seller/schedule.html', schedule=schedule)


# TO view and adjust store opening/closing times
@app.route('/store-schedule')
def store_schedule():
    if('manager_loggedin' not in session):
        return redirect(url_for('employee_login'))
    else:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute('SELECT * FROM business_hours')
        results = cursor.fetchall()
        for result in results:
            result['open_hour'] = background.to_12_hour_no_second(result['open_hour'])
            result['close_hour']= background.to_12_hour_no_second(result['close_hour'])
        close_db_connection(db, cursor)
        
        
        return render_template('seller/storetime.html', results=results)



# A page to manage/view upcoming appointments
@app.route('/appt-manage')
def manage_appt():
    if('manager_loggedin' not in session):
        return redirect(url_for('employee_login'))
    else:
        current_date = datetime.now().date()
        last_7days = current_date - timedelta(days=7)
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            '''
            SELECT a.appt_id, 
            a.booking_number, 
            a.customer_id, 
            s.service_name, 
            a.appointment_date, 
            a.appointment_start_time, 
            u.Name
            FROM appointments as a JOIN users as u JOIN services as s ON a.customer_id = u.CustomerID AND a.service_id = s.service_id
            ORDER BY a.appointment_date ASC, a.appointment_start_time DESC
            ''')
        results = cursor.fetchall()
        close_db_connection(db, cursor)

        return render_template('seller/viewappt.html', results=results, current_date=current_date, last_7days=last_7days)


@app.route('/past-appt')
def view_past_appt():
    if('manager_loggedin' not in session):
        return redirect(url_for('employee_login'))
    else:
        last_7days = datetime.now().date() - timedelta(days=7)
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            '''
            SELECT a.appt_id, 
            a.booking_number, 
            a.customer_id, 
            s.service_name, 
            a.appointment_date, 
            a.appointment_start_time, 
            u.Name
            FROM appointments as a JOIN users as u JOIN services as s ON a.customer_id = u.CustomerID AND a.service_id = s.service_id
            ORDER BY a.appointment_date ASC, a.appointment_start_time DESC
            ''')
        results = cursor.fetchall()
        close_db_connection(db, cursor)

        return render_template('seller/pastappt.html', results=results, last_7days=last_7days)





def update_user_password(user, hashed_password):
    cursor = db.cursor()
    cursor.execute('SELECT * FROM users WHERE user = %s', user)
    username = cursor.fetchone()
    if username:
        cursor.execute('UPDATE users SET passcode = %s WHERE UserName = %s', (hashed_password, user))
        db.commit()
        close_db_connection(db, cursor)


# Run the app
if __name__ == "__main__":
    print("Starting server at http://127.0.0.1:8000/")
    app.run(host='0.0.0.0', port=8000, debug=True)
    