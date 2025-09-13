import time
import sqlite3 
import functools

#### paste your with_db_decorator here

""" your code goes here"""

def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = None
        try:
            conn = sqlite3.connect(':memory:')
            result = func(conn, *args, **kwargs)
            return result
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            raise
        finally:
            if conn:
                conn.close()
                print("Database connection closed.")
    return wrapper

def retry_on_failure(retries=3, delay=2):
    """Decorator to retry a function on failure with specified retries and delay."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(retries):
                try:
                    result = func(*args, **kwargs)
                    return result
                except Exception as e:
                    last_error = e
                    print(f"Attempt {attempt + 1} failed with error: {e}")
                    if attempt < retries - 1:  # Don't sleep on last attempt
                        time.sleep(delay)
            raise last_error  # Raise the last exception if all retries fail
        return wrapper
    return decorator

def retry_on_failure(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs): 
        conn = args[0] 
        try:
            for arg in range(args[0]):
                result = func(*args, **kwargs)
                if result == Exception:
                    print("Failed!")
                    time.sleep(args[1])
                    func(*args, **kwargs)
                return result
        except Exception as e:
            conn.rollback()
            print(f"Transaction rolled back due to error: {e}")
            raise


@with_db_connection
@retry_on_failure(retries=3, delay=1)

def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

#### attempt to fetch users with automatic retry on failure

users = fetch_users_with_retry()
print(users)