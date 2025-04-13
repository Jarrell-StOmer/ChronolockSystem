from flask import Blueprint, render_template, request, flash
import mysql.connector
from mysql.connector import Error
import random
from datetime import datetime, timedelta

views = Blueprint('views', __name__)

@views.route('/passcode', methods=['GET', 'POST'])
def passcode():
    passcode = None  # Default value for passcode

    if request.method == 'POST':
        # Generate a random passcode
        GenPasscode = random.randint(1000, 9999)
        CreatedTime = datetime.now()
        Duration = timedelta(minutes=5)
        ExpiredTime = CreatedTime + Duration

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

                # Insert the generated passcode into the database
                insert_query = """INSERT INTO passcodes (GenPasscode, CreatedTime, ExpiredTime) VALUES (%s, %s, %s);"""
                cursor.execute(insert_query, (GenPasscode, CreatedTime, ExpiredTime))
                connection.commit()

                flash('Passcode generated successfully!', category='success')

        except Error as e:
            flash(f"An error occurred: {e}", category='error')

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    # Retrieve the most recent passcode from the database
    try:
        connection = mysql.connector.connect(
            host='localhost',
            port=3306,
            database='lock',
            user='dev',
            password='dev'
        )

        if connection.is_connected():
            cursor = connection.cursor()

            # Query the most recent passcode
            select_query = """SELECT GenPasscode FROM passcodes ORDER BY id DESC LIMIT 1;"""
            cursor.execute(select_query)
            result = cursor.fetchone()
            if result:
                passcode = result[0]  # Retrieve the passcode value

    except Error as e:
        flash(f"An error occurred while retrieving the passcode: {e}", category='error')

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

    return render_template('PasscodePage.html', passcode=passcode)

@views.route('/AdminManage', methods=['GET'])
def Admin_page():
    users = []  # Default empty list for users

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

            # Query to fetch user data with roles
            select_query = """
                SELECT
                    users.UserID,
                    users.Username,
                    roles.RoleName
                FROM
                    users
                INNER JOIN userroles ON users.UserID = userroles.UserID
                INNER JOIN roles ON userroles.RoleID = roles.RoleID;
            """
            cursor.execute(select_query)
            users = cursor.fetchall()  # Fetch all rows from the query result

    except Error as e:
        flash(f"An error occurred while retrieving user data: {e}", category='error')

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

    # Pass the user data to the template
    return render_template('Adminmanageusers.html', users=users)

@views.route('/Deleteuser', methods=['GET', 'POST'])
def Delete_page():
    
    return render_template('Deleteuser.html')

