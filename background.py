from flask import Blueprint, request, session,jsonify
import mysql.connector
from mysql.connector import Error
from datetime import datetime, timedelta, time

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

@background_bp.route('/save-week-schedule', methods=['POST'])
def save_week_schedule():
    data = request.get_json()

    time_slot = data.get('timeSlot')
    print(time_slot)
    managerID = data.get('managerID')
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
        print(open_hour, close_hour, current_day)

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