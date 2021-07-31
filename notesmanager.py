def loadnotes(noteid: str) -> str:
    """Returns the notes about a person.

    Notes format:
    name,bookname,borroweddate,returndate,totalcost -> on borrow
    name,bookname,returneddate,latereturn,totalcost(incase of fine) -> on return

    Keyword Arguments:
    notesid - str - id for uniquely identifying the notes.

    Return:
    notes - str - notes inside the file.
    """
    with open(f"./data/notes/{noteid}.txt", "r") as usernotes:
        notes = usernotes.read()
    return notes


def addtonotes(noteid: str, note_to_add: str) -> bool:
    """Returns True when addition is complete.
    
    This is to be done when the book is returned back.
    
    Keyword Arguments:
    noteid - str - id for uniquely identifying the notes.
    note_to_add - str - notes to add to the existing one.

    Return:
    True/False - bool - depending on the success or failure.
    """
    try:
        with open(f"./data/notes/{noteid}.txt", "a") as usernotes:
            usernotes.write(note_to_add)
        return True
    except IOError:
        return False


def savenotes(noteid: str, notes: str) -> bool:
    """Returns True when saving is complete.
    
    This is to be done when the book is borrowed. This also creates the file in case it doesn't exist or overwrites existing one. So, use this carefully.
    
    Keyword Arguments:
    noteid - str - id for uniquely identifying the notes.
    notes - str - notes to add to the new file one.

    Return:
    True/False - bool - depending on the success or failure.
    """
    try:
        with open(f"./data/notes/{noteid}.txt", "w") as usernotes:
            usernotes.write(notes)
        return True
    except IOError:
        return False
