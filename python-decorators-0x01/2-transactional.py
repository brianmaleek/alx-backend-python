import sqlite3 
import functools

"""your code goes here"""
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

def transactional(func):
    '''
    Decorator to manage transactions.
    It ensures that the function is executed within a transaction context,
    committing if successful and rolling back in case of an exception.
    '''
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()
            return result
        except Exception as e:
            print(f"An error occurred: {e}")
            conn.rollback()
            raise e
    return wrapper

@with_db_connection 
@transactional 
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id)) 

#### Update user's email with automatic transaction handling 

try:
    update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
    print("Email updated successfully")
except Exception as e:
    print(f"Error updating email: {e}")
