from flask import Flask
import mysql.connector
from mysql.connector import Error
import traceback
import os
import secrets
print(secrets.token_hex(16))
			
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')
    

    from .views import views
    from .auth import auth
    
    app.register_blueprint(auth, url_prefix='/')

    app.register_blueprint(views, url_prefix='/')
    
    
    return app
