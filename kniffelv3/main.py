from datenbank import init_db
from menus import main_menu
from ascii_art import yahtzee

if __name__ == "__main__":
    init_db()
    print(yahtzee)

    main_menu()
