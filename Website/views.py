from flask import Blueprint, render_template, request, flash, redirect, url_for
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

@views.route('/AdminManage', methods=['GET' , 'POST'])
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
    return render_template('Adminmanageusers.html', users=users)


@views.route('/add_user', methods=['POST'])
def add_user():
    if request.method == 'POST':
        username = request.form.get('Adduser')
        password = request.form.get('Addpassword')
        role = request.form.get('Addrole')

        # Validate the role input
        if role not in ['1', '2']:
            flash('Invalid role! Please enter either 1 (Admin) or 2 (User).', category='error')
            return render_template('Adminmanageusers.html')

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

                # Insert the new user into the database
                insert_user_query = """
                    INSERT INTO users (Username, USerPassword)
                    VALUES (%s, %s);
                """
                cursor.execute(insert_user_query, (username, password))
                connection.commit()

                # Get the UserID of the newly inserted user
                user_id = cursor.lastrowid

                # Insert the role into the userroletable
                insert_role_query = """
                    INSERT INTO userroles (UserID, RoleID)
                    VALUES (%s, %s);
                """
                cursor.execute(insert_role_query, (user_id, role))
                connection.commit()

                flash('User added successfully!', category='success')

        except Error as e:
            flash(f"An error occurred while adding the user: {e}", category='error')

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
        return redirect(url_for('views.Admin_page'))
 

@views.route('/delete_user', methods=['POST'])
def delete_user():
    if request.method == 'POST':
        username = request.form.get('Delete')  # Get the username from the form
        user_id = request.form.get('Userid')  # Get the UserID from the form

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

                # Check if the user exists with the given username and UserID
                check_user_query = """
                    SELECT UserID FROM users WHERE Username = %s AND UserID = %s;
                """
                cursor.execute(check_user_query, (username, user_id))
                user = cursor.fetchone()

                if user:
                    # Delete the user's role from the userroletable
                    delete_role_query = """
                        DELETE FROM userroles WHERE UserID = %s;
                    """
                    cursor.execute(delete_role_query, (user_id,))
                    connection.commit()

                    # Delete the user from the users table
                    delete_user_query = """
                        DELETE FROM users WHERE UserID = %s AND Username = %s;
                    """
                    cursor.execute(delete_user_query, (user_id, username))
                    connection.commit()

                    flash('User deleted successfully!', category='success')
                else:
                    flash('User not found! Please check the username and UserID.', category='error')

        except Error as e:
            flash(f"An error occurred while deleting the user: {e}", category='error')

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

        return redirect(url_for('views.Admin_page'))