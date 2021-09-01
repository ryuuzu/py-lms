from errors import NoMoreStocks, StockFull


class Book:
    """
    A class to represent a book.

    Attributes:
    -----------
    lib_id : str
        Unique Library ID of the book
    name : str
        Name of the book
    author : str
        Author of the book
    publiser : str
        Publisher of the book
    pub_date : str
        Published Date of the book
    total : int
        Total Stock of the book
    price : int 
        Price for borrowing the book (per 10 days)
    remaining : int
        Remaining Stock of the book

    Methods:
    --------
    borrow():
        Borrows the book i.e. reduces one from the remaining stock value.
    returned():
        Marks the book as returned i.e. adds one to the remaining stock value.
    getAvailableText():
        Returns the remaining stock info of the book.
    getDisplayText():
        Returns all the information of the book.
    getStockText():
        Returns the book information for saving.
    """

    def __init__(self, lib_id: str, name: str, author: str, publisher: str, pub_date: str, total: int, price: float, remaining: int = None):
        """
        Constructor for the Book object.

        Parameters:
        -----------
        lib_id : str
            Unique Library ID of the book
        name : str
            Name of the book
        author : str
            Author of the book
        publiser : str
            Publisher of the book
        pub_date : str
            Published Date of the book
        total : int
            Total Stock of the book
        price : int 
            Price for borrowing the book (per 10 days)
        remaining : int
            Remaining Stock of the book
        """
        self.lib_id = lib_id
        self.name = name
        self.author = author
        self.publisher = publisher
        self.pub_date = pub_date
        self.total = total
        self.price = price
        if remaining is None:
            self.remaining = total
        else:
            self.remaining = remaining

    def borrow(self):
        """
        Borrows the book i.e. reduces one from the remaining stock value.
        """
        if self.remaining >= 1:
            self.remaining -= 1
        else:
            raise NoMoreStocks(self.remaining, "Stock Empty.")

    def returned(self):
        """
        Marks the book as returned i.e. adds one to the remaining stock value.
        """
        if self.remaining <= self.total:
            self.remaining += 1
        else:
            raise StockFull(self.remaining, "Stock Already Full.")

    def getAvailableText(self) -> str:
        """
        Returns the remaining stock info of the book.
        """
        return f"|{self.lib_id:<10}|{self.name:<50}|{self.author:<20}|{self.remaining:<10}|{self.price:<10}|"

    def getDisplayText(self) -> str:
        """
        Returns all the information of the book.
        """
        return f"|{self.lib_id:<7}|{self.name:<45}|{self.author:<20}|{self.publisher:<22}|{self.pub_date:<5}|{self.total:<5}|{self.price:<6}|"

    def getStockText(self) -> str:
        """
        Returns the book information for saving.
        """
        return f"{self.lib_id},{self.name},{self.author},{self.publisher},{self.pub_date},{self.total},{self.remaining},{self.price}\n"
