import psycopg2
from config import DB_CONFIG

# ✅ Connect to Database
def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

# ✅ Create Tables
def create_tables():
    conn = get_db_connection()
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
            name VARCHAR(255) NOT NULL
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS borrowed_books (
            id SERIAL PRIMARY KEY,
            user_id INT REFERENCES users(id) ON DELETE CASCADE,
            book_id INT REFERENCES books(id) ON DELETE CASCADE,
            borrowed_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    
    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Tables Created Successfully!")

# ✅ Add Book
def add_book(title, author, year, genre, read):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO books (title, author, year, genre, read) VALUES (%s, %s, %s, %s, %s)", 
                   (title, author, year, genre, read))
    
    conn.commit()
    cursor.close()
    conn.close()

# ✅ Remove Book
def remove_book(title):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM books WHERE title = %s", (title,))
    
    conn.commit()
    cursor.close()
    conn.close()

# ✅ Display Books
def display_books():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return books

# ✅ Add User
def add_user(name):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO users (name) VALUES (%s)", (name,))
    
    conn.commit()
    cursor.close()
    conn.close()

# ✅ Display Users
def display_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return users

# ✅ Borrow Book
def borrow_book(user_id, book_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if book exists
    cursor.execute("SELECT id FROM books WHERE id = %s", (book_id,))
    book = cursor.fetchone()
    
    if not book:
        print("❌ Book ID not found!")
        return
    
    # Insert into borrowed_books
    cursor.execute("INSERT INTO borrowed_books (user_id, book_id) VALUES (%s, %s)", (user_id, book_id))
    
    conn.commit()
    cursor.close()
    conn.close()

# ✅ Return Book
def return_book(user_id, book_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM borrowed_books WHERE user_id = %s AND book_id = %s", (user_id, book_id))
    
    conn.commit()
    cursor.close()
    conn.close()

# ✅ Display Borrowed Books
def display_borrowed_books():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT users.name, books.title, borrowed_books.borrowed_at 
        FROM borrowed_books
        JOIN users ON borrowed_books.user_id = users.id
        JOIN books ON borrowed_books.book_id = books.id
    """)
    
    borrowed_books = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return borrowed_books

# ✅ Run Tables Creation
if __name__ == "__main__":
    create_tables()
