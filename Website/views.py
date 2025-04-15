from flask import Blueprint, render_template, request, flash, redirect, url_for, session
import mysql.connector
from mysql.connector import Error
import random
from datetime import datetime, timedelta

views = Blueprint('views', __name__)

@views.route('/passcode', methods=['GET'])
def passcode():
    # Render the PasscodePage template
    return render_template('PasscodePage.html')

@views.route('/generate_passcode', methods=['POST'])
def generate_passcode_button():
    # Generate a random passcode
    passcode = random.randint(1000, 9999)
    created_time = datetime.now()
    duration = timedelta(minutes=5)
    expired_at = created_time + duration

    # Retrieve the UserID from the session
    user_id = session.get('UserID')

    if not user_id:
        flash('No user is logged in. Please log in to generate a passcode.', category='error')
        return redirect(url_for('auth.login'))

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

            # Insert the passcode into the passcodes table
            insert_passcode_query = """
                INSERT INTO passcode (UserID, GenPasscode)
                VALUES (%s, %s);
            """
            cursor.execute(insert_passcode_query, (user_id, passcode))
            connection.commit()

            insert_passcodehistory_query = """
                INSERT INTO passcodehistory (CreatedTime, ExpiredTime, Duration)
                VALUES (%s, %s, %s);
            """
            cursor.execute(insert_passcodehistory_query, (created_time, expired_at, duration))
            connection.commit()
            
            # Display the passcode and its details on the screen
            flash(f"The passcode is: {passcode}", category='success')
            flash(f"The passcode was created at: {created_time.strftime('%Y-%m-%d %H:%M:%S')}", category='info')
            flash(f"The passcode will expire at: {expired_at.strftime('%Y-%m-%d %H:%M:%S')}", category='info')

    except Error as e:
        flash(f"An error occurred while storing the passcode: {e}", category='error')

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

    return redirect(url_for('views.passcode'))

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