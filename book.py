from errors import NoMoreStocks, StockFull

class Book:
    """
    """
    def __init__(self, lib_id: str, name: str, author: str, publisher: str, pub_date: str, total: int, price: float, remaining:int=None):
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
        if self.remaining >= 1:
            self.remaining -= 1
        else:
            raise NoMoreStocks(self.remaining, "Stock Empty.")
    
    def returned(self):
        if self.remaining <= self.total:
            self.remaining += 1
        else:
            raise StockFull(self.remaining, "Stock Already Full.")

    def getAvailableText(self):
        return f"{self.lib_id:<10}|{self.name:<50}|{self.author:<20}|{self.remaining:<10}|{self.price}\n"

    def getDisplayText(self):
        pass

    def getStockText(self):
        return f"{self.lib_id},{self.name},{self.author},{self.publisher},{self.pub_date},{self.total},{self.remaining},{self.price}\n"
