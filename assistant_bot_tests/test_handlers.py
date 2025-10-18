"""
Тести для модуля handlers.
"""

import pytest
from assistant_bot.contacts import ContactBook
from assistant_bot.handlers import (
    add_contact,
    change_contact,
    show_phone,
    show_all
)


class TestAddContact:
    """Тести для функції add_contact."""

    @pytest.fixture
    def contact_book(self):
        """Фікстура для створення нової книги контактів."""
        return ContactBook()

    def test_add_contact_success(self, contact_book):
        """Тест успішного додавання контакту."""
        result = add_contact(["John", "1234567890"], contact_book)
        assert result == "Contact added."
        assert contact_book.get_phone("John") == "1234567890"

    def test_add_contact_with_no_arguments(self, contact_book):
        """Тест додавання контакту без аргументів."""
        result = add_contact([], contact_book)
        assert result == "Error: Please provide name and phone number."

    def test_add_contact_with_one_argument(self, contact_book):
        """Тест додавання контакту з одним аргументом."""
        result = add_contact(["John"], contact_book)
        assert result == "Error: Please provide name and phone number."

    def test_add_contact_with_three_arguments(self, contact_book):
        """Тест додавання контакту з трьома аргументами."""
        result = add_contact(["John", "Doe", "1234567890"], contact_book)
        assert result == "Error: Please provide name and phone number."

    def test_add_duplicate_contact(self, contact_book):
        """Тест додавання дублікату контакту."""
        add_contact(["John", "1234567890"], contact_book)
        result = add_contact(["John", "9999999999"], contact_book)
        assert result == "Contact added."
        assert contact_book.get_phone("John") == "9999999999"

    def test_add_multiple_contacts(self, contact_book):
        """Тест додавання кількох контактів."""
        add_contact(["John", "1234567890"], contact_book)
        add_contact(["Alice", "0987654321"], contact_book)
        assert len(contact_book.get_all()) == 2


class TestChangeContact:
    """Тести для функції change_contact."""

    @pytest.fixture
    def contact_book(self):
        """Фікстура для створення книги контактів з одним контактом."""
        book = ContactBook()
        book.add("John", "1234567890")
        return book

    def test_change_existing_contact(self, contact_book):
        """Тест зміни існуючого контакту."""
        result = change_contact(["John", "9999999999"], contact_book)
        assert result == "Contact updated."
        assert contact_book.get_phone("John") == "9999999999"

    def test_change_non_existing_contact(self, contact_book):
        """Тест зміни неіснуючого контакту."""
        result = change_contact(["Alice", "9999999999"], contact_book)
        assert result == "Error: Contact 'Alice' not found."

    def test_change_contact_with_no_arguments(self, contact_book):
        """Тест зміни контакту без аргументів."""
        result = change_contact([], contact_book)
        assert result == "Error: Please provide name and new phone number."

    def test_change_contact_with_one_argument(self, contact_book):
        """Тест зміни контакту з одним аргументом."""
        result = change_contact(["John"], contact_book)
        assert result == "Error: Please provide name and new phone number."

    def test_change_contact_with_three_arguments(self, contact_book):
        """Тест зміни контакту з трьома аргументами."""
        result = change_contact(["John", "Doe", "9999999999"], contact_book)
        assert result == "Error: Please provide name and new phone number."

    def test_change_contact_in_empty_book(self):
        """Тест зміни контакту в порожній книзі."""
        empty_book = ContactBook()
        result = change_contact(["John", "9999999999"], empty_book)
        assert result == "Error: Contact 'John' not found."


class TestShowPhone:
    """Тести для функції show_phone."""

    @pytest.fixture
    def contact_book(self):
        """Фікстура для створення книги контактів з кількома контактами."""
        book = ContactBook()
        book.add("John", "1234567890")
        book.add("Alice", "0987654321")
        return book

    def test_show_phone_existing_contact(self, contact_book):
        """Тест показу телефону існуючого контакту."""
        result = show_phone(["John"], contact_book)
        assert result == "1234567890"

    def test_show_phone_non_existing_contact(self, contact_book):
        """Тест показу телефону неіснуючого контакту."""
        result = show_phone(["Bob"], contact_book)
        assert result == "Error: Contact 'Bob' not found."

    def test_show_phone_with_no_arguments(self, contact_book):
        """Тест показу телефону без аргументів."""
        result = show_phone([], contact_book)
        assert result == "Error: Please provide contact name."

    def test_show_phone_with_two_arguments(self, contact_book):
        """Тест показу телефону з двома аргументами."""
        result = show_phone(["John", "Doe"], contact_book)
        assert result == "Error: Please provide contact name."

    def test_show_phone_from_empty_book(self):
        """Тест показу телефону з порожньої книги."""
        empty_book = ContactBook()
        result = show_phone(["John"], empty_book)
        assert result == "Error: Contact 'John' not found."

    def test_show_phone_case_sensitive(self, contact_book):
        """Тест що пошук телефону чутливий до регістру."""
        result = show_phone(["john"], contact_book)
        assert result == "Error: Contact 'john' not found."


class TestShowAll:
    """Тести для функції show_all."""

    @pytest.fixture
    def contact_book(self):
        """Фікстура для створення книги контактів з кількома контактами."""
        book = ContactBook()
        book.add("John", "1234567890")
        book.add("Alice", "0987654321")
        book.add("Bob", "5555555555")
        return book

    def test_show_all_with_contacts(self, contact_book):
        """Тест показу всіх контактів."""
        result = show_all(contact_book)
        assert "John: 1234567890" in result
        assert "Alice: 0987654321" in result
        assert "Bob: 5555555555" in result

    def test_show_all_empty_book(self):
        """Тест показу всіх контактів з порожньої книги."""
        empty_book = ContactBook()
        result = show_all(empty_book)
        assert result == "No contacts saved."

    def test_show_all_format(self, contact_book):
        """Тест формату виводу всіх контактів."""
        result = show_all(contact_book)
        lines = result.split("\n")
        assert len(lines) == 3
        for line in lines:
            assert ": " in line

    def test_show_all_single_contact(self):
        """Тест показу одного контакту."""
        book = ContactBook()
        book.add("John", "1234567890")
        result = show_all(book)
        assert result == "John: 1234567890"

    def test_show_all_after_adding_contact(self):
        """Тест показу всіх контактів після додавання."""
        book = ContactBook()
        assert show_all(book) == "No contacts saved."
        book.add("John", "1234567890")
        assert show_all(book) == "John: 1234567890"