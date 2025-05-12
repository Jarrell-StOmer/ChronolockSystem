init.py
The __init__.py file is responsible for initializing the Flask application and setting up the application structure. It acts as the entry point for the application and typically contains the following responsibilities:
1. Initializing the Flask application.
2. Registering blueprints for modular routing.
3. Setting application-wide configurations.
4. Initializing Flask extensions.
5. Following the application factory pattern for flexibility.


   
auth.py
The auth.py file in this code is responsible for handling authentication and session management for the application. It defines routes and logic for user login and logout, ensuring that users can securely access the application based on their roles (e.g., Administrator or User).
Login:
Authenticate users based on their credentials.
Redirect users to different pages based on their roles (Administrator or User).

Logout:
Clear session data and redirect users to the login page.

Database Interaction:
Query the database to verify credentials and roles.

Session Management:
Store and clear session data for logged-in users.

Error Handling:
Handle database errors and display appropriate messages to the user.


connection.py
The connection.py file is responsible for managing the database connection in your application. It provides a centralized function, get_connection(), to establish a connection to the MySQL database. This helps reduce redundancy and ensures consistent database connection logic across the application.


views.py
The views.py file in your Flask application is responsible for defining the core routes and business logic of the application. It handles user interactions, processes requests, interacts with the database, and renders templates to display data to the user
1. Defining routes for core functionalities.
2. Handling user interactions and inputs.
3. Interacting with the database to fetch, insert, or update data.
4. Rendering templates to display data to users.
5. Managing sessions and providing feedback through flash() messages.
6. Implementing business logic for passcode management, user management, and reporting.


main.py
The main.py file serves as the entry point for your Flask application. Its primary purpose is to initialize and run the Flask application by calling the create_app() function from the __init__.py file in the Website package.


Adminmanageusers.html
The Adminmanageusers.html file is responsible for providing the Administrator Management Interface in your application. It allows administrators to manage users by adding or deleting them, as well as viewing a list of all users and their roles. This page is specifically designed for administrators to perform user management tasks such as:
1. View all users and their roles.
2. Add new users with specific roles.
3. Delete existing users.
4. Navigate to other functionalities like reports.
5. Logout securely.


Login.html
The Login.html page is responsible for providing the login interface for users of the application. It allows users to enter their credentials (username and password) to authenticate and gain access to the system. The Login.html page is responsible for:
1. Providing a login form for user authentication.
2. Sending user credentials to the backend for verification.
3. Displaying error messages in case of login failure.
4. Ensuring a responsive and user-friendly design.



Passcode.html
The PasscodePage.html file is responsible for providing the Passcode Management Interface for users. It allows users to generate new passcodes, view their existing passcodes, and log out of the application. This page is specifically designed for users to manage their passcodes efficiently. The PasscodePage.html file is responsible for:
1. Allowing users to generate new passcodes.
2. Displaying a table of existing passcodes with details.
3. Showing flash messages for feedback (e.g., success or error messages).
4. Providing a logout button for secure session termination.
5. Ensuring a responsive and visually appealing design.


Report.html
The Report.html file is responsible for providing the Administrator Report Interface in your application. It allows administrators to view detailed information about users, including their passcodes, creation times, expiration times, entry times, and associated rooms. This page is designed to display user-specific data in a structured and readable format. The Report.html file is responsible for:
1. Displaying detailed user data in a table format.
2. Handling cases where no user data is available.
3. Providing navigation back to the user management page.
4. Offering a clean and responsive design for administrators.
