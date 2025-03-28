from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__) #Only use if you have not created the flask app


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/lock'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

@app.route('/')
def index():
    return "MySQL database connection is ready!"

if __name__ == '__main__':
    app.run(debug=True)