from flask import Blueprint, request, session, flash, jsonify, url_for, current_app, redirect, render_template
from flask_mail import Message
import mysql.connector
from mysql.connector import Error
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
import os
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import SignatureExpired, BadSignature, URLSafeTimedSerializer
from config import Config

background_bp = Blueprint('background', __name__)


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

# Shut down the scheduler when exiting the app
import atexit
atexit.register(lambda: scheduler.shutdown())



@background_bp.route('/get_services')
def get_services():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    
    cursor.execute("SELECT service_id, service_type, service_name, price FROM services")
    results = cursor.fetchall()
    cursor.close()
    db.close()

    service_data = {}
    for row in results:
        service_id = row['service_id']
        service_type = row['service_type']
        service_name = row['service_name']
        price = row['price']

        
        # Create the formatted string "service_name - price"
        service_entry = {
            "service_name": f"{service_name} - {price}",
            "service_id": service_id
        }
        
        
        if service_type not in service_data:
            service_data[service_type] = []
        service_data[service_type].append(service_entry)

   
    return jsonify(service_data)


@background_bp.route('/cancel_booking', methods=['POST'])
def cancel_booking():
    appt_id = request.form.get('appt_id')
    
    if not appt_id:
        return jsonify({"error": "Appointment ID is required"}), 400

    db = get_db_connection()
    cursor = db.cursor()

    try:
        cursor.execute("DELETE FROM appointments WHERE appt_id = %s", (appt_id,))
        db.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Booking not found"}), 404

        return jsonify({"success": "Booking canceled successfully"}), 200
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        close_db_connection(db, cursor)


@background_bp.route('/final-confirm', methods=['POST'])
def final_confirm():

    data = request.get_json()

    selected_services = data.get('services')
    booking_number = data.get('bookingNumber')
    start_date_str = data.get('date')

    booking_details = []

    for service in selected_services:
        # Access `service id` and `timeSlot` properties from each entry
        service_id = service['service_id']
        service_name = service['service']
        time_slot = service['timeSlot']
        
        # making sure the format of time_slot is correct
        start_date = datetime.strptime(time_slot, "%m/%d/%Y %I:%M:%S %p")  


        appt_date = start_date.date()
        start_time = start_date.time()
        

        end_date = start_date + timedelta(minutes=30)
        end_time = end_date.time()


        booking_details.append(f"Service: {service_name} \nDate: {appt_date} \nTime: {start_time}\n")


        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute(
            'INSERT INTO appointments (booking_number, customer_id, service_id, appointment_date, appointment_start_time, appointment_end_time) VALUES (%s, %s, %s, %s, %s, %s)',
            (booking_number, session['CustomerID'], service_id, appt_date, start_time, end_time)
        )
        db.commit()
    db.close()
    cursor.close()

    email_body = (
        f"Dear Customer,\n\n"
        f"Your booking has been confirmed with the following details:\n\n"
        f"Booking Number: {booking_number}\n"
        f"Date: {start_date_str}\n"
        f"Services:\n" + "\n".join(booking_details) + "\n\n"
        f"Thank you for choosing our services!\n\n"
        f"Best Regards,\nYour Company Name"
    )

    # Send the email
    send_email_smtp(
        subject="Booking Confirmation",
        body=email_body,
        to_email=session['Email']  # Ensure 'CustomerEmail' is stored in session
    )


    return jsonify({"status": "success", "bookingNumber": booking_number})


#seller side
# 
# 
# 

@background_bp.route('/save-week-schedule', methods=['POST'])
def save_week_schedule():
    data = request.get_json()

    time_slot = data.get('timeSlot')
    managerID = session['ManagerID']
    days = data.get('days')

    db = get_db_connection()
    cursor = db.cursor()

    # Update query using 'days' as a dictionary with the proper values
    cursor.execute(
        '''
        UPDATE `week_schedule` 
        SET managerID = %s, monday = %s, tuesday = %s, wednesday = %s, thursday = %s, friday = %s, saturday = %s, sunday = %s 
        WHERE time_slot = %s
        ''', 
        (managerID, days['monday'], days['tuesday'], days['wednesday'], days['thursday'], days['friday'], days['saturday'], days['sunday'], time_slot)
    )
    db.commit()
    db.close()
    cursor.close()
    return jsonify({"success": "successful"})

@background_bp.route('/change-store-hours', methods=['POST'])
def change_store_hours():
    try:
        data = request.get_json()

        open_hour = data.get('open')
        close_hour = data.get('close')
        current_day = data.get('day')

        if not open_hour or not close_hour or not current_day:
            return jsonify({"error": "Missing required fields"}), 400

        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute('UPDATE `business_hours` SET open_hour = %s, close_hour = %s WHERE day = %s', (open_hour, close_hour, current_day))
        db.commit()
        db.close()
        cursor.close()
        return jsonify({"success": "Successfully changed"})
    
    except Exception as e:
    # Handle any unexpected errors
        return jsonify({"error": str(e)}), 500

@background_bp.route('/manage-services')
def manage_service():
    return


@background_bp.route('/edit-employee-info', methods=['POST'])
def edit_employee_info():
    data = request.get_json()

    try:
        employeeID = data.get('id')
        name = data.get('name')
        phone = data.get('phone')
        expertise = data.get('expertise')
        email = data.get('email')

        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute('UPDATE employee SET Employee_name = %s, Email = %s, Phone = %s, services_provided = %s WHERE EmployeeID = %s' , (name, email, phone, expertise, employeeID))
        
        db.commit()
        db.close()
        cursor.close()

        return jsonify({"success": "Succesffuly changed"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@background_bp.route('/remove-employee', methods=['POST'])
def remove_employee():
    try:
        data = request.get_json()

        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute('DELETE FROM employee where EmployeeID = %s', (data,))
        db.commit()
        db.close()
        cursor.close()

        return jsonify({"success": "Succesffuly changed"})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@background_bp.route('/add-employee', methods=['POST'])
def add_employee():
    try:
        data = request.get_json()

        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone')
        expertise = data.get('expertise')

        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute('INSERT INTO employee (Employee_name, Email, Phone, services_provided) VALUES (%s, %s, %s, %s)', (name, email, phone, expertise))
        db.commit()
        db.close()
        cursor.close()
        
        return jsonify({"success": "Successfully added an employee"})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500    



UPLOAD_FOLDER = 'static/photos'  # Ensure this folder exists

# Allowed extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_unique_filename(upload_folder, filename):
    base, ext = os.path.splitext(filename)
    counter = 1
    unique_filename = filename

    while os.path.exists(os.path.join(upload_folder, unique_filename)):
        unique_filename = f"{base}_{counter}{ext}"
        counter += 1

    return unique_filename

@background_bp.route('/add-service', methods=['POST'])
def upload_service_image():
    if 'service_image' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files.get('service_image')
    name = request.form.get('service_name')
    price = request.form.get('service_price')
    type = request.form.get('type')
    
    price = price_format(price)

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        upload_folder = current_app.config['UPLOAD_FOLDER']
        
        # Get a unique filename if it already exists
        unique_filename = get_unique_filename(upload_folder, filename)
        file_path = os.path.join(upload_folder, unique_filename)
        file.save(file_path)

        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute('INSERT INTO services (service_type, service_name, image, price) VALUES (%s, %s, %s, %s)', (type, name, file_path, price))
        db.commit()
        close_db_connection(db, cursor)

        return jsonify({'image_url': f'/static/photos/{unique_filename}'})
    
    return jsonify({'error': 'File type not allowed'}), 400

@background_bp.route('/update-service', methods=['POST'])
def update_service():
    
    image_changed = request.form.get('image_changed') == 'true'

    name = request.form.get('service_name')
    price = request.form.get('service_price')
    type = request.form.get('type')
    serviceID = request.form.get('id')

    db = get_db_connection()
    cursor = db.cursor()
    
    price = price_format(price)
    if (image_changed):
        if 'service_image' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        file = request.files.get('service_image')
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            upload_folder = current_app.config['UPLOAD_FOLDER']
            
            # Get a unique filename if it already exists
            unique_filename = get_unique_filename(upload_folder, filename)
            file_path = os.path.join(upload_folder, unique_filename)
            file.save(file_path)
            
            cursor.execute('UPDATE services SET service_type = %s, service_name = %s, image = %s, price = %s WHERE service_id = %s', (type, name, file_path, price, serviceID))
            db.commit()
            close_db_connection(db, cursor)

            return jsonify({"success": "Successfully updated"})
    else:
        cursor.execute('UPDATE services SET service_type = %s, service_name = %s, price = %s WHERE service_id = %s', (type, name, price, serviceID))
        db.commit()
        close_db_connection(db, cursor)
        return jsonify({"success": "Successfully updated"})
    
    db.commit()
    close_db_connection(db, cursor)
    return jsonify({"error": "File type not allowed"}), 400


@background_bp.route('/remove-service', methods=['POST'])
def remove_service():
    data = request.get_json()

    db = get_db_connection()
    cursor = db.cursor()
    
    cursor.execute('DELETE FROM services WHERE service_id = %s', (data,))
    
    db.commit()
    close_db_connection(db, cursor)
    return jsonify({"success": "successfully removed service"})

@background_bp.route('/search-employee', methods=['GET'])
def search_employee():
    data = request.args.get('name', '').strip()
    results = []
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    if data:
        cursor.execute('SELECT * FROM employee WHERE Employee_name LIKE %s', ('%' + data + '%',))
    else:
        cursor.execute('SELECT * FROM employee')
    results = cursor.fetchall()
    close_db_connection(db, cursor)
    
    return render_template('seller/employeeinfo.html', results=results)




def price_format(price):

    if price and '$' not in price:
        price = f'${price}'
    
    if price.endswith('+'):
        price_without_plus = price[:-1]
        
        if '.00' not in price_without_plus and '.0' not in price_without_plus:
            price = price_without_plus + '.00+'
        elif '.0' in price_without_plus:
            price = price_without_plus + '0+'
        else:
            price = price_without_plus + '+'
    
    if '.' in price and '+' not in price:
        if '.00' not in price and '.0' not in price:
            price = f'{price}00'
        if '.00' not in price and '.0' in price:
            price = f'{price}0'

    if '.' not in price:
        price = f'{price}.00'
    elif '$' not in price:
        price_parts = price.split('.')
        if len(price_parts[1]) == 1: 
            price = f'{price}0'
        elif len(price_parts[1]) > 2:
            price = f'{price_parts[0]}.{price_parts[1][:2]}'
    return price


def check_manager(name: str) -> bool:
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM managers where UserName = %s', (name,))
    result = cursor.fetchone()

    db.close()
    cursor.close()
    
    if result:
        return True
    
    return False

def check_managerid(num) -> bool:
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM managers where managerID = %s', (num,))
    result = cursor.fetchone()
    
    db.close()
    cursor.close()
    
    if result:
        return True
    
    return False

def check_user(name: str) -> bool:
    cursor = db.cursor()
    cursor.execute('SELECT * FROM users WHERE UserName = %s', (name,))
    have_name = cursor.fetchone()
    
    db.close()
    cursor.close()
    
    if have_name:
        return True
    else:
        return False

def to_24_hour_format(time_str):
 
    time_obj = datetime.strptime(time_str, "%I:%M %p")

 
    return time_obj.strftime("%H:%M:%S") 

def to_12_hour(td):
    total_seconds = int(td.total_seconds())
    
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)      

    hours_12 = hours % 12
    if hours_12 == 0:
        hours_12 = 12
    
    am_pm = "AM" if hours < 12 else "PM"

    return f"{hours_12:02}:{minutes:02}:{seconds:02} {am_pm}"

def to_12_hour_no_second(td):
    total_seconds = int(td.total_seconds())
    
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)


    hours_12 = hours % 12
    if hours_12 == 0:
        hours_12 = 12 

    am_pm = "AM" if hours < 12 else "PM"

    return f"{hours_12:02}:{minutes:02} {am_pm}"


def send_email_smtp(subject, body, to_email):
    
    mail = current_app.extensions['mail']

    msg = Message(subject, recipients=[to_email], body=body)
    try:
        mail.send(msg)
        print(f"Email sent successfully to {to_email}")
    except Exception as e:
        print(f"Failed to send email to {to_email}. Error: {str(e)}")



def appt_reminder():
    now = datetime.now()
    appt = now  + timedelta(hours=24)

    appt_date = appt.date()
    appt_time = appt.time()
    day_of_week = appt_date.strftime('%A')

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute(
    '''
    SELECT 
        apt.appt_id, 
        apt.booking_number, 
        apt.customer_id, 
        u.Name,
        u.Email,
        apt.service_id, 
        s.service_name,
        apt.appointment_date, 
        apt.appointment_start_time 
    FROM appointments AS apt
    JOIN users AS u ON apt.customer_id = u.CustomerID
    JOIN services AS s ON apt.service_id = s.service_id
    WHERE apt.appointment_date = %s 
    AND apt.appointment_start_time = %s;
    ''', 
    (appt_date, appt_time,)
    )
    results = cursor.fetchall()
    if results:
        for result in results:
            if result and result['Email']:
                result['appointment_start_time'] = to_12_hour_no_second(result['appointment_start_time'])
                send_email_smtp(
                    subject="Appointment Reminder",
                    body = (
                        f"Hello {result['Name']}, \n\n"
                        f"Just a reminder that you have an appointment at Jack&Son Nails Spa\n"
                        f"On {day_of_week}, {result['appointment_date']} at {result['appointment_start_time']}\n"
                        f"Service: {result['service_name']}"
                    ),
                    to_email=result['Email']
                )
            

scheduler = BackgroundScheduler()
scheduler.add_job(
        func=appt_reminder,
        trigger=CronTrigger(minute="0,30")
    )
scheduler.start()

def generate_token(email):
    s = URLSafeTimedSerializer(Config.SECRET_KEY)
    token = s.dumps(email, salt='password-reset-salt')
    return token

def get_email(token):
    try:
        s = URLSafeTimedSerializer(Config.SECRET_KEY)
        email = s.loads(token, salt='password-reset-salt', max_age=3600)
        return email
    except SignatureExpired:
        # If token is expired
        print('The reset link has expired.', 'danger')
        return None
    
    except BadSignature:
        # If token is invalid or tampered with
        print('The reset link is invalid or has been tampered with.', 'danger')
        return None
    
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        flash('An error occurred while processing your request.', 'danger')
        return None


@background_bp.route('/req_password_', methods=['GET', 'POST'])
def request_reset():
    if request.method == 'POST':
        email = request.form['email']
        print(email)
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        if user:
            token = generate_token(user['Email'])
            reset_link = url_for('background.reset_password', token=token, _external=True)
            send_email_smtp(
                subject="Reset Password",
                body= (f'Click the following link to reset your password: {reset_link}'),
                to_email=user['Email']
            )
            flash('A password reset email has been sent.', 'info')
            return redirect(url_for('login'))
        print('GET request received')
    return render_template('client/resetpass.html')




@background_bp.route('/resetpass/<token>', methods=['GET', 'POST'])
def reset_password(token):

    email = get_email(token)
    print('Email is:', email)
    # Implement form submission to reset password (update database)
    if request.method == 'POST':
        try:
            new_password = request.form['password']
            hashed_password = generate_password_hash(new_password)
            print(new_password)
            print(f"New Password (hashed): {hashed_password}")
            db = get_db_connection()
            cursor = db.cursor()
            cursor.execute("UPDATE users SET passcode = %s WHERE Email = %s", (hashed_password, email))
            db.commit()
            close_db_connection(db, cursor)
            print('Your password has been updated!', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            print(f"Error updating password: {str(e)}")
            flash('Failed to update the password. Please try again.', 'danger')

    return render_template('client/resetpass.html', token=token)
