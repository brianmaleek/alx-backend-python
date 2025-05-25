import aiosqlite
import asyncio

async def async_fetch_users():
    """Fetch all users from the database asynchronously"""
    try:
        async with aiosqlite.connect('users.db') as db:
            async with db.execute('SELECT * FROM users') as cursor:
                rows = await cursor.fetchall()
                print("All users:", rows)
                return rows
    except aiosqlite.Error as e:
        print(f"Error fetching all users: {e}")
        return []

async def async_fetch_older_users():
    """Fetch users older than 40 from the database asynchronously"""
    try:
        async with aiosqlite.connect('users.db') as db:
            async with db.execute('SELECT * FROM users WHERE age > ?', (40,)) as cursor:
                rows = await cursor.fetchall()
                print("Users older than 40:", rows)
                return rows
    except aiosqlite.Error as e:
        print(f"Error fetching older users: {e}")
        return []

async def setup_database():
    """Initialize database with sample data"""
    try:
        async with aiosqlite.connect('users.db') as db:
            await db.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    age INTEGER
                )
            ''')
            
            # Sample data
            users = [
                (1, "John Doe", 35),
                (2, "Jane Smith", 42),
                (3, "Bob Johnson", 45),
                (4, "Alice Brown", 38)
            ]
            
            await db.executemany(
                'INSERT OR REPLACE INTO users (id, name, age) VALUES (?, ?, ?)',
                users
            )
            await db.commit()
    except aiosqlite.Error as e:
        print(f"Error setting up database: {e}")

async def fetch_concurrently():
    """Execute both queries concurrently"""
    try:
        # Setup database first
        await setup_database()
        
        # Execute queries concurrently
        all_users, older_users = await asyncio.gather(
            async_fetch_users(),
            async_fetch_older_users()
        )
        
        return all_users, older_users
    except Exception as e:
        print(f"Error in concurrent execution: {e}")
        return [], []

def main():
    """Main function to run the async operations"""
    try:
        all_users, older_users = asyncio.run(fetch_concurrently())
        print("\nResults summary:")
        print(f"Total users: {len(all_users)}")
        print(f"Users over 40: {len(older_users)}")
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
    except Exception as e:
        print(f"Main execution error: {e}")

if __name__ == "__main__":
    main()