"""
Тести для модуля contacts.
"""

import pytest
from assistant_bot.contacts import ContactBook


class TestContactBook:
    """Тести для класу ContactBook."""

    @pytest.fixture
    def contact_book(self):
        """Фікстура для створення нової книги контактів."""
        return ContactBook()

    @pytest.fixture
    def filled_contact_book(self):
        """Фікстура для створення заповненої книги контактів."""
        book = ContactBook()
        book.add("John", "1234567890")
        book.add("Alice", "0987654321")
        book.add("Bob", "5555555555")
        return book

    def test_init_empty_contact_book(self, contact_book):
        """Тест ініціалізації порожньої книги контактів."""
        assert contact_book.contacts == {}
        assert contact_book.is_empty() is True

    def test_add_single_contact(self, contact_book):
        """Тест додавання одного контакту."""
        contact_book.add("John", "1234567890")
        assert "John" in contact_book.contacts
        assert contact_book.contacts["John"] == "1234567890"
        assert contact_book.is_empty() is False

    def test_add_multiple_contacts(self, contact_book):
        """Тест додавання кількох контактів."""
        contact_book.add("John", "1234567890")
        contact_book.add("Alice", "0987654321")
        assert len(contact_book.contacts) == 2
        assert contact_book.contacts["John"] == "1234567890"
        assert contact_book.contacts["Alice"] == "0987654321"

    def test_add_duplicate_contact_overwrites(self, contact_book):
        """Тест перезапису контакту з однаковим ім'ям."""
        contact_book.add("John", "1234567890")
        contact_book.add("John", "9999999999")
        assert contact_book.contacts["John"] == "9999999999"
        assert len(contact_book.contacts) == 1

    def test_change_existing_contact(self, filled_contact_book):
        """Тест зміни існуючого контакту."""
        result = filled_contact_book.change("John", "1111111111")
        assert result is True
        assert filled_contact_book.contacts["John"] == "1111111111"

    def test_change_non_existing_contact(self, filled_contact_book):
        """Тест зміни неіснуючого контакту."""
        result = filled_contact_book.change("NonExistent", "1111111111")
        assert result is False
        assert "NonExistent" not in filled_contact_book.contacts

    def test_change_contact_in_empty_book(self, contact_book):
        """Тест зміни контакту в порожній книзі."""
        result = contact_book.change("John", "1234567890")
        assert result is False

    def test_get_phone_existing_contact(self, filled_contact_book):
        """Тест отримання телефону існуючого контакту."""
        phone = filled_contact_book.get_phone("John")
        assert phone == "1234567890"

    def test_get_phone_non_existing_contact(self, filled_contact_book):
        """Тест отримання телефону неіснуючого контакту."""
        phone = filled_contact_book.get_phone("NonExistent")
        assert phone is None

    def test_get_phone_from_empty_book(self, contact_book):
        """Тест отримання телефону з порожньої книги."""
        phone = contact_book.get_phone("John")
        assert phone is None

    def test_get_all_contacts(self, filled_contact_book):
        """Тест отримання всіх контактів."""
        all_contacts = filled_contact_book.get_all()
        assert len(all_contacts) == 3
        assert "John" in all_contacts
        assert "Alice" in all_contacts
        assert "Bob" in all_contacts

    def test_get_all_from_empty_book(self, contact_book):
        """Тест отримання всіх контактів з порожньої книги."""
        all_contacts = contact_book.get_all()
        assert all_contacts == {}

    def test_is_empty_on_empty_book(self, contact_book):
        """Тест перевірки порожньої книги."""
        assert contact_book.is_empty() is True

    def test_is_empty_on_filled_book(self, filled_contact_book):
        """Тест перевірки заповненої книги."""
        assert filled_contact_book.is_empty() is False

    def test_is_empty_after_adding_contact(self, contact_book):
        """Тест перевірки після додавання контакту."""
        contact_book.add("John", "1234567890")
        assert contact_book.is_empty() is False

    def test_contacts_are_mutable(self, contact_book):
        """Тест що контакти можна змінювати."""
        contact_book.add("John", "1234567890")
        contact_book.contacts["John"] = "9999999999"
        assert contact_book.get_phone("John") == "9999999999"