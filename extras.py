from os import get_terminal_size
from errors import NoTerminalFound

def get_terminal_columns() -> int:
    """
    Returns the total columns in the terminal.
    Used for centering texts.
    """
    try:
        #Gets the columns attribute of terminal size from the os module.
        return get_terminal_size().columns
    except OSError:
        raise NoTerminalFound("Please run the script in a terminal") #An error in case the script isn't running in a terminal