import mysql.connector
from mysql.connector import Error

def get_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            port=3306,
            database='lock',
            user='dev',
            password='dev'
        )
        return connection
    except Error as e:
        print(f"Error connecting to the database: {e}")
        return None