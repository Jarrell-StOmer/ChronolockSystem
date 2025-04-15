from flask import Blueprint , render_template, request, flash, redirect, url_for, session
from flask import Flask
import mysql.connector
from mysql.connector import Error
auth = Blueprint('auth', __name__)


@auth.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Check if the login is for an administrator
        admin_username = request.form.get('Adminusername')
        admin_password = request.form.get('Adminpassword')

        # Check if the login is for a regular user
        user_username = request.form.get('username')
        user_password = request.form.get('password')

        user_id = session.get('UserID')


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

                # If admin credentials are provided
                if admin_username and admin_password:
                    admin_query = """
                        SELECT * FROM users
                        INNER JOIN userroles ON users.UserID = userroles.UserID
                        INNER JOIN roles ON userroles.RoleID = roles.RoleID
                        WHERE users.Username = %s AND users.UserPassword = %s AND roles.RoleName = 'Administrator';
                    """
                    cursor.execute(admin_query, (admin_username, admin_password))
                    admin = cursor.fetchone()

                    if admin:
                        session['UserID'] = admin[0]  # Store UserID in session
                        flash('Welcome, Administrator!', category='success')
                        return redirect(url_for('views.Admin_page'))  # Redirect to AdminManageUsers page
                    else:
                        flash('Invalid administrator credentials.', category='error')

                # If user credentials are provided
                elif user_username and user_password:
                    user_query = """
                        SELECT * FROM users
                        INNER JOIN userroles ON users.UserID = userroles.UserID
                        INNER JOIN roles ON userroles.RoleID = roles.RoleID
                        WHERE users.Username = %s AND users.UserPassword = %s AND roles.RoleName = 'User';
                    """
                    cursor.execute(user_query, (user_username, user_password))
                    user = cursor.fetchone()

                    if user:
                        session['UserID'] = user[0]  # Store UserID in session
                        print(f"Session UserID set to: {session['UserID']}")
                        flash('Welcome, User!', category='success')
                        return redirect(url_for('views.passcode'))  # Redirect to PasscodePage
                    if user:
                        print(f"User found: {user}")
                    else:
                        flash('Invalid user credentials.', category='error')

                else:
                    flash('Please fill in all required fields.', category='error')

        except Error as e:
            flash(f"An error occurred: {e}", category='error')

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    
    return render_template('Login.html')



'''@auth.route('/createuser', methods=['Get','POST'])
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

    return render_template('Createuser.html')'''