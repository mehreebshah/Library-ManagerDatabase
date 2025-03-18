import psycopg2
from config import DB_CONFIG

def create_tables():
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    # 📚 Books Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id SERIAL PRIMARY KEY,      # 🆔 Unique ID
            title VARCHAR(255) NOT NULL,    # 📖 Title of the Book
            author VARCHAR(255) NOT NULL,    # ✍️ Author of the Book
            year INT NOT NULL,              # 📆 Year of Publication
            genre VARCHAR(100) NOT NULL,    # 📑 Genre of the Book
            read BOOLEAN DEFAULT FALSE,     # ✅ Read or Not
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP        # 🕒 Date Added
        );
    """)

    # 👤 Users Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (   
            id SERIAL PRIMARY KEY,     # 🆔 Unique ID
            name VARCHAR(100) NOT NULL,    # 👤 Name of the User
            email VARCHAR(100) UNIQUE NOT NULL,     # 📧 Email of the User
            joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP    # 🕒 Date Joined
        );
    """)

    # 🔄 Borrowed Books Table (Track which user borrowed which book)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS borrowed_books (
            id SERIAL PRIMARY KEY,      # 🆔 Unique ID
            user_id INT REFERENCES users(id) ON DELETE CASCADE,     # 👤 User ID
            book_id INT REFERENCES books(id) ON DELETE CASCADE,     # 📖 Book ID
            borrowed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,        # 🕒 Date Borrowed
            returned BOOLEAN DEFAULT FALSE              # 🔄 Returned or Not
        );
    """)

    # 🚀 Indexing for faster searching
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_books_title ON books(title);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);")

    conn.commit()           # 🚀 Commit the changes
    cursor.close()          # 🚀 Close the cursor
    conn.close()        # 🚀 Close the connection
    print("✅ All tables created successfully!")   # 🚀 Success message

# Run karein
if __name__ == "__main__":
    create_tables()
