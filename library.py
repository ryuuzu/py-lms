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
    """
    A class to represent the Library.

    Attributes:
    -----------
    name : str
        Name of the Library.
    user : str
        User who logged into the library system.
    bookdb :list[Book]
        A list of Book objects that are in the library.

    Methods:
    --------
    add_book():
        Add a book to the Library's Database.
    remove_book():
        Remove a book from the Library's Database.
    available_books():
        List out the books that are available for borrow.
    show_all_books():
        List out all the books in the Library's Database.
    borrow_book():
        Creates a borrow record and updates Library's Database.
    return_book():
        Creates a return record and updates Library's Database.
    get_noteid(checkReturned=True):
        Returns the note ID based on user's input and choice.
    create_notes(noteid):
        Returns a Note object based on the notes file.
    get_note_text(notes):
        Returns formatted text to write in text file.
    find_book_by_id(bookid):
        Returns a Book object with lib_id attribute same as the bookid.
    find_book(bookname):
        Returns a Book object with name attribute same as the bookname.
    find_similar_book(bookname):
        Returns a Book object with name attribute similar to the bookname.
    check_duplicates(bookid):
        Returns a Book object with lib_id attribute same as the bookid.
    print_notes(notes = None):
        Prints the transaction with proper formatting.
    savebookdb():
        Saves the Library's Database to file.
    """

    def __init__(self, name: str, user: str):
        """
        Constructor for the Library object.

        Parameters:
        -----------
        name : str
            Name of the Library
        user : str
            User who logged into the Library system.
        """
        self.name = name
        self.user = user
        self.bookdb: list[Book] = loadbookstocks()

    def add_book(self):
        """
        Add a book to the Library's Database.
        """
        # Calling the method to get input
        bookname, author, publisher, pub_date, total, price = get_book_details_input()
        # Loop for getting proepr input
        while True:
            # asking the user for bookid of the book
            bookid = input("Enter the book's unique Library ID: ")
            # Checkign if there is any book with same id.
            book_dupli = self.check_duplicates(bookid)
            if (book_dupli is None):
                break
            else:
                # Showing a error message with book name
                print(
                    f"The book titled {book_dupli.name} already has this ID.\n Please use other one.")
                continue
        # Creating a book object
        new_book = Book(bookid, bookname, author,
                        publisher, pub_date, total, price)
        # Adding the book to the database
        self.bookdb.append(new_book)
        # Printing the output
        print(
            f"The book titled {new_book.name} has been added to the database.")

    def remove_book(self):
        """
        Remove a book from the Library's Database.
        """
        # Loop for getting proper input.
        while True:
            # ASking the user for input
            bookname = input("Enter the book name (or exit to exit.): ")
            # Finding the book
            book = self.find_book(bookname)
            if book is not None:
                break  # Proceeds if the book was found
            elif book == "exit":
                return  # Proceeds if user entered "exit"
            else:
                # Proceeds otherwise
                matching_book = self.find_similar_book()
                # Finding similar books for the bookname
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
        self.bookdb.remove(book)  # Removing the book from the database
        # Printing proper output
        print(
            f"The book titled {book.name} by {book.author} has been removed from the database.")

    def available_books(self):
        """
        List out the books that are available for borrow.
        """
        columns = get_terminal_columns()  # Getting terminal columns size

        # Title for the display
        title = "Available books to borrow in the Library"
        print(title.center(columns))
        # Heading for the diplsay
        heading = f"|{'Book ID':<10}|{'Book Name':<50}|{'Author':<20}|{'Remaining':<10}|{'Price':<10}|"
        print_center(
            f"{''.join(['-' for x in range(len(heading))])}")
        print_center(heading)
        # Iterating through all the books in database.
        for book in self.bookdb:
            # Checking if the book is avaiable with proper stock.
            if book.remaining > 0:
                print_center(book.getAvailableText())
        print_center(
            f"{''.join(['-' for x in range(len(heading))])}")

    def show_all_books(self):
        """
        List out all the books in the Library's Database.
        """
        columns = get_terminal_columns()  # Getting terminal columns

        # Title for the display.
        title = "Books in the Library"
        print(title.center(columns))
        # Heading for the display.
        heading = f"|{'Book ID':<7}|{'Book Name':<45}|{'Author':<20}|{'Publisher':<22}|{'Year':<5}|{'Total':<5}|{'Price':<6}|"
        print_center(
            f"{''.join(['-' for x in range(len(heading))])}")
        print_center(heading)
        # Iterating through all the books in database.
        for book in self.bookdb:
            # Getting the book display text with the help of method.
            print_center(book.getDisplayText())
        print_center(
            f"{''.join(['-' for x in range(len(heading))])}")

    def borrow_book(self):
        """
        Creates a borrow record and updates Library's Database.
        """
        # Asking the user for borrower's name.
        name = input("Enter the name of the borrower: ").lower().title()
        # Getting current datetime in timestamp as int.
        timestamp = int(datetime.now().timestamp())
        # Creating the noteid
        noteid = f"{name.lower().replace(' ', '-')}-{timestamp}"
        # Initialising the borrowing list
        total_borrowing_books = []
        # First loop for adding multiple books
        while True:
            # Second loop for checking repeated books
            while True:
                # Third loop for getting proper book name
                while True:
                    # Asking the user for book name
                    bookarg = input("Enter the book name or ID: ")
                    # Finding the book witht he method
                    book = self.find_book_by_id(bookarg)
                    if book is not None:
                        break
                    else:
                        # Finding the book witht he method again
                        book = self.find_book(bookarg)
                        # Breaking the loop if the book is not None
                        if book is not None:
                            break
                        else:
                            # Finding similar named books with the method.
                            matching_book = self.find_similar_book(bookarg)
                            # Printing a message if the matching book is also None.
                            if matching_book is None:
                                print("Please make sure the book name is correct.")
                            else:
                                # Asking the user for confirmation
                                option = input(
                                    f"Did you mean {matching_book.name}? (Y/N): ").upper()
                                if option == "Y":
                                    # Assigning book with the matching book value after confirmation
                                    book = matching_book
                                    # Breaking the loop
                                    break
                                else:
                                    # Printing a message asking correct input.
                                    print(
                                        "Please make sure the book name is correct.")
                # Checking if the book is already in the list.
                if book in total_borrowing_books:
                    # Printing a message if it is.
                    print(
                        "The book has already been added to borrow list. Please use a different one.")
                else:
                    # Breaking the loop
                    break
            try:
                # Marking the book as borrowed and replacing the old object in the list.
                index = self.bookdb.index(book)
                book.borrow()
                self.bookdb[index] = book
            except NoMoreStocks as e:
                # An error message in case there is no stock available.
                print(e.args[1], "The book isn't avaiable for borrowing.")
            else:
                # Adding the book to the list
                total_borrowing_books.append(book)
            option1 = input("Do you want to add more books? (Y/N): ").upper()
            if option1 == "Y":
                continue
            else:
                break
        notes = Note(name, total_borrowing_books, datetime.now())
        self.print_notes(notes)
        savenotes(noteid, self.get_note_text(notes), notes.get_borrow_notes())

    def return_book(self):
        """
        Creates a return record and updates Library's Database.
        """
        # Calling the method to get noteid.
        noteid = self.get_noteid()
        # Proceeding if the noteid is not None.
        if noteid is not None:
            # Calling the method to create Note object.
            notes = self.create_notes(noteid)
            # Calling the method to print the note.
            self.print_notes(notes)
            # Asking the user for confirmation
            option = input(
                "Please confirm that this is the correct transaction. (Y/N): ").upper()
            if option == "Y":
                # Proceeding if the correct note was selected.
                for book in notes.books:
                    try:
                        # Marking the book as returned and replacing the old object in the list.
                        index = self.bookdb.index(book)
                        book.returned()
                        self.bookdb[index] = book
                    except StockFull as e:
                        # An error message in case the stock is full.
                        print(
                            e.args[1], f"The book stocks for {book.name} is already full. Please check it physically.")
                # Marking the note as returned.
                notes.mark_returned()
                # Calculating the cost.
                notes.calculate_cost()
                # Printing the date
                self.print_notes(notes)
                # Adding the return notes to the file.
                addtonotes(noteid, self.get_note_text(
                    notes), notes.get_return_notes())
            else:
                # Aborting in case the user doesn't want to proceed.
                print("Aborting the process.")

    def get_noteid(self, checkReturned=True) -> str:
        """
        Returns the note ID based on user's input and choice.

        Parameters:
        -----------
        checkReturned : bool, optional
            Boolean value to skip returned record or not.

        Returns:
        --------
        noteid : str
            File name of the note.
        """
        # Asking the user for input
        name = input("Enter the name of the borrower: ")
        noteid = None  # Initialising the value of note id.
        # Calling th search notes function from the notesmanager module
        notes_list = searchnotes(
            f"{name.lower().replace(' ', '-')}", checkReturned)
        # Checking if the list is empty or not.
        if len(notes_list) == 0:
            # A message to end the process in case there are no notes
            print(
                f"No borrow notes were found for {name}. Please make sure that the name is spelled correctly.")
        # Checking if there is only one noteid
        elif len(notes_list) == 1:
            noteid = notes_list[0]
        else:
            # Printing all the notes found with cartain details.
            print(f"{'S.No.':<6}{'Name':<20}{'Books Borrowed':<15}Date")
            for index, notes in enumerate(notes_list):
                notes_lines = loadnotes(notes)
                # Calculating the total books with list comprehension
                total_books = sum(
                    [1 for note_line in notes_lines if note_line.startswith("BORROW:")])
                name, timestamp = notes.rsplit("-", 1)
                # Formatting the name properly.
                name = name.replace("-", " ").title()
                # Converting the timestamp to datetime object
                date = datetime.fromtimestamp(float(timestamp))
                print(
                    f"{index+1:<6}{name:<20}{total_books:<15}{date.strftime('%A, %B %d, %Y')}")
            while True:
                try:
                    print(f"Multiple Records found on {name}")
                    # Asking the user for input
                    option = int(input(
                        "Which transaction would you like to add return record for (Use S.No.)?: "))
                except ValueError:
                    # An error incase wrong datatype was used.
                    print("Please enter a proper value.")
                try:
                    # getting the noteid according to the index.
                    noteid = notes_list[option-1]
                    break
                except IndexError:
                    # AN error incase wrong index was used.
                    print("Please enter correct value from the S.No.")
        return noteid

    def create_notes(self, noteid) -> Note:
        """
        Returns a Note object based on the notes file.

        Paramters:
        ----------
        noteid : str
            File name of the note.

        Returns:
        --------
        note : Note
            Note object based on the notes textfile.
        """
        # Loading the notes from the noteid/filename.
        note_lines = loadnotes(noteid)
        # Some default values
        returned = False
        returneddate = None
        late_days = 0
        final_cost = 0.0
        books = []  # Books list of book object that was borrowed.
        for note_line in note_lines:
            if note_line.startswith("BORROW:"):
                # Getting borrow values from the line accordingly.
                note_line = note_line.strip("BORROW:")
                note_args = note_line.split(",")
                name = note_args[0]
                bookname = note_args[1]
                borroweddate = datetime.fromisoformat(note_args[2])
                book = self.find_book(bookname)
                books.append(book)
            elif note_line.startswith("RETURN:"):
                # Getting return values from the line accordingly
                note_line = note_line.strip("RETURN:")
                note_args = note_line.split(",")
                returned = True
                returneddate = datetime.fromisoformat(note_args[1])
                late_days = int(note_args[2])
                final_cost = float(note_args[3])
        # Creating note object based on the file values
        note = Note(name, books, borroweddate, returned,
                    returneddate, late_days, final_cost)
        return note  # Returns the note object created

    def get_note_text(self, notes: Note) -> str:
        """
        Returns formatted text to write in text file

        Parameters:
        -----------
        notes : Note
            Note object to write.

        Returns:
        --------
        note_text : str
            Formatted text.
        """
        columns = 120
        note_text = ""
        note_text += f"{self.name}\n".center(columns)
        note_text += f"Sender: {self.user}\n".rjust(70)
        note_text += f"{''.join(['-' for x in range(columns)])}\n"
        note_text += "Invoice\n"
        note_text += f"Receiver: {notes.name}\n"
        note_text += f"Date: {notes.borroweddate.strftime('%d %B, %Y')}\n"
        note_text += f"Return Due: {notes.returndate.strftime('%d %B, %Y')}\n"
        if notes.returned:
            note_text += f"Returned Date: {notes.returneddate.strftime('%d %B, %Y')}\n"
        header = f"|{'Book ID':<10} | {'Book Name':<50} | {'Author':<20} | {'Price':<10}|"
        note_text += f"{''.join(['-' for x in range(len(header))])}".center(columns)
        note_text += "\n"
        note_text += header.center(columns)
        note_text += "\n"
        for book in notes.books:
            note_text += f"|{book.lib_id:<10} | {book.name:<50} | {book.author:<20} | {book.price:<10}|".center(
                columns)
        note_text += "\n"
        if notes.returned:
            note_text += f"|{'':<10} | {'':<50} | {'Fine':<20} | {notes.fine:<10}|".center(
                columns)
            note_text += "\n"
            note_text += f"|{'':<10} | {'':<50} | {'Total':<20} | {notes.final_cost:<10}|".center(
                columns)
        else:
            note_text += f"|{'':<10} | {'':<50} | {'Initial Total':<20} | {notes.cost:<10}|".center(
                columns)
        note_text += "\n"
        note_text += f"{''.join(['-' for x in range(len(header))])}".center(columns)
        note_text += "\n"
        note_text += f"{''.join(['-' for x in range(columns)])}\n"
        note_text += "Kindly return the book before or at the due date.\n"
        note_text += "Note: You will be fined Rs.10 per day for late return.\n"
        return note_text

    def find_book_by_id(self, bookid) -> Book:
        """
        Returns a Book object with lib_id attribute same as the bookid.

        Parameters:
        -----------
        bookid : str
            ID of the book.

        Returns:
        book : Book or None
            Book with lib_id attribute same as the bookid.
        """
        # Iterating through all the books in the list.
        for book in self.bookdb:
            # Check for bookid
            if (bookid.lower() == book.lib_id.lower()):
                return book  # Returns book if bookid matches lib_id.
        return None  # Returns None if nothing was found in the end.

    def find_book(self, bookname) -> Book:
        """
        Returns a Book object with name attribute same as the bookname.

        Parameters:
        -----------
        bookname : str
            Name of the book.

        Returns:
        --------
        book : Book or None
            Book with name attribute same as the bookname.
        """
        # Iterating through all the books in the list.
        for book in self.bookdb:
            # Check for bookname
            if (bookname.lower() == book.name.lower()):
                return book  # Returns book if bookname matches name.
        return None  # Returns None if nothing was found in the end.

    def find_similar_book(self, bookname) -> Book:
        """
        Returns a Book object with name attribute similar to the bookname.

        Parameters:
        -----------
        bookname : str
            Name of the book.

        Returns:
        --------
        book : Book or None
            Book with name attribute similar to the bookname.
        """
        # List comprehension to get all book names in lowercase.
        book_names = [book.name.lower() for book in self.bookdb]
        # Getting closed match from the list.
        matches = get_close_matches(bookname, book_names)
        # CHeck for matches length
        if len(matches) > 0:
            return self.find_book(matches[0])  # Returns the first match
        else:
            return None  # Returns None if there are no matches

    def check_duplicates(self, bookid) -> Book:
        """
        Returns a Book object with lib_id attribute same as the bookid.

        Parameters:
        -----------
        bookid : str
            Library ID of the book.

        Returns:
        --------
        book : Book or None
            Book with lib_id attribute same as the bookid.

        """
        # Iterating through all the books in the list.
        for book in self.bookdb:
            # Check for bookid
            if (bookid == book.lib_id):
                return book  # Returns book is bookid matches lib_id
        return None  # Returns None if nothing was found in the end

    def print_notes(self, notes: Note = None):
        """
        Prints the transaction with proper formatting.

        Parameters:
        -----------
        note: Note, optional
            Note object to be printed.
        """
        # Checks if the notes is None
        if notes is None:
            # Gets notes from the user
            noteid = self.get_noteid(checkReturned=False)
            notes = self.create_notes(noteid)
        columns = get_terminal_columns()  # Getting terminal columns
        # A lot of printing with a lot of formatting.
        print(f"{self.name}".center(columns))
        print(f"Sender: {self.user}".rjust(columns))
        print(f"{''.join(['-' for x in range(columns)])}")
        print("Invoice")
        print(f"Receiver: {notes.name}")
        print(f"Date: {notes.borroweddate.strftime('%d %B, %Y')}")
        print(f"Return Due: {notes.returndate.strftime('%d %B, %Y')}")
        # Printing returned date as well if notes are returned
        if notes.returned:
            print(f"Returned Date: {notes.returneddate.strftime('%d %B, %Y')}")
        # Printing transaction table
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
        # Transaction table end
        # Some end notes printing
        print(f"{''.join(['-' for x in range(columns)])}")
        print("Kindly return the book before or at the due date.")
        print("Note: You will be fined Rs.10 per day for late return.")

    def savebookdb(self):
        """
        Saves the Library's Database to file.
        """
        # Calling the save function from libraryfs module
        savebookstocks(self.bookdb)


def print_center(to_print: str):
    """
    Prints the string in center.

    Parameters:
    -----------
    to_print : str
        String to be printed in the center.
    """
    # Getting the terminal columns
    columns = get_terminal_columns()
    # Printing the string with no line break in the end.
    # There is no line break here due to formatting errors.
    print(to_print.center(columns), end="")


# Program testing purposes.
if __name__ == "__main__":
    lib = Library("Islington Library", "Ryuu")
    lib.print_notes()
