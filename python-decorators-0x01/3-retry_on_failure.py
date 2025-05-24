import time
import sqlite3 
import functools

#### paste your with_db_decorator here
def with_db_connection(func):
    # your code goes here
    '''Decorator to manage database connections.'''
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            result = func(conn, *args, **kwargs)
            return result
        finally:
            # close the connection
            conn.close()
    return wrapper

""" your code goes here"""
def retry_on_failure(retries=3, delay=1):
    '''
    Decorator to retry a function call on failure.
    It retries the function up to `retries` times with a delay between attempts.
    '''
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    print(f"Attempt {attempt + 1} failed: {e}")
                    if attempt < retries - 1:
                        time.sleep(delay)
            raise last_exception # Raise the last exception if all attempts fail
        return wrapper
    return decorator


@with_db_connection
@retry_on_failure(retries=3, delay=1)

def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

#### attempt to fetch users with automatic retry on failure

users = fetch_users_with_retry()
print(users)
