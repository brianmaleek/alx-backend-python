import time
import sqlite3 
import functools


query_cache = {}

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

def cache_query(func):
    '''
    Decorator to cache the results of a query.
    It stores the results in a dictionary using the query as the key.
    If the query has been executed before, it returns the cached result.
    '''
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        query = kwargs.get('query', None) or args[0]
        if query in query_cache:
            print("Returning cached result for query:", query)
            return query_cache[query]
        else:
            print("Executing new query:", query)
            result = func(conn, *args, **kwargs)
            query_cache[query] = result
            return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

#### First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

#### Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")