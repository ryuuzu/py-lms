from datetime import datetime
from extras import get_terminal_columns


def get_login_menu():
    """
    Displays the login menu and doesn't let the user pass unless valid credentials are used.
    """
    # Printing a line break
    print("\n")
    columns = get_terminal_columns()  # Getting the coloumns of the terminal
    # A welcome message to print in the center.
    print("Welcome to Utsav's Library Management System.".center(columns))
    print("Please enter your login credentials:")  # Login Creds input.
    # Loading the file containing all the passwords.
    with open("./data/passwords.txt", "r") as pw_file:
        pws = pw_file.read().split("|")  # Splitting the passwords.
    while True:
        # Asking the user to input username and password.
        username = input("Username: ")
        password = input("Password: ")

        # Looping through all the usernames and passwords saved.
        for pass_line in pws:
            # Splitting the string to username and password.
            user, pw = pass_line.split(",")
            if user == username:  # A check if the username matches.
                if password == pw:  # A check if the password matched.
                    # Printing login success message
                    print("Login successful.")
                    # Returning the username that was used for login.
                    return username
                else:
                    # Error message if the password was wrong.
                    print("ERROR! Invalid Password.")
                    break
            # A check if the object was last in the list.
            elif pws.index(pass_line) == (len(pws) - 1):
                print("ERROR! User Not Found.")


def get_main_menu():
    """
    Displays the main menu with the options.
    This doesn't let the user pass unless valid option is used"""
    # Text to diplay in the main menu.
    main_menu_text = """
Options:

1: List the books available to borrow.
2: Add a borrow record.
3: Add a return record.
4: Add a book to the database.
5: Remove a book from the database.
6: Print a note.
7: Display all the books in the database.
8: Save the book stocks manually.
9 or exit: To exit the management system.
"""
    # Printing the text.
    print(main_menu_text)
    # A list of all valid options
    valid_options_list = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "exit"]
    # A infinite loop for getting correct input
    while True:
        # Asking the user to enter an option
        option = input("Enter an option to start the task: ").lower()
        if option in valid_options_list:  # A check if the input is valid
            return option  # Returning the user's input
        else:
            # An error message in case the input isn't valid
            print("ERROR! Invalid Option.")
            continue

def get_book_details_input():
    """
    Takes input from the user for book details.
    Has its own checks for proper datatype usage.
    """
    # Taking user input
    bookname = input("Enter the book's name: ")
    author = input("Enter the book's author name: ")
    publisher = input("Enter the book's publisher name: ")
    # A loop to get proper input from the user.
    while True:
        pub_date = input("Enter the book's published date (YYYY): ")
        try:
            # A check for valid date. This won't store value since I want it as a string.
            datetime.strptime(pub_date, "%Y")
            break  # Breaks if the date is in proper format
        except ValueError:
            # Loops around if it is wrong.
            print("ERROR! Please use proper format (YYYY-MM-DD) and enter valid values.")
            continue
    # A loop to get proper input from the user.
    while True:
        total_str = input("Enter the book's total stock: ")
        try:
            total = int(total_str)
            break  # Breaks after successfully parsing the string to float.
        except ValueError:
            # Loops around if it is wrong.
            print("ERROR! Please use proper integer value.")
            continue
    # A loop to get proper input from the user.
    while True:
        price_str = input(
            "Set the price for borrowing the book (per 10 days): ")
        try:
            price = float(price_str)
            break  # Breaks after successfully parsing the string to float.
        except ValueError:
            # Loops around if it is wrong.
            print("ERROR! Please use proper float/integer value.")
            continue

    return bookname, author, publisher, pub_date, total, price
