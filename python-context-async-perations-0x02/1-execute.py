import sqlite3

class ExecuteQuery:
    def __init__(self, query, params=None, database_name="user.db"):
        """
        Initialize the query context manager
        
        Args:
            query (str): SQL query to execute
            params (tuple, optional): Query parameters
            database_name (str): Database file name
        """
        self.query = query
        self.params = params
        self.database_name = database_name
        self.connection = None
        self.cursor = None

    def __enter__(self):
        """
        Establish database connection and execute query
        
        Returns:
            list: Query results
        """
        try:
            self.connection = sqlite3.connect(self.database_name)
            self.cursor = self.connection.cursor()
            
            if self.params:
                self.cursor.execute(self.query, self.params)
            else:
                self.cursor.execute(self.query)
                
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            raise RuntimeError(f"Database error: {e}")

    def __exit__(self, exc_type, exc_val, traceback):
        """
        Clean up database resources
        
        Args:
            exc_type: Exception type if error occurred
            exc_val: Exception value if error occurred
            traceback: Traceback if error occurred
        """
        try:
            if self.cursor:
                self.cursor.close()
            if self.connection:
                if exc_type:
                    self.connection.rollback()
                else:
                    self.connection.commit()
                self.connection.close()
        except sqlite3.Error as e:
            print(f"Error during cleanup: {e}")
        return False

def main():
    # Create test table
    create_table = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT,
        age INTEGER
    )"""
    
    with ExecuteQuery(create_table) as _:
        pass

    # Insert test data
    sample_users = [
        ("John Doe", 30),
        ("Jane Smith", 22),
        ("Bob Wilson", 45)
    ]

    for user in sample_users:
        with ExecuteQuery(
            "INSERT INTO users (name, age) VALUES (?, ?)", 
            user
        ) as _:
            pass

    # Test the age query
    age_query = "SELECT * FROM users WHERE age > ?"
    with ExecuteQuery(age_query, (25,)) as results:
        print("Users older than 25:")
        for user in results:
            print(f"ID: {user[0]}, Name: {user[1]}, Age: {user[2]}")

if __name__ == "__main__":
    main()
