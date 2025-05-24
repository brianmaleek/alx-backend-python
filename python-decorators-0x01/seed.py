import sqlite3
import csv


def create_database():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL,
            gender TEXT NOT NULL,
            race TEXT NOT NULL,
            phone_number TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

def insert_users_from_csv(csv_file):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    with open(csv_file, 'r', newline='', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        inserted = 0
        for row in csv_reader:
            try:
                cursor.execute('''
                    INSERT INTO users (id, first_name, last_name, email, gender, race, phone_number)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (int(row['id']), row['first_name'], row['last_name'], row['email'], row['gender'], row['Race'], row['Phone']))
                inserted += 1
            except sqlite3.IntegrityError:
                print(f"User with ID {row['id']} already exists. Skipping.")       

    conn.commit()
    print(f"Inserted {inserted} users from {csv_file} into the database.")
    conn.close()

def verify_data():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) FROM users')
    count = cursor.fetchone()[0]
    print(f"Total number of users in the database: {count}")

    cursor.execute('SELECT * FROM users LIMIT 5')
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    conn.close()

if __name__ == "__main__":
    create_database()
    insert_users_from_csv('users.csv')
    verify_data()
    print("Database setup and data insertion complete.")
