import sqlite3

class DatabaseConnection:
    def __init__(self, database_name='user.db'):
        self.database_name = database_name
        self.connection = None
        self.cursor = None
    
    def __enter__(self):
        """
        Establishes a database connection and returns the cursor.
        """
        self.connection = sqlite3.connect(self.database_name)
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Closes the database connection.
        """
        if self.cursor:
            self.cursor.close()

        if self.connection:
            if exc_type is not None:
                # If an exception occurred, rollback the transaction
                self.connection.rollback()
            else:
                # If no exception, commit the transaction
                self.connection.commit()
        self.connection.close()

# Example usage
if __name__ == "__main__":
    # First, create and populate the table (for demonstration)
    with DatabaseConnection() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT,
                email TEXT
            )
        """)
        # Insert some sample data
        cursor.execute("INSERT OR IGNORE INTO users (name, email) VALUES (?, ?)",
                      ("Brian Maleek", "brianmaleek@example.com"))
        cursor.execute("INSERT OR IGNORE INTO users (name, email) VALUES (?, ?)",
                      ("Maleek Brian", "maleekbrian.com"))
        cursor.connection.commit()

    # Example usage
    with DatabaseConnection('user.db') as cursor:
        cursor.execute('SELECT * FROM users')
        results = cursor.fetchall()

        # Print the results
        for row in results:
            print(row)
