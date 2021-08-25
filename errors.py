class BookError(Exception):
    pass

class NoMoreStocks(BookError):
    pass

class StockFull(BookError):
    pass

class NoTerminalFound(Exception):
    pass

class FileDoesNotExist(Exception):
    pass