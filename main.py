from library import Library
from input_funcs import get_login_menu, get_main_menu
from time import sleep


username = get_login_menu()
my_library = Library("Islington Library", username)
print(f"Hello, {username}! Welcome to the {my_library.name}'s Main Menu.")
while True:
    option = get_main_menu()
    if option == "1":
        my_library.available_books()
    elif option == "2":
        my_library.borrow_book()
    elif option == "3":
        my_library.return_book()
    elif option == "4":
        my_library.add_book()
    elif option == "5":
        my_library.remove_book()
    elif option == "6":
        my_library.print_notes()
    elif option == "7":
        my_library.show_all_books()
    elif option == "8":
        my_library.savebookdb()
        print("The database has been saved.")
    else:
        print("Saving the database...")
        my_library.savebookdb()
        print("Logging you out...")
        sleep(2)
        print("Logged out successfully. Thank you.")
        break
print("Exited successfully.")
