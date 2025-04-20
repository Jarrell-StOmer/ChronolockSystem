from flask import Blueprint, render_template, request, flash, redirect, url_for, session
import mysql.connector
from mysql.connector import Error
import random
from datetime import datetime, timedelta
import json
from flask import jsonify

views = Blueprint('views', __name__)

@views.route('/access_request/<userId>/<passcode>', methods=['GET'])
def access_request(userId, passcode):

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
                SELECT users.Username 
                FROM passcode 
                INNER JOIN users ON users.UserID=passcode.UserID
                WHERE passcode.UserId=%s AND passcode.GenPasscode = %s;"""

            cursor.execute(select_query, (userId, passcode) )
            user = cursor.fetchall()  # Fetch all rows from the query result
            
            if user==[]:
                return 'False'
            
    except Error as e:
        flash(f"An error occurred while retrieving user data: {e}", category='error')

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    
        return 'True'  # Return True if the user exists


@views.route('/passcode', methods=['GET'])
def passcode():
    user_id = session.get('UserID')
    fetch_passcodes_query = """
        SELECT p.UserID, p.GenPasscode, ph.CreatedTime, ph.ExpiredTime
        FROM passcode p
        INNER JOIN passcodehistory ph ON p.PassID = ph.PassID
        WHERE p.UserID = %s
        ORDER BY ph.CreatedTime DESC;
    """

    passcodes = []  # Initialize an empty list for passcodes

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
            cursor.execute(fetch_passcodes_query, (user_id,))
            passcodes = cursor.fetchall()  # Fetch all passcodes for the user

    except Error as e:
        flash(f"An error occurred while fetching passcodes: {e}", category='error')

    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

    # Pass the passcodes to the template
    return render_template('PasscodePage.html', passcodes=passcodes)

@views.route('/generate_passcode', methods=['POST'])
def generate_passcode_button():
    connection = None  # Initialize connection to None
    try:
        # Generate a random passcode
        passcode = random.randint(1000, 9999)
        created_time = datetime.now()
        duration = timedelta(minutes=5)
        expired_at = created_time + duration

        user_id = session.get('UserID')

        if not user_id:
            flash('No user is logged in. Please log in to generate a passcode.', category='error')
            return redirect(url_for('auth.login'))

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

            # Insert the passcode into the passcode table
            insert_passcode_query = """
                INSERT INTO passcode (UserID, GenPasscode)
                VALUES (%s, %s);
            """
            cursor.execute(insert_passcode_query, (user_id, passcode))
            connection.commit()

            # Get the PasscodeID of the newly inserted passcode
            passcode_id = cursor.lastrowid

            # Insert the CreatedTime and ExpiredTime into the passcode_history table
            insert_history_query = """
                INSERT INTO passcodehistory (PassID, CreatedTime, ExpiredTime)
                VALUES (%s, %s, %s);
            """
            cursor.execute(insert_history_query, (passcode_id, created_time, expired_at))
            connection.commit()

            # Fetch all passcodes for the current user
            fetch_passcodes_query = """
                SELECT p.UserID, p.GenPasscode, ph.CreatedTime, ph.ExpiredTime
                FROM passcode p
                INNER JOIN passcodehistory ph ON p.PassID = ph.PassID
                WHERE p.UserID = %s
                ORDER BY ph.CreatedTime DESC;
            """
            cursor.execute(fetch_passcodes_query, (user_id,))
            passcodes = cursor.fetchall()  # Fetch all passcodes for the user

            # Display the passcode and its details on the screen
            flash(f"The passcode is: {passcode}", category='success')
            flash(f"The passcode was created at: {created_time.strftime('%Y-%m-%d %H:%M:%S')}", category='info')
            flash(f"The passcode will expire at: {expired_at.strftime('%Y-%m-%d %H:%M:%S')}", category='info')

    except Error as e:
        flash(f"An error occurred while storing the passcode: {e}", category='error')
        passcodes = []

    finally:
        # Safely close the connection if it was successfully initialized
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

    # Render the PasscodePage template with the passcodes
    return render_template('PasscodePage.html', passcodes=passcodes)

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
    
@views.route('/report', methods=['GET'])
def report():
    # Logic to fetch and display the report
    return render_template('Report.html')

@views.route('/verify_and_display', methods=['POST', 'GET'])
def verify_and_display():
    connection = None  # Initialize connection to None
    try:
        # Check if the Content-Type is application/json
        if request.content_type != 'application/json':
            flash('Invalid Content-Type. Expected application/json.', category='error')
            return render_template('Report.html', user=None)
        
        # Parse the JSON data from the request
        data = request.get_json()
        received_code = data.get('code')

        if not received_code:
            flash('No code provided', category='error')
            return render_template('Report.html', user=None)

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

            # Query to verify the passcode and fetch user data
            verify_query = """
                SELECT 
                    users.UserID, 
                    users.Username, 
                    passcode.CreatedTime, 
                    passcode.ExpiredTime, 
                    logs.EntryTime, 
                    rooms.RoomName
                FROM passcode
                INNER JOIN users ON passcode.UserID = users.UserID
                LEFT JOIN logs ON users.UserID = logs.UserID
                LEFT JOIN rooms ON logs.RoomID = rooms.RoomID
                WHERE passcode.GenPasscode = %s;
            """
            cursor.execute(verify_query, (received_code,))
            result = cursor.fetchone()

            if result:
                # If the passcode is valid, prepare user data
                user_data = {
                    'UserID': result[0],
                    'Username': result[1],
                    'CreatedTime': result[2],
                    'ExpiredTime': result[3],
                    'EntryTime': result[4],
                    'Room': result[5]
                }

                 # Generate the current EntryTime
                entry_time = datetime.now()

                # Insert or update the EntryTime in the logs table
                update_logs_query = """
                    INSERT INTO logs (UserID, EntryTime)
                    VALUES (%s, %s)
                    ON DUPLICATE KEY UPDATE EntryTime = VALUES(EntryTime);
                """
                cursor.execute(update_logs_query, (user_data['UserID'], entry_time))
                connection.commit()

                # Update the 'used' column in the logattempts table
                update_log_query = """
                    UPDATE logattempts
                    SET used = TRUE
                    WHERE GenPasscode = %s;
                """
                cursor.execute(update_log_query, (received_code,))
                connection.commit()

                # Pass the user data to the Report.html template
                return render_template('Report.html', user=user_data)
            else:
                # If the passcode is invalid, flash an error message
                flash('Invalid code', category='error')
                return render_template('Report.html', user=None)

    except Error as e:
        flash(f"Database error: {e}", category='error')
        return render_template('Report.html', user=None)

    finally:
        # Safely close the connection if it was successfully initialized
        if connection and connection.is_connected():
            cursor.close()
            connection.close()