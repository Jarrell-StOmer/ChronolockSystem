from flask import Flask
import mysql.connector
from mysql.connector import Error
import traceback

			
def create_app():
    app = Flask(__name__)
    app.config['SECRET KEY'] = 'a3f5c8d9e2b4f7a1c6d8e9f0b2a4c7d89'
    

    from .views import views
    from .auth import auth
    
    app.register_blueprint(auth, url_prefix='/')

    app.register_blueprint(views, url_prefix='/')
    
    
    return app
