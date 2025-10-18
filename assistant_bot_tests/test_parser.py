"""
Тести для модуля parser.
"""

from assistant_bot.parser import parse_input


class TestParseInput:
    """Тести для функції parse_input."""

    def test_parse_simple_command(self):
        """Тест парсингу простої команди без аргументів."""
        cmd, *args = parse_input("hello")
        assert cmd == "hello"
        assert args == []

    def test_parse_command_with_one_argument(self):
        """Тест парсингу команди з одним аргументом."""
        cmd, *args = parse_input("phone John")
        assert cmd == "phone"
        assert args == ["John"]

    def test_parse_command_with_two_arguments(self):
        """Тест парсингу команди з двома аргументами."""
        cmd, *args = parse_input("add John 1234567890")
        assert cmd == "add"
        assert args == ["John", "1234567890"]

    def test_parse_command_with_multiple_arguments(self):
        """Тест парсингу команди з багатьма аргументами."""
        cmd, *args = parse_input("add John Doe 1234567890")
        assert cmd == "add"
        assert args == ["John", "Doe", "1234567890"]

    def test_parse_uppercase_command(self):
        """Тест парсингу команди у верхньому регістрі."""
        cmd, *args = parse_input("HELLO")
        assert cmd == "hello"
        assert args == []

    def test_parse_mixed_case_command(self):
        """Тест парсингу команди у змішаному регістрі."""
        cmd, *args = parse_input("HeLLo")
        assert cmd == "hello"
        assert args == []

    def test_parse_command_with_extra_spaces(self):
        """Тест парсингу команди з зайвими пробілами."""
        cmd, *args = parse_input("  add   John   1234567890  ")
        assert cmd == "add"
        assert args == ["John", "1234567890"]

    def test_parse_exit_command(self):
        """Тест парсингу команди exit."""
        cmd, *args = parse_input("exit")
        assert cmd == "exit"
        assert args == []

    def test_parse_close_command(self):
        """Тест парсингу команди close."""
        cmd, *args = parse_input("close")
        assert cmd == "close"
        assert args == []

    def test_parse_command_with_tabs(self):
        """Тест парсингу команди з табуляцією."""
        cmd, *args = parse_input("add\tJohn\t1234567890")
        assert cmd == "add"
        assert args == ["John", "1234567890"]