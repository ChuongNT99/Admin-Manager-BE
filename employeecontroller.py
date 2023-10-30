import  mysql.connector
from flask import *
from flask_cors import CORS

app=Flask(__name__)

# api_cors_config = {
#     "origins": ["http://localhost::5000"],
#     "methods": ["GET", "POST", "PUT", "DELETE"],
#     "allow_headers": ["Authorization", "Content-Type"]
# }

# CORS(app, resources={
#     r"/*": api_cors_config
# })

#CORS(app,origins='https://06dd-210-245-110-144.ngrok-free.app')


def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'  
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE' 
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type' 
    return response

@app.after_request
def after_request(response):
    return add_cors_headers(response)

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '001122',
    'database': 'admin_manager_db',
}
    
employee_api = Blueprint("employee_api", __name__)

@app.route('/employee', methods=['POST', 'GET'])
def data():
    if request.method=='GET':
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM employees")
            rows = cursor.fetchall()
            return jsonify({'employee': rows})
        except Exception as e:
            return jsonify({'error': 'Internal Server Error'}), 500
        finally:
            cursor.close()
            conn.close()
    if request.method=='POST':   
        try:
            _json=request.json
            _employees_name=_json['employees_name']
            _email=_json['email']
            _phone_number=_json['phone_number']
            conn = mysql.connector.connect(**db_config)
            cursor=conn.cursor()
            cursor.execute("INSERT INTO employees(employees_name,email,phone_number) VALUES(%s,%s,%s)",(_employees_name,_email,_phone_number))
            conn.commit()  
            return jsonify({"message": "Created employee successfully"})
        except Exception as e:
            return jsonify({'error': 'Internal Server Error'}), 500
        finally:
            cursor.close()
            conn.close()
@app.route('/employee/<int:employees_id>',methods=[ 'DELETE', 'PUT'])
def employee_one(employees_id):
    
    if request.method=='PUT':
        try:
            _json = request.json
            _employee_name = _json['employees_name']
            _email=_json['email']
            _phone_number=_json['phone_number']
            conn = mysql.connector.connect(**db_config)
            cursor=conn.cursor()
            query = "UPDATE employees SET employees_name=%s, email=%s, phone_number=%s WHERE employees_id=%s" 
            cursor.execute(query, (_employee_name,_email,_phone_number,employees_id))
            conn.commit()  
            return jsonify({"message": "Update employee successfully"})
        except Exception as e:
            return jsonify({'error': 'Internal Server Error'}), 500
        finally:
            cursor.close()
            conn.close()

    if request.method=='DELETE':
        try:    
            conn=mysql.connector.connect(**db_config)
            cursor=conn.cursor()
            cursor.execute("DELETE FROM employees WHERE employees_id =%s",(employees_id,))
            conn.commit()
            return jsonify({"message": "Delete employee successfully"})
        except Exception as e:
            return jsonify({'error': 'Internal Server Error'}), 500
        finally:
            cursor.close()
            conn.close()   
   
        
if __name__ == "__main__":
    app.run(debug=True)