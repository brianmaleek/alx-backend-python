import mysql.connector
import os
from dotenv import load_dotenv
from typing import List, Tuple, Generator

# Load environment variables
load_dotenv(override=True)

def paginate_users(page_size: int, offset: int = 0) -> List[Tuple]:
    """
    Fetch a page of users from the database
    Args:
        page_size: Number of records per page
        offset: Starting position for fetching records
    Returns:
        List of user records for the requested page
    """
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DATABASE_HOST"),
            user=os.getenv("DATABASE_USER"),
            password=os.getenv("DATABASE_PASSWORD"),
            database="ALX_prodev"
        )
        
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT user_id, name, email, age FROM user_data LIMIT %s OFFSET %s",
                (page_size, offset)
            )
            return cursor.fetchall()
            
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return []
    finally:
        if 'connection' in locals() and connection.is_connected():
            connection.close()

def lazy_pagination(page_size: int) -> Generator[List[Tuple], None, None]:
    """
    Generator function that yields pages of user data lazily
    Args:
        page_size: Number of records per page
    Yields:
        List of user records for each page
    """
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:  # Stop when no more records
            break
        yield page
        offset += page_size

if __name__ == "__main__":
    # Test lazy pagination
    for page_number, page in enumerate(lazy_paginate(3), 1):
        print(f"\nPage {page_number}:")
        for user in page:
            user_id, name, email, age = user
            print(f"User: {name}, Email: {email}, Age: {age}")

