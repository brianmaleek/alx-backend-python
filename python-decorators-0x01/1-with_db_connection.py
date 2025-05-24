import sqlite3 
import functools

def with_db_connection(func):
    # your code goes here
    '''
    Decorator to manage database connections.
    It ensures that a connection is opened before the function call
    and closed after the function execution, handling exceptions and committing transactions.
    '''
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            # call the wrapped function with the connection as the first argument and any additional arguments
            result = func(conn, *args, **kwargs)
            conn.commit()
            return result
        except Exception as e:
            print(f"An error occurred: {e}")
            conn.rollback()
        finally:
            # close the connection
            conn.close()
    return wrapper

@with_db_connection 
def get_user_by_id(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone() 

#### Fetch user by ID with automatic connection handling 

user = get_user_by_id(user_id=1)
print(user)
