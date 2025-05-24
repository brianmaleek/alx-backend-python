import sqlite3
import functools
from datetime import datetime

#### decorator to lof SQL queries

""" YOUR CODE GOES HERE"""
def log_queries(func):
    '''
    Decorator to log SQL queries executed by the function.
    It prints the query before executing it.
    '''
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get('query', None) or args[0]
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if query:
            print(f"{timestamp}: Executing query: {query}")
        return func(*args, **kwargs)
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

#### fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")
