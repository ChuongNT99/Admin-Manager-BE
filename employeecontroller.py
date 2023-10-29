import  mysql.connector
from flask import *

app=Flask(__name__)

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '001122',
    'database': 'admin_manager_db',
}
    

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
            conn = mysql.connector.connect(**db_config)
            cursor=conn.cursor()
            cursor.execute("INSERT INTO employees(employees_name) VALUES(%s)",(_employees_name,))
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
            conn = mysql.connector.connect(**db_config)
            cursor=conn.cursor()
            query = "UPDATE employees SET employees_name=%s WHERE employees_id=%s" 
            cursor.execute(query, (_employee_name,employees_id))
            conn.commit()  
            return jsonify({"message": "Update successfully"})
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
            return jsonify({"message": "Delete successfully"})
        except Exception as e:
            return jsonify({'error': 'Internal Server Error'}), 500
        finally:
            cursor.close()
            conn.close()   
   
        
if __name__ == "__main__":
    app.run(debug=True)