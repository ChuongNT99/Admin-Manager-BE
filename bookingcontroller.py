from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '001122',
    'database': 'admin_manager_db',
}


def create_db_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None


@app.route('/rooms', methods=['POST'])
def create_room():
    data = request.get_json()
    room_name = data.get('room_name')

    conn = create_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO room_meeting (room_name, status) VALUES (%s, %s)", (room_name, False))
        conn.commit()
        return jsonify({'message': 'Room created successfully'})
    except Error as e:
        return jsonify({'error': 'Internal Server Error'}), 500
    finally:
        cursor.close()
        conn.close()


@app.route('/rooms', methods=['GET'])
def get_rooms():
    conn = create_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM room_meeting")
        rows = cursor.fetchall()
        return jsonify({'rooms': rows})
    except Error as e:
        return jsonify({'error': 'Internal Server Error'}), 500
    finally:
        cursor.close()
        conn.close()


@app.route('/bookings', methods=['POST'])
def book_room():
    data = request.get_json()
    room_id = data.get('room_id')
    time_start = data.get('time_start_booking')
    time_end = data.get('time_end_booking')
    employees = data.get('employees')

    conn = create_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO booking (room_id, time_start_booking, time_end_booking) VALUES (%s, %s, %s)",
                       (room_id, time_start, time_end))
        booking_id = cursor.lastrowid  # Lấy ID của lịch họp vừa tạo
        conn.commit()

        # Thêm các nhân viên vào lịch họp
        for employee_id in employees:
            cursor.execute("INSERT INTO booking_employees (booking_id, employees_id) VALUES (%s, %s)",
                           (booking_id, employee_id))
        conn.commit()

        # Cập nhật trạng thái phòng sang "bận"
        cursor.execute(
            "UPDATE room_meeting SET status = %s WHERE room_id = %s", (True, room_id))
        conn.commit()

        return jsonify({'message': 'Booking created successfully'})
    except Error as e:
        return jsonify({'error': 'Internal Server Error'}), 500
    finally:
        cursor.close()
        conn.close()


# Lấy danh sách lịch họp


@app.route('/bookings', methods=['GET'])
def get_bookings():
    conn = create_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM booking")
        rows = cursor.fetchall()
        return jsonify({'bookings': rows})
    except Error as e:
        return jsonify({'error': 'Internal Server Error'}), 500
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    app.run(debug=True)
