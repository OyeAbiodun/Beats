from flask import Blueprint, render_template, session, redirect, url_for, flash, request, send_file
from db.connection import create_connection  # Import create_connection from db.connection
from werkzeug.utils import secure_filename
import os
from werkzeug.security import generate_password_hash

# Create the Blueprint for the admin dashboard
admin_dashboard = Blueprint('admin_dashboard', __name__)


# Helper function for file validation (only mp3, wav are allowed)
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'mp3', 'wav'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Route for the dashboard
@admin_dashboard.route('/')
def index():
    if 'admin_id' not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in
    return render_template('admin_dashboard.html')


# Route to view users
@admin_dashboard.route('/view_users')
def view_users():
    if 'admin_id' not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in
    connection = create_connection()
    if connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Beatz_Users")  # Adjust the query for your user model
            users = cursor.fetchall()  # Fetch all users from the database
        return render_template('view_users.html', users=users)
    else:
        flash('Error connecting to the database.', 'danger')
        return redirect(url_for('admin_dashboard.index'))


# Route to create a new admin
from werkzeug.security import generate_password_hash


@admin_dashboard.route('/create_admin', methods=['GET', 'POST'])
def create_admin():
    if 'admin_id' not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in

    if request.method == 'POST':
        first_name = request.form.get('firstName')  # Correcting the field name
        surname = request.form.get('surname')  # Correcting the field name
        email = request.form.get('email')
        password = request.form.get('password')  # Get password from form

        # Hash the password before storing it
        hashed_password = generate_password_hash(password)

        connection = create_connection()
        if connection:
            with connection.cursor() as cursor:
                # Check if the admin already exists by email
                cursor.execute("SELECT * FROM admin_users WHERE email = %s", (email,))
                if cursor.fetchone():  # Check if an admin with the same email exists
                    flash('An admin with this email already exists!', 'danger')
                    return redirect(url_for('admin_dashboard.create_admin'))

                # Insert new admin into the database with hashed password
                cursor.execute('''INSERT INTO admin_users (first_name, last_name, email, password)
                                  VALUES (%s, %s, %s, %s)''',
                               (first_name, surname, email, hashed_password))
                connection.commit()  # Commit the new admin record

            flash('New admin created successfully!', 'success')
        else:
            flash('Error connecting to the database.', 'danger')

        return redirect(url_for('admin_dashboard.index'))  # Redirect to the dashboard after success

    return render_template('create_admin.html')  # Return the form to create a new admin


# Route to manage admin profiles
@admin_dashboard.route('/manage_admins')
def manage_admins():
    if 'admin_id' not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in
    connection = create_connection()
    if connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM admin_users")  # Fetch all admin profiles
            admins = cursor.fetchall()
        return render_template('manage_admins.html', admins=admins)
    else:
        flash('Error connecting to the database.', 'danger')
        return redirect(url_for('admin_dashboard.index'))


# Route to upload beats
@admin_dashboard.route('/upload_beats', methods=['GET', 'POST'])
def upload_beats():
    if 'admin_id' not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in
    if request.method == 'POST':
        file = request.files['beat_file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            upload_folder = os.path.join(os.getcwd(), 'path_to_upload_folder')  # Use dynamic folder path
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)  # Ensure folder exists
            file.save(os.path.join(upload_folder, filename))  # Adjust the path as needed

            connection = create_connection()
            if connection:
                with connection.cursor() as cursor:
                    cursor.execute('''INSERT INTO Beats (name, filepath, admin_id) 
                                      VALUES (%s, %s, %s)''',
                                   (filename, upload_folder, session['admin_id']))
                    connection.commit()
            flash('Beats uploaded successfully!', 'success')
        else:
            flash('Invalid file type. Only mp3, wav files are allowed.', 'danger')
        return redirect(url_for('admin_dashboard.index'))

    return render_template('upload_beats.html')


# Route for the media player
@admin_dashboard.route('/admin_media_player')
def admin_media_player():
    if 'admin_id' not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in
    connection = create_connection()
    if connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Beats WHERE admin_id = %s",
                           (session['admin_id'],))  # Get beats uploaded by admin
            beats = cursor.fetchall()
        return render_template('admin_media_player.html', beats=beats)
    else:
        flash('Error connecting to the database.', 'danger')
        return redirect(url_for('admin_dashboard.index'))


# Route to display user statistics
@admin_dashboard.route('/user_statistics')
def user_statistics():
    if 'admin_id' not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in
    connection = create_connection()
    if connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM Beatz_Users")  # Get total user count
            total_users = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM Beatz_Users WHERE is_active = TRUE")  # Get active users
            active_users = cursor.fetchone()[0]
            inactive_users = total_users - active_users
            stats = {
                'total_users': total_users,
                'active_users': active_users,
                'inactive_users': inactive_users
            }
        return render_template('user_statistics.html', statistics=stats)
    else:
        flash('Error connecting to the database.', 'danger')
        return redirect(url_for('admin_dashboard.index'))


# Route to download data
@admin_dashboard.route('/download_data')
def download_data():
    if 'admin_id' not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in
    connection = create_connection()
    if connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Beatz_Users")  # Fetch all users
            users = cursor.fetchall()

        import csv
        from io import StringIO

        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(['ID', 'First Name', 'Last Name', 'Email', 'Phone Number'])  # Column names

        for user in users:
            writer.writerow(user)  # Adjust according to your user columns

        output.seek(0)
        return send_file(output, as_attachment=True, download_name="user_data.csv", mimetype="text/csv")
    else:
        flash('Error connecting to the database.', 'danger')
        return redirect(url_for('admin_dashboard.index'))


# Route for logging out
@admin_dashboard.route('/logout')
def logout():
    session.pop('admin_id', None)  # Remove admin session
    flash('Logged out successfully!', 'info')
    return redirect(url_for('login'))  # Redirect to login page
