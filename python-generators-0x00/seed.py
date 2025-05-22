import mysql.connector
import uuid
import csv
import os
from dotenv import load_dotenv

# Load environment variables before any database operations
load_dotenv(override=True)

# Add debug prints to verify environment variables
print(f"Database Host: {os.getenv('DATABASE_HOST')}")
print(f"Database User: {os.getenv('DATABASE_USER')}")
print(f"Database Password is set: {'Yes' if os.getenv('DATABASE_PASSWORD') else 'No'}")

def connect_db():
    # Connect to the MySQL database
    try:
        connection =  mysql.connector.connect(
            host=os.getenv("DATABASE_HOST"),
            user=os.getenv("DATABASE_USER"),
            password=os.getenv("DATABASE_PASSWORD")
        )
        if connection.is_connected():
            print("Connected to MySQL database")
            return connection

    except mysql.connector.Error as err:
        print(f"Error connecting to mySQL: {err}")
        return None

def create_database(connection):
    # Create the ALX_prodev database if it doesn't exist
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        connection.commit()
        print("Database ALX_prodev created successfully or already exists")
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error creating database: {err}")

def connect_to_prodev():
    # Connect to the ALX_prodev database
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DATABASE_HOST"),
            user=os.getenv("DATABASE_USER"),
            password=os.getenv("DATABASE_PASSWORD"),
            database="ALX_prodev"
        )
        if connection.is_connected():
            print("Connected to ALX_prodev database")
            return connection

    except mysql.connector.Error as err:
        print(f"Error connecting to ALX_prodev: {err}")
        return None

def create_table(connection):
    # Create the users table if it doesn't exist
    try:
        cursor = connection.cursor()
        create_table = """
            CREATE TABLE IF NOT EXISTS user_data (
                user_id VARCHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL UNIQUE,
                age INT NOT NULL,
                INDEX idx_user_id (user_id)
            )
        """
        cursor.execute(create_table)
        connection.commit()
        print("Table users data created successfully or already exists")
        cursor.close()
        return True
    except mysql.connector.Error as err:
        print(f"Error creating table: {err}")
        # Rollback incase of error
        if connection.is_connected():
            connection.rollback()
        return False

def insert_data(connection, csv_file):
    try:
        cursor = connection.cursor()
        with open(csv_file, 'r') as file:
            # Use DictReader instead of reader
            csv_reader = csv.DictReader(file)
            for data in csv_reader:
                params = (str(uuid.uuid4()), data['name'], data['email'], data['age'])
                cursor.execute("""
                    INSERT INTO user_data (user_id, name, email, age) 
                    VALUES (%s, %s, %s, %s)
                """, params)
        connection.commit()
        print("Data inserted successfully")
    except Exception as e:
        print(f"Error inserting data: {e}")
    finally:
        cursor.close()

def main():
    """ Main function to execute the script """
    # Connect to the database
    server_connection = connect_db()
    if server_connection is None:
        return

    # Create the database
    create_database(server_connection)
    server_connection.close()

    # Connect to the ALX_prodev database
    prodev_connection = connect_to_prodev()
    if prodev_connection is None:
        return

    # Create the users table
    if not create_table(prodev_connection):
        prodev_connection.close()
        return

    # Read data from the CSV file and insert it into the users table
    try:
        insert_data(prodev_connection, 'user_data.csv')
    except FileNotFoundError:
        print("CSV file not found. Please ensure the file exists in the same directory as this script.")
    except Exception as e:
        print(f"An error occurred while reading the CSV file: {e}")
    finally:
        if prodev_connection.is_connected():
            prodev_connection.close()
            print("Database connection closed")

if __name__ == "__main__":
    main()

# Uncomment the following line to print the database connection
db = connect_to_prodev()
if db:
    print("Database connection object:", db)
else:
    print("Failed to connect to the database")

