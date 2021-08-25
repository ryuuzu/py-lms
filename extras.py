from os import get_terminal_size
from errors import NoTerminalFound

def get_terminal_columns():
    try:
        return get_terminal_size().columns
    except OSError:
        raise NoTerminalFound("Please run the script in a terminal")