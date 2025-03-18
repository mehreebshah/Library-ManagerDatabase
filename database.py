import psycopg2   # ✅ Import psycopg2 library
from config import DB_CONFIG   # ✅ Import DB_CONFIG from config.py

def connect_db():       #  Create a function to connect to the database
    return psycopg2.connect(**DB_CONFIG)

def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            author VARCHAR(255) NOT NULL,
            year INT NOT NULL,
            genre VARCHAR(100) NOT NULL,
            read BOOLEAN DEFAULT FALSE
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS borrowed_books (
            id SERIAL PRIMARY KEY,
            user_id INT REFERENCES users(id) ON DELETE CASCADE,
            book_id INT REFERENCES books(id) ON DELETE CASCADE,
            borrow_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Tables created successfully!")

if __name__ == "__main__":
    create_tables()
