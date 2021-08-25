from note import Note
from book import Book
from libraryfs import *
from notesmanager import *
from datetime import datetime
from difflib import get_close_matches
from extras import get_terminal_columns
from errors import NoMoreStocks, StockFull
from input_funcs import get_book_details_input


class Library:

    def __init__(self, name: str, user: str):
        self.name = name
        self.user = user
        self.bookdb: list[Book] = loadbookstocks()

    def add_book(self):
        bookname, author, publisher, pub_date, total, price = get_book_details_input()
        while True:
            bookid = input("Enter the book's unique Library ID: ")
            book_dupli = self.check_duplicates(bookid)
            if (book_dupli is None):
                break
            else:
                print(
                    f"The book titled {book_dupli.name} already has this ID.\n Please use other one.")
                continue
        new_book = Book(bookid, bookname, author,
                        publisher, pub_date, total, price)
        self.bookdb.append(new_book)
        print(
            f"The book titled {new_book.name} has been added to the database.")

    def remove_book(self):
        while True:
            bookname = input("Enter the book name: ")
            book = self.find_book(bookname)
            if book is not None:
                break
            else:
                matching_book = self.find_similar_book()
                if matching_book is None:
                    print("Please make sure the book name is correct.")
                else:
                    option = input(
                        f"Did you mean {matching_book.name}? (Y/N): ").upper()
                    if option == "Y":
                        book = matching_book
                        break
                    else:
                        print("Please make sure the book name is correct.")
        self.bookdb.remove(book)
        print(
            f"The book titled {book.name} by {book.author} has been removed from the database.")

    def available_books(self):
        columns = get_terminal_columns()

        title = "Available books to borrow in the Library"
        string_to_print = f"{title.center(columns)}"

        heading = f"{'Book ID':<10}|{'Book Name':<50}|{'Author':<20}|{'Remaining':<10}|{'Price'}\n"
        string_to_print += heading

        for book in self.bookdb:
            if book.remaining >= 1:
                string_to_print += book.getAvailableText()

        print(string_to_print)

    def show_all_books(self):
        columns = get_terminal_columns()

        title = "Available books to borrow in the Library"
        string_to_print = f"{title.center(columns)}"

        heading = f"{'Book ID':<10}|{'Book Name':<50}|{'Author':<20}|{'Remaining':<10}|{'Price'}\n"
        string_to_print += heading

        for book in self.bookdb:
            string_to_print += book.getAvailableText()

        print(string_to_print)

    def borrow_book(self):
        name = input("Enter the name of the borrower: ").lower().title()
        isotime = int(datetime.now().timestamp())
        noteid = f"{name.lower().replace(' ', '-')}-{isotime}"
        total_borrowing_books = []
        while True:
            while True:
                bookname = input("Enter the book name: ")
                book = self.find_book(bookname)
                if book is not None:
                    break
                else:
                    matching_book = self.find_similar_book(bookname)
                    if matching_book is None:
                        print("Please make sure the book name is correct.")
                    else:
                        option = input(
                            f"Did you mean {matching_book.name}? (Y/N): ").upper()
                        if option == "Y":
                            book = matching_book
                            break
                        else:
                            print("Please make sure the book name is correct.")
            try:
                index = self.bookdb.index(book)
                book.borrow()
                self.bookdb[index] = book
            except NoMoreStocks as e:
                print(e.args[1], "The book isn't avaiable for borrowing.")
            else:
                total_borrowing_books.append(book)
            option1 = input("Do you want to add more books? (Y/N): ").upper()
            if option1 == "Y":
                continue
            else:
                break
        notes = Note(name, total_borrowing_books, datetime.now())
        self.print_notes(notes)
        savenotes(noteid, notes.get_borrow_notes())

    def return_book(self):
        noteid = self.get_noteid()
        notes = self.create_notes(noteid)
        for book in notes.books:
            try:
                index = self.bookdb.index(book)
                book.returned()
                self.bookdb[index] = book
            except StockFull as e:
                print(
                    e.args[1], "The book stocks is already full. Please check it physically.")
        notes.mark_returned()
        notes.calculate_cost()
        self.print_notes(notes)
        addtonotes(noteid, notes.get_return_notes())

    def get_noteid(self, checkReturned = True):
        name = input("Enter the name of the borrower: ")
        noteid = None
        notes_list = searchnotes(
            f"{name.lower().replace(' ', '-')}", checkReturned)
        if len(notes_list) == 0:
            print(
                f"No notes were found for {name}. Please make sure that the name is spelled correctly.")
        elif len(notes_list) == 1:
            noteid = notes_list[0]
        else:
            print(f"{'S.No.':<6}{'Name':<20}Date")
            for index, notes in enumerate(notes_list):
                name, timestamp = notes.rsplit("-", 1)
                name = name.replace("-", " ").title()
                date = datetime.fromtimestamp(float(timestamp))
                print(f"{index+1:<6}{name:<20}{date.strftime('%A, %B %d, %Y')}")
            while True:
                try:
                    print(f"Multiple Records found on {name}")
                    option = int(input(
                        "Which transaction would you like to add return record for (Use S.No.)?: "))
                except ValueError:
                    print("Please enter correct value.")
                try:
                    noteid = notes_list[option-1]
                    break
                except IndexError:
                    print("Please enter correct value.")
        return noteid

    def create_notes(self, noteid) -> Note:
        note_lines = loadnotes(noteid)
        # name,bookname,borroweddate,returndate,cost -> on borrow
        # name,returneddate,latereturn,totalcost(incase of fine) -> on return
        returned = False
        returneddate = None
        late_days = 0
        final_cost = 0.0
        books = []
        for note_line in note_lines:
            if note_line.startswith("BORROW:"):
                note_line = note_line.strip("BORROW:")
                note_args = note_line.split(",")
                name = note_args[0]
                bookname = note_args[1]
                borroweddate = datetime.fromisoformat(note_args[2])
                book = self.find_book(bookname)
                books.append(book)
            elif note_line.startswith("RETURN:"):
                note_line = note_line.strip("RETURN:")
                note_args = note_line.split(",")
                returned = True
                returneddate = datetime.fromisoformat(note_args[1])
                late_days = int(note_args[2])
                final_cost = float(note_args[3])
        note = Note(name, books, borroweddate, returned,
                    returneddate, late_days, final_cost)
        return note

    def find_book(self, bookname) -> Book:
        for book in self.bookdb:
            if (bookname.lower() == book.name.lower()):
                return book
        return None

    def find_similar_book(self, bookname) -> Book:
        book_names = [book.name.lower() for book in self.bookdb]
        matches = get_close_matches(bookname, book_names)
        if len(matches) > 0:
            return self.find_book(matches[0])
        else:
            return None

    def check_duplicates(self, bookid) -> Book:
        for book in self.bookdb:
            if (bookid == book.lib_id):
                return book
        return None

    def print_notes(self, notes: Note = None):
        if notes is None:
            noteid = self.get_noteid(checkReturned = False)
            notes = self.create_notes(noteid)
        columns = get_terminal_columns()
        print(f"{self.name}".center(columns))
        print(f"Sender: {self.user}".rjust(columns))
        print(f"{''.join(['-' for x in range(columns)])}")
        print("Invoice")
        print(f"Receiver: {notes.name}")
        print(f"Date: {notes.borroweddate.strftime('%d %B, %Y')}")
        print(f"Return Due: {notes.returndate.strftime('%d %B, %Y')}")
        if notes.returned:
            print(f"Returned Date: {notes.returneddate.strftime('%d %B, %Y')}")
        header = f"|{'Book ID':<10} | {'Book Name':<50} | {'Author':<20} | {'Price':<10}|"
        print_center(
            f"{''.join(['-' for x in range(len(header))])}")
        print_center(header)
        for book in notes.books:
            print_center(
                f"|{book.lib_id:<10} | {book.name:<50} | {book.author:<20} | {book.price:<10}|")
        if notes.returned:
            print_center(
                f"|{'':<10} | {'':<50} | {'Fine':<20} | {notes.fine:<10}|")
            print_center(
                f"|{'':<10} | {'':<50} | {'Total':<20} | {notes.final_cost:<10}|")
        else:
            print_center(
                f"|{'':<10} | {'':<50} | {'Initial Total':<20} | {notes.cost:<10}|")
        print(f"{''.join(['-' for x in range(len(header))])}".center(columns))
        print(f"{''.join(['-' for x in range(columns)])}")
        print("Kindly return the book before or at the due date.")
        print("Note: You will be fined Rs.10 per day for late return.")

    def savebookdb(self):
        savebookstocks(self.bookdb)


def print_center(to_print):
    columns = get_terminal_columns()
    print(to_print.center(columns), end="")


if __name__ == "__main__":
    lib = Library("Islington Library", "Ryuu")
    lib.print_notes()
