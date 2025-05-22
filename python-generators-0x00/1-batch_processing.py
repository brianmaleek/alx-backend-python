import mysql.connector
import os
from dotenv import load_dotenv
from typing import List, Tuple, Generator

# Load environment variables
load_dotenv(override=True)

def stream_users_in_batches(batch_size: int) -> Generator[List[Tuple], None, None]:
    """
    Generator function that yields batches of user data
    Args:
        batch_size: Number of records to fetch in each batch
    Yields:
        List of tuples containing user data
    """
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DATABASE_HOST"),
            user=os.getenv("DATABASE_USER"),
            password=os.getenv("DATABASE_PASSWORD"),
            database="ALX_prodev"
        )
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT user_id, name, email, age FROM user_data")
            while True:
                batch = cursor.fetchmany(batch_size)
                if not batch:
                    break
                yield batch
                
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            connection.close()

def batch_processing(batch_size) -> Generator[List[Tuple], None, None]:
    """
    Process batches of users and filter those over 25
    Args:
        batch_size: Size of each batch to process
    Yields:
        Filtered batch of users over 25
    """
    for batch in stream_users_in_batches(batch_size):
        filtered_batch = [user for user in batch if int(user[3]) > 25]
        if filtered_batch:
            yield filtered_batch

if __name__ == "__main__":
    # Test batch processing
    for processed_batch in batch_processing(batch_size=3):
        print("\nProcessed batch:")
        for user in processed_batch:
            user_id, name, email, age = user
            print(f"User: {name}, Age: {age}")