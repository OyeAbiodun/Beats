from flask import Flask, render_template, redirect, url_for, request, session, flash
from db.connection import setup_database
from db.model import register_user, verify_user, verify_admin
from werkzeug.security import generate_password_hash, check_password_hash
from admin_dashboard import admin_dashboard
import os


app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'default_key')
DATABASE_URL = os.environ.get('DATABASE_URL')

setup_database()

@app.route('/')
def welcome():
    return render_template('welcome.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_data = {
            'first_name': request.form['firstName'],
            'surname': request.form['surname'],
            'email': request.form['email'],
            'password': generate_password_hash(request.form['password']),  # Hash the password here
            'phone_no': request.form['phoneNo'],
            'country': request.form['country'],
            'state': request.form['state'],
            'address': request.form['address'],
            'zip_code': request.form['zipCode']
        }

        registration_status = register_user(user_data)

        # Check if registration was successful and show flash message on the login page
        if "successful" in registration_status:
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        else:
            flash(registration_status, 'danger')

    return render_template('register.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['username']
        password = request.form['password']


        user = verify_user(email, password)
        admin = verify_admin(email, password)

        if user:
            session['user_id'] = user['user_id']
            flash(f'Welcome, {email}!', 'success')
            return redirect(url_for('user_dashboard'))
        elif admin:
            session['admin_id'] = admin['admin_id']
            flash(f'Welcome, Admin!', 'success')
            return redirect(url_for('admin_dashboard.index'))
        else:
            flash("Invalid email or password", "danger")

    return render_template('login.html')


@app.route('/user_dashboard')
def user_dashboard():
    return render_template('media_player.html')


@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        # Here you can add the logic to handle the forgot password functionality,
        # like generating a reset token and sending an email.
        flash("If this email is registered, a reset link will be sent.")
        return redirect(url_for('login'))
    return render_template('forgot_password.html')


app.register_blueprint(admin_dashboard, url_prefix='/admin_dashboard')




if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
