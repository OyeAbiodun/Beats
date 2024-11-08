import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from werkzeug.security import generate_password_hash

# Database configuration
DB_NAME = "postgres"
DB_USER = "postgres"  # Replace with your PostgreSQL username
DB_PASSWORD = "@Abiodun8."  # Replace with your PostgreSQL password
DB_HOST = "localhost"
DB_PORT = "5432"

# Default admin credentials
DEFAULT_ADMIN_EMAIL = "admin@beatzapp.com"
DEFAULT_ADMIN_PASSWORD = "admin123"  # You can change this password later

# Establishing a connection to the PostgreSQL database
def create_connection():
    try:
        connection = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        return connection
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

# Function to set up database tables and create a default admin
def setup_database():
    connection = create_connection()
    if connection:
        try:
            with connection.cursor() as cursor:
                # Create Beatz_Users table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS Beatz_Users (
                        user_id SERIAL PRIMARY KEY,
                        first_name VARCHAR(50) NOT NULL,
                        surname VARCHAR(50) NOT NULL,
                        email VARCHAR(100) UNIQUE NOT NULL,
                        password TEXT NOT NULL,
                        phone_no VARCHAR(20),
                        country VARCHAR(50),
                        state VARCHAR(50),
                        address TEXT,
                        zip_code VARCHAR(20)
                    );
                ''')

                # Create admin_users table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS admin_users (
                        admin_id SERIAL PRIMARY KEY,
                        first_name VARCHAR(50),
                        last_name VARCHAR(50),
                        email VARCHAR(100) UNIQUE NOT NULL,
                        password VARCHAR(255) NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                ''')

                # Create Beats table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS Beats (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(100) NOT NULL,
                        filepath TEXT,
                        upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                ''')

                # Create User_Statistics table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS User_Statistics (
                        id SERIAL PRIMARY KEY,
                        user_id INT REFERENCES Beatz_Users(user_id) ON DELETE CASCADE,
                        downloads INT DEFAULT 0,
                        playlists_created INT DEFAULT 0
                    );
                ''')

                # Check if the default admin exists, if not, create one
                cursor.execute("SELECT * FROM admin_users WHERE email = %s", (DEFAULT_ADMIN_EMAIL,))
                if cursor.fetchone() is None:
                    # Insert default admin with hashed password
                    hashed_password = generate_password_hash(DEFAULT_ADMIN_PASSWORD)
                    cursor.execute('''
                        INSERT INTO admin_users (first_name, last_name, email, password)
                        VALUES (%s, %s, %s, %s)
                    ''', ("Admin", "User", DEFAULT_ADMIN_EMAIL, hashed_password))

                    print("Default admin created successfully.")
                else:
                    print("Default admin already exists.")

                print("Tables created successfully.")
        except Exception as e:
            print(f"Error creating tables or default admin: {e}")
        finally:
            connection.close()
