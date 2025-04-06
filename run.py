import mysql.connector
from app.db import *
from mysql.connector import Error 
import traceback

connection = mysql.connector.connect(host='localhost', 
                                port='3306', 
                                database='lock', 
                                user='dev', 
                                password='dev')
if connection.is_connected():
    print("Connection OK!")


username = "joseph"
userpassword = 1234

insert_users(connection, username ,userpassword)





"""		connection = mysql.connector.connect(
			host = 'localhost',
			port = '3306',
			database = 'khronolock',
			user = 'dev',
			password ='dev'
		)
"""
