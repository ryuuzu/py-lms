import os


def loadnotes(noteid: str) -> list[str]:
    """
    Returns the notes about a person.

    Notes format:
    -------------
    name,bookname,borroweddate,returndate,cost -> on borrow
    name,returneddate,latereturn,totalcost(incase of fine) -> on return

    Parameters:
    -----------
    notesid : str
        id for uniquely identifying the notes.

    Returns:
    --------
    notes : str
        notes inside the file.
    """
    # A try catch block for errors.
    try:
        # Opening the file in a context manager
        with open(f"./data/notes/{noteid}.data", "r") as usernotes:
            notes = usernotes.readlines()  # Loading the file with lines
        notess = [note.strip("\n") for note in notes]
        return notess  # Returning the lines list.
    except IOError:
        return None  # Returns None in case of IOError


def addtonotes(noteid: str, note_file_text:str ,note_data_file: str) -> bool:
    """
    Returns True when addition is complete.

    This is to be done when the book is returned back.

    Parameters:
    -----------
    noteid : str
        id for uniquely identifying the notes.
    note_file_text : str
        notes to write for the text file.
    note_data_file : str
        notes to add to the existing data file.

    Returns:
    --------
    True/False : bool
        Boolean Value depending on the success or failure.
    """
    # A try block to catch any errors in case there is one.
    try:
        # Opening the file in a context manager
        with open(f"./data/notes/{noteid}.txt", "w") as usernotes:
            # Writing the notes to the end of the file.
            usernotes.write(note_file_text)
        with open(f"./data/notes/{noteid}.data", "a") as usernotesdata:
            # Writing the notes to the end of the file.
            usernotesdata.write(note_data_file)
        return True  # Returns True after everything goes properly
    except IOError:
        return False  # Returns False in case of IOError.


def searchnotes(keyword: str, checkReturned: bool) -> list:
    """
    Returns a list of names of files that match the keyword form the notes directory.

    Parameters:
    -----------
    keyword : str
        keyword to search for in the notes directory.
    checkReturned : bool
        to skip returned notes or not.

    Returns:
    --------
    search_results : list
        list of all the file names that match the keyword.
    """
    # Initiating a list to contain the search results.
    search_results = []
    # Looping through all files/folders in notes directory.
    for filename in os.listdir("./data/notes/"):
        # A check if the path is a file.
        if os.path.isfile(f"./data/notes/{filename}"):
            if filename.endswith(".data"):
                # A check if the book has already been returned.
                if checkReturned:
                    with open(f"./data/notes/{filename}") as note:
                        lines = note.readlines()
                    if lines[-1].startswith("RETURN:"):
                        continue
                # A check if the file is txt and has keyword in it.
                if keyword in filename:
                    # Adding the filename to the list
                    search_results.append(filename.strip('.data'))
    # Retunrning the search results.
    return search_results


def savenotes(noteid: str, note_file_text: str, note_data_file: str) -> bool:
    """
    Returns True when saving is complete.

    This is to be done when the book is borrowed. This also creates the file in case it doesn't exist or overwrites existing one. So, use this carefully.

    Parameters:
    -----------
    noteid : str
        id for uniquely identifying the notes.
    note_file_text : str
        notes to write for the text file.
    note_data_file : str
        notes to add to the new data file.

    Returns:
    --------
    True/False : bool
        Boolean Value depending on the success or failure.
    """
    # A try block to catch any errors in case there is one
    try:
        # Opening the file in a context manager
        with open(f"./data/notes/{noteid}.txt", "w") as usernotes:
            # Writing the notes to the end of the file.
            usernotes.write(note_file_text)
        with open(f"./data/notes/{noteid}.data", "w") as usernotesdata:
            # Writing the notes to the end of the file.
            usernotesdata.write(note_data_file)
        return True  # Returns True after everything went smoothly
    except IOError:
        return False  # Returns False in case of an error.
