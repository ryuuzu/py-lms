def loadbookstocks() -> dict:
    """Returns the books stocks details as dict.

    Book details format:
    bookid,bookname,author,publisher,pub_date,totalqnty,remaining,price(per 10 days)

    Return:
    bookdb - dict containing bookid as key and other details as value.
    """

    # This will be the Python dictionary containing all the book details with their id as its key.
    bookdb = {}
    # Opening the book stocks file inside a context manager
    with open("./data/bookstocks.txt", "r") as bookstocks:
        # Reading all the lines from the file
        books_detail = bookstocks.readlines()
    # Iterating through the lines one by one.
    for book_details in books_detail:
        # Splitting and assigning them to proper variables
        bookid, bookname, author, publisher, pub_date, total, remaining, price = book_details.split(
            ",")
        # Adding the details to our dictionary with book id as key and other details as value.
        bookdb[bookid] = {"name": bookname,
                          "author": author,
                          "publisher": publisher,
                          "pub_date": pub_date,
                          "total": int(total),
                          "remaining": int(remaining),
                          "price": float(price)}
    # Returns the main dict after adding all the book details.
    return bookdb


def savebookstocks(bookdb: dict) -> bool:
    """Returns True when saving is complete.

    Book details format:
    bookid,bookname,author,publisher,pub_date,totalqnty,remaining,price(per 10 days)

    Keyword Arguments:
    bookdb - dict containing bookid as key and other details as value.

    Return:
    True/False - bool depending on the success or failure.
    """

    # Initializing a string that will be written on the bookstocks file.
    stringToWrite = ""
    # Iterating through all the items in the dict.
    for bookid, book_details in bookdb.items():
        # Adding the bookid as the starting value
        stringToWrite += bookid + ","
        # Converting all the values inside dict to string (some values are in int and float).
        dict_values_in_string = [str(x) for x in book_details.values()]
        # Joining all the elements with the join function.
        stringToWrite += ",".join(dict_values_in_string)
        # Adding a line break at the end.
        stringToWrite += "\n"
    # Attempt to write the data into the bookstocks.txt file
    try:
        with open("./data/bookstocks.txt", "w") as bookstocks:
            bookstocks.write(stringToWrite)
        # Returns True when everything went smooth
        return True
    except IOError:
        # Returns False in case of an IOError.
        return False


if __name__ == "__main__":
    books = loadbookstocks()
    print(books)
    books['1']['name'] = "newname"
    savebookstocks(books)
