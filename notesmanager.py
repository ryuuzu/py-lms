import os


def loadnotes(noteid: str) -> list[str]:
    """Returns the notes about a person.

    Notes format:
    name,bookname,borroweddate,returndate,cost -> on borrow
    name,returneddate,latereturn,totalcost(incase of fine) -> on return

    Keyword Arguments:
    notesid - str - id for uniquely identifying the notes.

    Return:
    notes - str - notes inside the file.
    """
    # A try catch block for errors.
    try:
        # Opening the file in a context manager
        with open(f"./data/notes/{noteid}.txt", "r") as usernotes:
            notes = usernotes.readlines()  # Loading the file with lines
        notess = [note.strip("\n") for note in notes]
        return notess  # Returning the lines list.
    except IOError:
        return None  # Returns None in case of IOError


def addtonotes(noteid: str, note_to_add: str) -> bool:
    """Returns True when addition is complete.

    This is to be done when the book is returned back.

    Keyword Arguments:
    noteid - str - id for uniquely identifying the notes.
    note_to_add - str - notes to add to the existing one.

    Return:
    True/False - bool - depending on the success or failure.
    """
    # A try block to catch any errors in case there is one.
    try:
        # Opening the file in a context manager
        with open(f"./data/notes/{noteid}.txt", "a") as usernotes:
            # Writing the notes to the end of the file.
            usernotes.write(note_to_add)
        return True  # Returns True after everything goes properly
    except IOError:
        return False  # Returns False in case of IOError.


def searchnotes(keyword: str, checkReturned) -> list:
    """Returns a list of names of files that match the keyword form the notes directory.

    Keyword Arguments:
    keyword - str - keyword to search for in the notes directory.

    Return:
    search_results - list - list of all the file names that match the keyword.
    """
    # Initiating a list to contain the search results.
    search_results = []
    # Looping through all files/folders in notes directory.
    for filename in os.listdir("./data/notes/"):
        # A check if the path is a file.
        if os.path.isfile(f"./data/notes/{filename}"):
            # A check if the book has already been returned.
            if checkReturned:
                print("Checking")
                with open(f"./data/notes/{filename}") as note:
                    lines = note.readlines()
                if lines[-1].startswith("RETURN:"):
                    print("Breaking")
                    continue
            # A check if the file is txt and has keyword in it.
            if filename.endswith(".txt") and keyword in filename:
                # Adding the filename to the list
                print("Added one")
                search_results.append(filename.strip('.txt'))
    # Retunrning the search results.
    print(search_results)
    return search_results


def savenotes(noteid: str, notes: str) -> bool:
    """Returns True when saving is complete.

    This is to be done when the book is borrowed. This also creates the file in case it doesn't exist or overwrites existing one. So, use this carefully.

    Keyword Arguments:
    noteid - str - id for uniquely identifying the notes.
    notes - str - notes to add to the new file one.

    Return:
    True/False - bool - depending on the success or failure.
    """
    # A try block to catch any errors in case there is one
    try:
        # Opening the file in a context manager
        with open(f"./data/notes/{noteid}.txt", "w") as usernotes:
            usernotes.write(notes)  # Writing the notes into the file
        return True  # Returns True after everything went smoothly
    except IOError:
        return False  # Returns False in case of an error.
