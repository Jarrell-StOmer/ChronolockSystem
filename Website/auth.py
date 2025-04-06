from flask import Blueprint , render_template, request, flash

auth = Blueprint('auth', __name__)

@auth.route('/', methods=['GET', 'POST'])
def login():
    return render_template('Login.html')



@auth.route('/createuser', methods=['Get','POST'])
def createuser():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
       
        """ if len(password) < 5:
            flash('Password must be at least 5 characters long.', category='error')
        elif len(username) < 2:
            flash('Username must be at least 2 characters long.', category='error')
        else:
            flash('User created!', category='success')
        pass"""
        
    return render_template('Createuser.html')
