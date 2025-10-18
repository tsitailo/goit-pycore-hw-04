"""
Модуль з функціями-обробниками команд.
"""

from assistant_bot.contacts import ContactBook


def add_contact(args, contact_book):
    """
    Додає новий контакт до книги контактів.

    Args:
        args (list): Список аргументів [ім'я, телефон]
        contact_book (ContactBook): Об'єкт книги контактів

    Returns:
        str: Повідомлення про результат операції
    """
    if len(args) != 2:
        return "Error: Please provide name and phone number."

    name, phone = args
    contact_book.add(name, phone)
    return "Contact added."


def change_contact(args, contact_book):
    """
    Змінює номер телефону для існуючого контакту.

    Args:
        args (list): Список аргументів [ім'я, новий_телефон]
        contact_book (ContactBook): Об'єкт книги контактів

    Returns:
        str: Повідомлення про результат операції
    """
    if len(args) != 2:
        return "Error: Please provide name and new phone number."

    name, phone = args

    if contact_book.change(name, phone):
        return "Contact updated."
    else:
        return f"Error: Contact '{name}' not found."


def show_phone(args, contact_book):
    """
    Виводить номер телефону для зазначеного контакту.

    Args:
        args (list): Список аргументів [ім'я]
        contact_book (ContactBook): Об'єкт книги контактів

    Returns:
        str: Номер телефону або повідомлення про помилку
    """
    if len(args) != 1:
        return "Error: Please provide contact name."

    name = args[0]
    phone = contact_book.get_phone(name)

    if phone:
        return phone
    else:
        return f"Error: Contact '{name}' not found."


def show_all(contact_book):
    """
    Повертає всі збережені контакти з номерами телефонів.

    Args:
        contact_book (ContactBook): Об'єкт книги контактів

    Returns:
        str: Відформатований список контактів
    """
    if contact_book.is_empty():
        return "No contacts saved."

    result = []
    for name, phone in contact_book.get_all().items():
        result.append(f"{name}: {phone}")

    return "\n".join(result)