from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__) 

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '001122',
    'database': 'admin_manager_db',
}

@app.route('/rooms', methods=['GET'])
def get_rooms():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM room_meeting")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify({'rooms': rows})

@app.route('/rooms', methods=['POST'])
def create_room():
    data = request.get_json()
    room_name = data.get('room_name')
    status = data.get('status')

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO room_meeting (room_name, status) VALUES (%s, %s)", (room_name, status))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Room created successfully'})

@app.route('/rooms/<int:room_id>', methods=['PUT'])
def update_room(room_id):
    data = request.get_json()
    room_name = data.get('room_name')
    status = data.get('status')

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("UPDATE room_meeting SET room_name=%s, status=%s WHERE room_id=%s", (room_name, status, room_id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Room updated successfully'})

@app.route('/rooms/<int:room_id>', methods=['DELETE'])
def delete_room(room_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM room_meeting WHERE room_id=%s", (room_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Room deleted successfully'})

if __name__ == "__main":
    app.run(debug=True)