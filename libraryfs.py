from book import Book


def loadbookstocks() -> dict:
    """
    Returns the books stocks details as list.

    Book details format:
    --------------------
    bookid,bookname,author,publisher,pub_date,totalqnty,remaining,price(per 10 days)

    Returns:
    --------
    bookdb : list
        contains book objects containing the book details.
    """

    # This will be the Python dictionary containing all the book details with their id as its key.
    bookdb = []
    # Opening the book stocks file inside a context manager
    with open("./data/bookstocks.txt", "r") as bookstocks:
        # Reading all the lines from the file
        books_detail = bookstocks.readlines()
    # Iterating through the lines one by one.
    for book_details in books_detail:
        # Removing the last line break escape sequence at the end
        book_details = book_details.strip("\n")
        # Splitting and assigning them to proper variables
        bookid, bookname, author, publisher, pub_date, total, remaining, price = book_details.split(
            ",")
        # Creating an object of the book.
        book_to_add = Book(bookid, bookname, author, publisher,
                           pub_date, int(total), float(price), int(remaining))
        # Adding the book to the list.
        bookdb.append(book_to_add)
    # Returns the main list after adding all the book details.
    return bookdb


def savebookstocks(bookdb: list) -> bool:
    """
    Returns True when saving is complete.

    Book details format:
    --------------------
    bookid,bookname,author,publisher,pub_date,totalqnty,remaining,price(per 10 days)

    Parameters:
    -----------
    bookdb : list
        contains book objects containing the book details.

    Returns:
    --------
    True/False : bool
        bool value depending on the success or failure.
    """

    # A list comprehension to get all the details for saving.
    stringToWrite = [book.getStockText() for book in bookdb]
    # Attempt to write the data into the bookstocks.txt file
    try:
        with open("./data/bookstocks.txt", "w") as bookstocks:
            bookstocks.writelines(stringToWrite)
        # Returns True when everything went smooth.
        return True
    except IOError:
        # Returns False in case of an IOError.
        return False


if __name__ == "__main__":
    books = loadbookstocks()
    print(books)
    books['1']['name'] = "newname"
    savebookstocks(books)
