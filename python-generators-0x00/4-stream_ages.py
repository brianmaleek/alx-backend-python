import mysql.connector
import os
from dotenv import load_dotenv
from typing import Generator

# Load environment variables
load_dotenv(override=True)

def stream_user_ages() -> Generator[int, None, None]:
    """
    Generator function that yields user ages one by one
    Yields:
        int: Age of each user
    """
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DATABASE_HOST"),
            user=os.getenv("DATABASE_USER"),
            password=os.getenv("DATABASE_PASSWORD"),
            database="ALX_prodev"
        )
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT age FROM users")
            while True:
                row = cursor.fetchone()
                if not row:
                    break
                yield int(row[0])
                
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            connection.close()

def calculate_average_age() -> float:
    """
    Calculate average age using the stream_user_ages generator
    Returns:
        float: Average age of users
    """
    total_age = 0
    count = 0
    
    for age in stream_user_ages():
        total_age += age
        count += 1
    
    return total_age / count if count > 0 else 0

if __name__ == "__main__":
    average_age = calculate_average_age()
    print(f"Average age of users: {average_age:.2f}")
