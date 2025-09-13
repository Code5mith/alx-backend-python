import sqlite3
import functools

def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if args:
            query = args[0]
            print(f"Executing SQL query: '{query}'")
        else:
            query = kwargs.get('query')
            if query:
                print(f"Executing SQL query: '{query}'")

        results = func(*args, **kwargs)
        return results

    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results
