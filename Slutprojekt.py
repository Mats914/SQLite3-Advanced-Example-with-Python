import sqlite3
from typing import List, Tuple, Optional


class LibraryDB:
    """
    A class to manage a simple library database using SQLite3.
    This includes operations for books and authors.
    """

    def __init__(self, db_name: str = "library.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        """Create the authors and books tables if they do not exist."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS authors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author_id INTEGER,
                FOREIGN KEY (author_id) REFERENCES authors(id)
            )
        ''')
        self.conn.commit()

    def add_author(self, name: str) -> int:
        """Insert a new author and return their ID."""
        self.cursor.execute("INSERT INTO authors (name) VALUES (?)", (name,))
        self.conn.commit()
        return self.cursor.lastrowid

    def add_book(self, title: str, author_id: int) -> int:
        """Insert a new book with a given author ID."""
        self.cursor.execute("INSERT INTO books (title, author_id) VALUES (?, ?)", (title, author_id))
        self.conn.commit()
        return self.cursor.lastrowid

    def get_all_books(self) -> List[Tuple]:
        """Retrieve all books with their authors."""
        self.cursor.execute('''
            SELECT books.id, books.title, authors.name
            FROM books
            JOIN authors ON books.author_id = authors.id
        ''')
        return self.cursor.fetchall()

    def update_book_title(self, book_id: int, new_title: str):
        """Update the title of a specific book."""
        self.cursor.execute("UPDATE books SET title = ? WHERE id = ?", (new_title, book_id))
        self.conn.commit()

    def delete_book(self, book_id: int):
        """Delete a book by its ID."""
        self.cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
        self.conn.commit()

    def close(self):
        """Close the database connection."""
        self.conn.close()


# Demo usage (You can remove this section if only library logic is needed)
if __name__ == "__main__":
    db = LibraryDB()

    # Add authors
    author_id_1 = db.add_author("George Orwell")
    author_id_2 = db.add_author("J.K. Rowling")

    # Add books
    db.add_book("1984", author_id_1)
    db.add_book("Animal Farm", author_id_1)
    db.add_book("Harry Potter and the Philosopher's Stone", author_id_2)

    # Display all books with authors
    books = db.get_all_books()
    print("\nBooks in Library:")
    for book in books:
        print(f"ID: {book[0]}, Title: '{book[1]}', Author: {book[2]}")

    # Update a book title
    db.update_book_title(1, "Nineteen Eighty-Four")

    # Delete a book
    db.delete_book(2)

    # Final list after changes
    print("\nUpdated Books List:")
    for book in db.get_all_books():
        print(f"ID: {book[0]}, Title: '{book[1]}', Author: {book[2]}")

    # Close the database
    db.close()
