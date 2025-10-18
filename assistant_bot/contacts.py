"""
Модуль для роботи зі словником контактів.
"""

class ContactBook:
    """
    Клас для зберігання та управління контактами.
    """

    def __init__(self):
        """Ініціалізація порожнього словника контактів."""
        self.contacts = {}

    def add(self, name, phone):
        """
        Додає контакт до книги.

        Args:
            name (str): Ім'я контакту
            phone (str): Номер телефону
        """
        self.contacts[name] = phone

    def change(self, name, phone):
        """
        Змінює номер телефону контакту.

        Args:
            name (str): Ім'я контакту
            phone (str): Новий номер телефону

        Returns:
            bool: True якщо контакт знайдено, False якщо ні
        """
        if name in self.contacts:
            self.contacts[name] = phone
            return True
        return False

    def get_phone(self, name):
        """
        Повертає номер телефону контакту.

        Args:
            name (str): Ім'я контакту

        Returns:
            str or None: Номер телефону або None якщо контакт не знайдено
        """
        return self.contacts.get(name)

    def get_all(self):
        """
        Повертає всі контакти.

        Returns:
            dict: Словник з усіма контактами
        """
        return self.contacts

    def is_empty(self):
        """
        Перевіряє чи порожня книга контактів.

        Returns:
            bool: True якщо порожня, False якщо ні
        """
        return len(self.contacts) == 0