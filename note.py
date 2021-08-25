from typing import final
from book import Book
import datetime


class Note:
    def __init__(self, name: str, books: list[Book], borroweddate: datetime.datetime, returned: bool = False, returneddate: datetime.datetime = None, late_days: int = 0, final_cost: float = 0.0):
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
        self.returneddate = datetime.datetime.now()
        self.returned = True

    def calculate_cost(self):
        if self.returned:
            costs = [book.price for book in self.books]
            total_cost = sum(costs)
            late_days = (self.returneddate - self.borroweddate).days
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
        borrow_notes = ""
        for borrowed_book in self.books:
            borrow_notes += f"BORROW:{self.name},{borrowed_book.name},{self.borroweddate.isoformat()},{self.returndate.isoformat()},{borrowed_book.price}\n"

        return borrow_notes

    def get_return_notes(self):
        if self.returned:
            return f"RETURN:{self.name},{self.returneddate.isoformat()},{self.late_days},{self.final_cost}"
        else:
            return None
