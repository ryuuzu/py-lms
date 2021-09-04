from typing import final
from book import Book
import datetime


class Note:
    """
    A class to represent a note.

    Attributes:
    -----------
    name : str
        Name of the borrower
    books: list[Book]
        List of book objects that were borrowed.
    borroweddate: datetime.datetime
        Date when the book was borrowed.
    returndate : datetime.datetime
        Date when the book is to be returned.
    retuned : bool
        Boolean value representing if the book has been returned or not.
    returneddate : datetime.datetime
        Date when the book was returned.
    late_days : int
        Total days the book was delivered late for.
    final_cost : float
        Total cost of the transaction, with fine.
    cost : float
        Initial cost of the transaction, without fine.
    fine : float
        Total fine added.
    
    Methods:
    --------
    mark_returned():
        Mark the note as returned.
    calculate_cost():
        Calculate the total cost, after adding fine.
    get_borrow_notes():
        Returns the borrow notes to be written in data file.
    get_return_notes():
        Returns the borrow notes to be written in data file.
    """
    def __init__(self, name: str, books: list[Book], borroweddate: datetime.datetime, returned: bool = False, returneddate: datetime.datetime = None, late_days: int = 0, final_cost: float = 0.0):
        """
        Constructor for the Note object.
        
        Parameters:
        -----------
        name : str
            Name of the borrower
        books: list[Book]
            List of book objects that were borrowed.
        borroweddate: datetime.datetime
            Date when the book was borrowed.
        retuned : bool
            Boolean value representing if the book has been returned or not.
        returneddate : datetime.datetime
            Date when the book was returned.
        late_days : int
            Total days the book was delivered late for.
        final_cost : float
            Total cost of the transaction, with fine.
        """
        self.name = name
        self.books = books
        self.borroweddate = borroweddate
        self.returndate = borroweddate + datetime.timedelta(days=10)
        self.returned = returned
        self.returneddate = returneddate
        self.late_days = late_days
        self.final_cost = final_cost
        self.cost = sum([book.price for book in self.books])
        if final_cost != 0.0:
            self.fine = final_cost - self.cost

    def mark_returned(self):
        """
        Mark the note as returned.
        """
        self.returneddate = datetime.datetime.now()
        self.returned = True

    def calculate_cost(self):
        """
        Calculate the total cost, after adding fine.
        """
        if self.returned:
            costs = [book.price for book in self.books]
            total_cost = sum(costs)
            late_days = (self.returneddate - self.returndate).days
            if late_days > 0:
                fine: int = late_days * 10.0
            else:
                fine: int = 0
            self.fine = fine
            self.late_days = late_days
            self.final_cost = total_cost + fine
        else:
            print("Please make the books as returned first.")

    def get_borrow_notes(self):
        """
        Returns the borrow notes to be written in data file.
        """
        borrow_notes = ""
        for borrowed_book in self.books:
            borrow_notes += f"BORROW:{self.name},{borrowed_book.name},{self.borroweddate.isoformat()},{self.returndate.isoformat()},{borrowed_book.price}\n"
        return borrow_notes

    def get_return_notes(self):
        """
        Returns the borrow notes to be written in data file.

        Returns:
        --------
        
        """
        if self.returned:
            return f"RETURN:{self.name},{self.returneddate.isoformat()},{self.late_days},{self.final_cost}"
        else:
            return None
