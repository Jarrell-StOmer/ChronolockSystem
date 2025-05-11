from flask import Blueprint , render_template, request, flash, redirect, url_for, session
from flask import Flask
import mysql.connector
from mysql.connector import Error
from connection import get_connection
auth = Blueprint('auth', __name__)


@auth.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get the username and password from the form
        username = request.form.get('username')
        password = request.form.get('password')

        try:
            # Connect to the database
            connection = get_connection()

            if connection.is_connected():
                cursor = connection.cursor()

                # Check if the user is an administrator
                admin_query = """
                    SELECT * FROM users
                    INNER JOIN userroles ON users.UserID = userroles.UserID
                    INNER JOIN roles ON userroles.RoleID = roles.RoleID
                    WHERE users.Username = %s AND users.UserPassword = %s AND roles.RoleName = 'Administrator';
                """
                cursor.execute(admin_query, (username, password))
                admin = cursor.fetchone()

                if admin:
                    session['UserID'] = admin[0]  # Store UserID in session
                    flash('Welcome, Administrator!', category='success')
                    return redirect(url_for('views.Admin_page'))  # Redirect to AdminManageUsers page

                # Check if the user is a regular user
                user_query = """
                    SELECT * FROM users
                    INNER JOIN userroles ON users.UserID = userroles.UserID
                    INNER JOIN roles ON userroles.RoleID = roles.RoleID
                    WHERE users.Username = %s AND users.UserPassword = %s AND roles.RoleName = 'User';
                """
                cursor.execute(user_query, (username, password))
                user = cursor.fetchone()

                if user:
                    session['UserID'] = user[0]  # Store UserID in session
                    flash('Welcome, User!', category='success')
                    return redirect(url_for('views.passcode'))  # Redirect to PasscodePage

                # If no match is found
                flash('Invalid credentials. Please try again.', category='error')

        except Error as e:
            flash(f"An error occurred: {e}", category='error')

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    return render_template('Login.html')

@auth.route('/logout', methods=['GET'])
def logout():
    # Clear the session
    session.clear()
    flash('You have been logged out.', category='success')
    return redirect(url_for('auth.login'))

