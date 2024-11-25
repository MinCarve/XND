import re
from flask import Flask, render_template, flash, redirect, url_for, request
from flask_login import UserMixin, current_user, login_user, logout_user, login_manager, LoginManager, login_required
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import (StringField, PasswordField, SubmitField,              
                     BooleanField)
from wtforms.validators import DataRequired, Length, Email, EqualTo
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


CSRFProtect(app)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
csrf = CSRFProtect(app)
csrf.init_app(app)


login_manager = LoginManager(app)
login_manager.login_view = 'signin'
login_manager.login_message_category = 'info'
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20), unique = True, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    password = db.Column(db.String(60), nullable = False)

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(),  Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=20)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

def format_field_name(field_name):
    return ' '.join(word.capitalize() for word in field_name.split('_'))

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/index')
def redirect_to_root():
    return redirect('/', code=302)

@app.errorhandler(404) 
def not_found(e): 
  return render_template("404.html") 

@app.route("/logout", methods = ['GET', 'POST'])
def logout():
    if (request.method == "POST") & (request.form.get('post_header') == 'log out'):
    
        logout_user()
        return redirect(url_for('index'))
    return redirect(url_for('index'))

@app.route("/account")
@login_required
def account():
    if current_user.is_authenticated:
        return render_template("account.html", name=current_user.name)
    else:
        return redirect(url_for('signin'))



@app.route("/signin", methods = ['GET', 'POST'])
def signin():

    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email = login_form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, login_form.password.data):
            login_user(user, remember = login_form.remember.data)

            return redirect(url_for('index'))
        else:
            flash('Wrong email or password', 'danger')
            return redirect(url_for('signin'))
        
    return render_template("signin.html", login_form = login_form)

@app.route("/signup")
def signup():
    register_form = RegistrationForm()       
    return render_template("signup.html", register_form = register_form)


@app.route("/register", methods = ['GET', 'POST'])
def register():
    db.create_all()

    register_form = RegistrationForm()       
    if register_form.validate_on_submit():

        user = User.query.filter_by(
               email = register_form.email.data).first()
        
        if user:
            flash('This email is already in use', 'danger')
            return redirect(url_for('signup'))


        hashed_password =   bcrypt.generate_password_hash(register_form.password.data).decode('utf-8')
        user = User(name = register_form.name.data,
                    email = register_form.email.data,
                    password = hashed_password)
        
        reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
     
        # compiling regex
        pwcheck = re.compile(reg)
        
        # searching regex                 
        valid = re.search(pwcheck, register_form.password.data)
        if not valid:
            flash('Password must contain at least one uppercase letter, one lowercase letter, one number, one special character, and be between 8-20 characters long', 'danger')
            return redirect(url_for('signup'))


        db.session.add(user)
        db.session.commit()               

        print('Your account has been created. You can now log in!', 'success')
        return redirect(url_for('index'))
    
    else:
        for field, errors in register_form.errors.items():
            for error in errors:
                flash(f"Error in {format_field_name(field)}: {error}")
            return redirect(url_for('signup'))

    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)