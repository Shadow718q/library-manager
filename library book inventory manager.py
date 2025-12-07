import json
import os

# File to store library data
DATA_FILE = "library_data.json"

class Book:
    def _init_(self, book_id, title, author, issued=False):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.issued = issued

    def to_dict(self):
        return {
            "book_id": self.book_id,
            "title": self.title,
            "author": self.author,
            "issued": self.issued
        }


class Library:
    def _init_(self):
        self.books = {}
        self.load_data()

    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as file:
                data = json.load(file)
                for book_data in data:
                    book = Book(**book_data)
                    self.books[book.book_id] = book

    def save_data(self):
        with open(DATA_FILE, "w") as file:
            json.dump([b.to_dict() for b in self.books.values()], file, indent=4)

    def add_book(self, book_id, title, author):
        if book_id in self.books:
            print("Book ID already exists!")
            return
        self.books[book_id] = Book(book_id, title, author)
        self.save_data()
        print("Book added successfully!")

    def search(self, keyword):
        results = [b for b in self.books.values()
                   if keyword.lower() in b.title.lower() or keyword.lower() in b.author.lower()]
        return results

    def issue_book(self, book_id):
        if book_id in self.books:
            if not self.books[book_id].issued:
                self.books[book_id].issued = True
                self.save_data()
                print("Book issued successfully!")
            else:
                print("Book is already issued!")
        else:
            print("Invalid Book ID!")

    def return_book(self, book_id):
        if book_id in self.books:
            if self.books[book_id].issued:
                self.books[book_id].issued = False
                self.save_data()
                print("Book returned successfully!")
            else:
                print("Book was not issued.")
        else:
            print("Invalid Book ID!")

    def report(self):
        total = len(self.books)
        issued = len([b for b in self.books.values() if b.issued])
        print(f"Total Books: {total}, Issued Books: {issued}")


def menu():
    library = Library()

    while True:
        print("\n====== Library Book Inventory Manager ======")
        print("1. Add Book")
        print("2. Search Book")
        print("3. Issue Book")
        print("4. Return Book")
        print("5. Report")
        print("6. Exit")
        choice = input("Enter choice: ")

        if choice == '1':
            id = input("Book ID: ")
            title = input("Title: ")
            author = input("Author: ")
            library.add_book(id, title, author)

        elif choice == '2':
            keyword = input("Enter title/author to search: ")
            results = library.search(keyword)
            print("\nSearch Results:")
            for b in results:
                status = "Issued" if b.issued else "Available"
                print(f"{b.book_id} - {b.title} by {b.author} ({status})")
            if not results:
                print("No books found!")

        elif choice == '3':
            id = input("Enter Book ID to issue: ")
            library.issue_book(id)

        elif choice == '4':
            id = input("Enter Book ID to return: ")
            library.return_book(id)

        elif choice == '5':
            library.report()

        elif choice == '6':
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid Choice! Try again.")

if _name_ == "_main_":
    menu()