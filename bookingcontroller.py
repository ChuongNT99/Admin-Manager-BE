from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "001122",
    "database": "admin_manager_db",
}


def create_db_connection():
    return mysql.connector.connect(**db_config)


@app.route("/bookings", methods=["POST"])
def book_room():
    try:
        data = request.get_json()
        room_id = data.get("room_id")
        room_time = data.get("room_time")
        time_start_booking = data.get("time_start_booking")
        time_end_booking = data.get("time_end_booking")
        employees_id = data.get("employees_id")

        conn = create_db_connection()
        cursor = conn.cursor()

        # Kiểm tra xem phòng có sẵn trong khoảng thời gian đã chọn hay không
        cursor.execute(
            "SELECT room_id FROM booking WHERE room_id = %s AND "
            "((time_start_booking <= %s AND time_end_booking >= %s) OR "
            "(time_start_booking <= %s AND time_end_booking >= %s))",
            (room_id, time_start_booking, time_start_booking,
             time_end_booking, time_end_booking),
        )
        existing_booking = cursor.fetchone()

        if existing_booking:
            return jsonify({"error": "Room is already booked for this time"}), 400

        cursor.execute(
            "INSERT INTO booking (room_id, room_time, time_start_booking, time_end_booking, employees_id) "
            "VALUES (%s, %s, %s, %s, %s)",
            (room_id, room_time, time_start_booking,
             time_end_booking, employees_id),
        )
        conn.commit()

        # Cập nhật trạng thái của phòng
        cursor.execute(
            "UPDATE room_meeting SET status = 1 WHERE room_id = %s", (room_id,))
        conn.commit()

        return jsonify({"message": "Room booked successfully"})
    except Exception as e:
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        cursor.close()
        conn.close()
