import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)

def stream_users():
    """
    Generator function that yields one row at a time from the users table
    Returns: yields a tuple containing user data
    """
    try:
        # Connect to the database
        connection = mysql.connector.connect(
            host=os.getenv("DATABASE_HOST"),
            user=os.getenv("DATABASE_USER"),
            password=os.getenv("DATABASE_PASSWORD"),
            database="ALX_prodev"
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            # Execute the query
            cursor.execute("SELECT * FROM users")
            
            # Fetch one row at a time
            while True:
                row = cursor.fetchone()
                if row is None:
                    break
                yield row
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        # Close the cursor and connection
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()

if __name__ == "__main__":
    # Test the generator
    for user in stream_users():
        if user:
            user_id, name, email, age = user
            print(f"User: {name}, Email: {email}, Age: {age}")
