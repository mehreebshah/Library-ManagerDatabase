import os
import streamlit as st
from crud import add_book, remove_book, display_books, add_user, borrow_book, return_book, display_users, display_borrowed_books

# 🎨 Streamlit Page Config
st.set_page_config(page_title="Library Management System", page_icon="📚", layout="wide")

# 📌 Library Logo Handling
logo_path = "library_logo.png"
if os.path.exists(logo_path):
    st.sidebar.image(logo_path, use_container_width=True)
else:
    st.sidebar.write("📚 Library Management System")

# 🌟 Sidebar Menu
st.sidebar.title("📌 Library Actions")
option = st.sidebar.radio("Select an action", ["📖 Add Book", "🗑 Remove Book", "📚 View Books", "👤 Manage Users", "📙 Borrow/Return Books"])

# ✅ 📖 Add Book
if option == "📖 Add Book":
    st.subheader("➕ Add a New Book")
    col1, col2 = st.columns(2)
    
    with col1:
        title = st.text_input("📖 Book Title")
        author = st.text_input("✍️ Author")
    
    with col2:
        year = st.number_input("📆 Year", min_value=1000, max_value=2100, step=1)
        genre = st.text_input("📑 Genre")
    
    read = st.checkbox("✅ Read")
    
    if st.button("📚 Add Book"):
        add_book(title, author, year, genre, read)
        st.success(f'✅ Book "{title}" Added!')

# ✅ 🗑 Remove Book
elif option == "🗑 Remove Book":
    st.subheader("❌ Remove a Book")
    title = st.text_input("📖 Enter Book Title to Remove")
    
    if st.button("🗑 Remove Book"):
        remove_book(title)
        st.warning(f'⚠️ Book "{title}" Removed!')

# ✅ 📚 View Books
elif option == "📚 View Books":
    st.subheader("📚 Library Collection")
    search_query = st.text_input("🔍 Search Book by Title or Author")
    
    books = display_books()
    if search_query:
        books = [book for book in books if search_query.lower() in book[1].lower() or search_query.lower() in book[2].lower()]
    
    if books:
        for book in books:
            st.markdown(f"""
            🆔 **ID:** {book[0]}  
            📖 **Title:** {book[1]}  
            ✍️ **Author:** {book[2]}  
            📆 **Year:** {book[3]}  
            📑 **Genre:** {book[4]}  
            ✅ **Read:** {'Yes' if book[5] else 'No'}  
            ---
            """)
    else:
        st.warning("⚠️ No Books Found!")

# ✅ 👤 Manage Users
elif option == "👤 Manage Users":
    st.subheader("👤 Library Users")
    name = st.text_input("👤 Enter User Name")
    
    if st.button("➕ Add User"):
        add_user(name)
        st.success(f'✅ User "{name}" Added!')
    
    st.subheader("📋 Registered Users")
    users = display_users()
    for user in users:
        st.write(f"🆔 {user[0]} | 👤 {user[1]}")

# ✅ 📙 Borrow/Return Books
elif option == "📙 Borrow/Return Books":
    st.subheader("📙 Borrow or Return a Book")
    user_id = st.number_input("🆔 Enter User ID", min_value=1)
    book_id = st.number_input("📖 Enter Book ID", min_value=1)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📙 Borrow Book"):
            borrow_book(user_id, book_id)
            st.success("✅ Book Borrowed Successfully!")

    with col2:
        if st.button("📗 Return Book"):
            return_book(user_id, book_id)
            st.success("✅ Book Returned Successfully!")

    st.subheader("📋 Borrowed Books")
    borrowed_books = display_borrowed_books()
    for book in borrowed_books:
        st.write(f"👤 User {book[0]} borrowed 📖 Book {book[1]}")

st.sidebar.markdown("---")
st.sidebar.info("📌 Developed by **Areeba** 🚀")
