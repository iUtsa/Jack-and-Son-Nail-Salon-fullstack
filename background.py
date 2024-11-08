from flask import Flask, Blueprint, request, redirect, url_for, session, flash, jsonify, make_response
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Mail, Message
import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta, time, date

background_bp = Blueprint('background', __name__)

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Utsh@das2001",
    database="test2"
)

def get_db_connection():
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Utsh@das2001",
            database="test2"
        )
        if db.is_connected():
            return db
    except Error as e:
        print("Error connecting to MySQL database:", e)
        return None




@background_bp.route('/get_services')
def get_services():
    # Database connection (update with your connection details)
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    
    # Query to get all services
    cursor.execute("SELECT service_id, service_type, service_name, price FROM services")
    results = cursor.fetchall()
    cursor.close()
    db.close()

    # Organize data by service_type
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
        cursor.close()
        db.close()





@background_bp.route('/final-confirm', methods=['POST'])
def final_confirm():

    data = request.get_json()

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

    for service in selected_services:
        # Access `service id` and `timeSlot` properties from each entry
        service_id = service['service_id']
        time_slot = service['timeSlot']
        
        # making sure the format of time_slot is correct
        start_date = datetime.strptime(time_slot, "%m/%d/%Y %I:%M:%S %p")  


        appt_date = start_date.date()
        start_time = start_date.time()
        

        end_date = start_date + timedelta(minutes=30)
        end_time = end_date.time()

        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute(
            'INSERT INTO appointments (booking_number, customer_id, service_id, appointment_date, appointment_start_time, appointment_end_time) VALUES (%s, %s, %s, %s, %s, %s)',
            (booking_number, session['CustomerID'], service_id, appt_date, start_time, end_time)
        )
        db.commit()
    db.close()
    cursor.close()


    return jsonify({"status": "success", "bookingNumber": booking_number})

def check_user(name: str) -> bool:
    cursor = db.cursor()
    cursor.execute('SELECT * FROM users WHERE UserName = %s', (name,))
    have_name = cursor.fetchone()
    db.close()
    if have_name:
        return True
    else:
        return False


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

