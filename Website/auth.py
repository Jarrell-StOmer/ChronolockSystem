from flask import Blueprint , render_template, request, flash, redirect, url_for, session
from flask import Flask
import mysql.connector
from mysql.connector import Error
auth = Blueprint('auth', __name__)


@auth.route('/', methods=['GET', 'POST'])
def login():

    return render_template('Login.html')



@auth.route('/createuser', methods=['Get','POST'])
def createuser():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
       
        if len(username) < 2:
            flash('Username must be at least 2 characters long.', category='error')
        elif len(password) < 5:
            flash('Password must be at least 5 characters long.', category='error')
        else:
            try:
                # Connect to the database
                connection = mysql.connector.connect(
                    host='localhost',
                    port=3306,
                    database='lock',
                    user='dev',
                    password='dev'
                )

                if connection.is_connected():
                    cursor = connection.cursor()

                    # Insert user into the database
                    insert_query = """INSERT INTO users (username, userpassword) VALUES (%s, %s)"""
                    cursor.execute(insert_query, (username, password))
                    connection.commit()

                    flash('User created successfully!', category='success')
                    return redirect(url_for('auth.login'))  # Redirect to login page

            except Error as e:
                flash(f"An error occurred: {e}", category='error')

            finally:
                if connection.is_connected():
                    cursor.close()
                    connection.close()

    return render_template('Createuser.html')