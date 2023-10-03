import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('library.db')
cursor = conn.cursor()

# Create the Books table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Books (
        BookID TEXT PRIMARY KEY,
        Title TEXT,
        Author TEXT,
        ISBN TEXT,
        Status TEXT
    )
''')

# Create the Users table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        UserID TEXT PRIMARY KEY,
        Name TEXT,
        Email TEXT
    )
''')

# Create the Reservations table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Reservations (
        ReservationID TEXT PRIMARY KEY,
        BookID TEXT,
        UserID TEXT,
        ReservationDate TEXT,
        FOREIGN KEY (BookID) REFERENCES Books (BookID),
        FOREIGN KEY (UserID) REFERENCES Users (UserID)
    )
''')

# Add a new book to the Books table
def add_book():
    book_id = input("Enter BookID: ")
    title = input("Enter Title: ")
    author = input("Enter Author: ")
    isbn = input("Enter ISBN: ")
    status = "Available"

    cursor.execute('''
        INSERT INTO Books (BookID, Title, Author, ISBN, Status)
        VALUES (?, ?, ?, ?, ?)
    ''', (book_id, title, author, isbn, status))

    conn.commit()
    print("Book added successfully.")

# Find book details based on BookID
def find_book_by_id(book_id):
    cursor.execute('''
        SELECT Books.Title, Books.Author, Books.ISBN, Books.Status, Users.Name, Users.Email
        FROM Books
        LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
        LEFT JOIN Users ON Reservations.UserID = Users.UserID
        WHERE Books.BookID = ?
    ''', (book_id,))

    book_info = cursor.fetchone()

    if book_info:
        print("Title:", book_info[0])
        print("Author:", book_info[1])
        print("ISBN:", book_info[2])
        print("Status:", book_info[3])
        if book_info[4]:
            print("Reserved by", book_info[4])
            print("Contact Email:", book_info[5])
        else:
            print("Not reserved.")
    else:
        print("Book not found.")

# Find book reservation status based on input text
def find_reservation_status(text):
    if text.startswith("LB"):
        book_id = text
        find_book_by_id(book_id)
    elif text.startswith("LU"):
        user_id = text
        find_books_by_user(user_id)
    elif text.startswith("LR"):
        reservation_id = text
        find_reservation_by_id(reservation_id)
    else:
        title = text
        find_books_by_title(title)

# Find books reserved by a user based on UserID
def find_books_by_user(user_id):
    cursor.execute('''
        SELECT Books.BookID, Books.Title, Books.Status
        FROM Books
        INNER JOIN Reservations ON Books.BookID = Reservations.BookID
        WHERE Reservations.UserID = ?
    ''', (user_id,))

    books = cursor.fetchall()

    if books:
        for book in books:
            print("BookID:", book[0])
            print("Title:", book[1])
            print("Status:", book[2])
    else:
        print("No books reserved by this user.")

# Find reservation details based on ReservationID
def find_reservation_by_id(reservation_id):
    cursor.execute('''
        SELECT ReservationDate, BookID, UserID
        FROM Reservations
        WHERE ReservationID = ?
    ''', (reservation_id,))

    reservation = cursor.fetchone()

    if reservation:
        print("ReservationID:", reservation_id)
        print("ReservationDate:", reservation[0])
        print("BookID:", reservation[1])
        print("UserID:", reservation[2])
    else:
        print("Reservation not found.")

# Find all books in the database
def find_all_books():
    cursor.execute('''
        SELECT Books.BookID, Books.Title, Books.Author, Books.ISBN, Books.Status, Users.Name, Users.Email
        FROM Books
        LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
        LEFT JOIN Users ON Reservations.UserID = Users.UserID
    ''')

    books = cursor.fetchall()

    if books:
        for book in books:
            print("BookID:", book[0])
            print("Title:", book[1])
            print("Author:", book[2])
            print("ISBN:", book[3])
            print("Status:", book[4])
            if book[5]:
                print("Reserved by", book[5])
                print("Contact Email:", book[6])
            else:
                print("Not reserved.")
    else:
        print("No books found in the database.")

# Modify book details based on BookID
def modify_book(book_id, new_status):
    cursor.execute('''
        UPDATE Books
        SET Status = ?
        WHERE BookID = ?
    ''', (new_status, book_id))

    conn.commit()
    print("Book status updated.")

# Delete a book based on BookID
def delete_book(book_id):
    cursor.execute('''
        DELETE FROM Books
        WHERE BookID = ?
    ''', (book_id,))
    cursor.execute('''
        DELETE FROM Reservations
        WHERE BookID = ?
    ''', (book_id,))

    conn.commit()
    print("Book deleted.")

# Main program loop
while True:
    print("\nLibrary Management System")
    print("1. Add a new book")
    print("2. Find book details by BookID")
    print("3. Find reservation status by BookID, Title, UserID, or ReservationID")
    print("4. Find all books in the database")
    print("5. Modify book details by BookID")
    print("6. Delete a book by BookID")
    print("7. Exit")

    choice = input("Select an option (1/2/3/4/5/6/7): ")

    if choice == '1':
        add_book()
    elif choice == '2':
        book_id = input("Enter BookID: ")
        find_book_by_id(book_id)
    elif choice == '3':
        text = input("Enter BookID, Title, UserID, or ReservationID: ")
        find_reservation_status(text)
    elif choice == '4':
        find_all_books()
    elif choice == '5':
        book_id = input("Enter BookID: ")
        new_status = input("Enter new Status: ")
        modify_book(book_id, new_status)
    elif choice == '6':
        book_id = input("Enter BookID: ")
        delete_book(book_id)
    elif choice == '7':
        print("Exiting the program.")
        break
    else:
        print("Invalid choice. Please select a valid option (1/2/3/4/5/6/7).")

# Close the database connection
conn.close()
