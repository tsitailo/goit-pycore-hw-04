"""
Головний модуль програми з основним циклом обробки команд.
"""

from assistant_bot.parser import parse_input
from assistant_bot.contacts import ContactBook
from assistant_bot.handlers import add_contact, change_contact, show_phone, show_all


def main():
    """
    Головна функція, яка управляє циклом обробки команд.
    """
    contact_book = ContactBook()
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, contact_book))

        elif command == "change":
            print(change_contact(args, contact_book))

        elif command == "phone":
            print(show_phone(args, contact_book))

        elif command == "all":
            print(show_all(contact_book))

        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()