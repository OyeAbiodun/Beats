from db.connection import create_connection
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize the Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:@cndro25aackk@100.119.29.70:5432/your_database_name' # Update with your actual DB URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable unnecessary tracking of object modifications

# Initialize the SQLAlchemy object
db = SQLAlchemy(app)
# ---- User Operations ----

def register_user(user_data):
    connection = create_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM Beatz_Users WHERE email = %s", (user_data['email'],))
                if cursor.fetchone():
                    return "User with this email already exists."

                # Hash the password before saving it
                user_data['password'] = generate_password_hash(user_data['password'])

                cursor.execute('''
                    INSERT INTO Beatz_Users 
                    (first_name, surname, email, password, phone_no, country, state, address, zip_code)
                    VALUES 
                    (%(first_name)s, %(surname)s, %(email)s, %(password)s, %(phone_no)s, %(country)s, %(state)s, %(address)s, %(zip_code)s)
                ''', user_data)
                connection.commit()
                return "Registration successful."
        except Exception as e:
            connection.rollback()  # Rollback if there's an error during the transaction
            return f"Error during registration: {e}"
        finally:
            connection.close()
    return "Database connection failed."


def verify_user(email, password):
    connection = create_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT user_id, password FROM Beatz_Users WHERE email = %s", (email,))
                user = cursor.fetchone()

                # Check if the password is correct
                if user and check_password_hash(user[1], password):
                    return {"user_id": user[0]}
                else:
                    return None
        except Exception as e:
            return f"Error during user verification: {e}"
        finally:
            connection.close()
    return None


# ---- Admin Operations ----

def create_admin(admin_data):
    connection = create_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM admin_users WHERE email = %s", (admin_data['email'],))
                if cursor.fetchone():
                    return "Admin with this email already exists."

                # Hash the password before saving it
                admin_data['password'] = generate_password_hash(admin_data['password'])

                cursor.execute('''
                    INSERT INTO admin_users 
                    (first_name, last_name, email, password)
                    VALUES 
                    (%(first_name)s, %(last_name)s, %(email)s, %(password)s)
                ''', admin_data)
                connection.commit()
                return "Admin registration successful."
        except Exception as e:
            connection.rollback()  # Rollback if there's an error during the transaction
            return f"Error during admin registration: {e}"
        finally:
            connection.close()
    return "Database connection failed."


def verify_admin(email, password):
    connection = create_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT admin_id, password FROM admin_users WHERE email = %s", (email,))
                admin = cursor.fetchone()

                # Check if the password is correct
                if admin and check_password_hash(admin[1], password):
                    return {"admin_id": admin[0]}
                else:
                    return None
        except Exception as e:
            return f"Error during admin verification: {e}"
        finally:
            connection.close()
    return None


# ---- Beat Operations ----

def upload_beat(beat_name, filepath):
    connection = create_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO Beats (name, filepath) VALUES (%s, %s)", (beat_name, filepath))
                connection.commit()
                return "Beat uploaded successfully."
        except Exception as e:
            connection.rollback()  # Rollback if there's an error during the transaction
            return f"Error uploading beat: {e}"
        finally:
            connection.close()
    return "Database connection failed."


def get_all_beats():
    connection = create_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM Beats ORDER BY upload_date DESC")
                beats = cursor.fetchall()
                return beats
        except Exception as e:
            return f"Error fetching beats: {e}"
        finally:
            connection.close()
    return []

# db/model.py


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    surname = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))
    phone_no = db.Column(db.String(20))
    country = db.Column(db.String(50))
    state = db.Column(db.String(50))
    address = db.Column(db.String(200))
    zip_code = db.Column(db.String(10))

class Admin(db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))

class Beat(db.Model):
    __tablename__ = 'beats'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255))
    admin_id = db.Column(db.Integer, db.ForeignKey('admins.id'))
    admin = db.relationship('Admin', backref='beats')
