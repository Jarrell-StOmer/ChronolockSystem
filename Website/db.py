import mysql.connector
from mysql.connector import Error 
import traceback

def db_connect(host, port, db, user, passw):
	
		try:
			connection = mysql.connector.connect(host,port,db,user,passw)

			if connection.is_connected():
				print("Connection OK!")
				return connection
			
		except Error as e:
			print("MYSQL Error:", e)
			traceback.print_exc()


	
	


def insert_users(connection, username,userpassword):
	if connection.is_connected():
		cursor=connection.cursor()

		insert_query= """INSERT INTO users (username, userpassword) VALUES(%s,%s);  """

		data= (username,userpassword)

		cursor.execute(insert_query,data)
		connection.commit()
		print("Data inserted Successfully")

		cursor.close()
		connection.close()
		print("MYSQL Conection is closed")
			