from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'  
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE' 
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type' 
    return response

@app.after_request
def after_request(response):
    return add_cors_headers(response)

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "001122",
    "database": "admin_manager_db",
}

def create_db_connection():
    return mysql.connector.connect(**db_config)

@app.route("/rooms", methods=["GET"])
def get_rooms():
    try:
        conn = create_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM room_meeting")
        rows = cursor.fetchall()
        return jsonify({"rooms": rows})
    except Exception as e:
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        cursor.close()
        conn.close()

@app.route("/rooms", methods=["POST"])
def create_room():
    try:
        data = request.get_json()
        room_name = data.get("room_name")
        status = data.get("status", 0)

        conn = create_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT room_name FROM room_meeting WHERE room_name = %s", (room_name,)
        )
        existing_room = cursor.fetchone()

        if existing_room:
            return jsonify({"error": "Room already exists"}), 400

        cursor.execute(
            "INSERT INTO room_meeting (room_name, status) VALUES (%s, %s)",
            (room_name, status),
        )
        conn.commit()
        return jsonify({"message": "Room created successfully"})
    except Exception as e:
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        cursor.close()
        conn.close()

@app.route("/rooms/<int:room_id>", methods=["PUT"])
def update_room(room_id):
    try:
        data = request.get_json()
        room_name = data.get("room_name")

        conn = create_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT room_name FROM room_meeting WHERE room_id != %s AND room_name = %s",
            (room_id, room_name),
        )
        existing_room = cursor.fetchone()

        if existing_room:
            return jsonify({"error": "Room name already exists"}), 400

        cursor.execute(
            "UPDATE room_meeting SET room_name=%s WHERE room_id=%s",
            (room_name, room_id),
        )
        conn.commit()
        return jsonify({"message": "Room updated successfully"})
    except Exception as e:
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        cursor.close()
        conn.close()

@app.route("/rooms/<int:room_id>", methods=["DELETE"])
def delete_room(room_id):
    try:
        conn = create_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM room_meeting WHERE room_id=%s", (room_id,))
        conn.commit()
        return jsonify({"message": "Room deleted successfully"})
    except Exception as e:
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        cursor.close()
        conn.close()

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not Found"}), 404

if __name__ == "__main":
    app.run(debug=True)
