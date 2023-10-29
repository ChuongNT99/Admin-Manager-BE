import mysql.connector

# MySQL configurations
db_config = {
    'user': 'root',
    'password': '001122',
    'database': 'admin_manager_db',
    'host': 'localhost'
}


# Tạo đối tượng kết nối MySQL
mysql = mysql.connector.connect(**db_config)