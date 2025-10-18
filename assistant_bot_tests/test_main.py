"""
Тести для модуля main.
"""

from unittest.mock import patch

from assistant_bot.main import main


class TestMain:
    """Тести для функції main."""

    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_hello_command(self, mock_print, mock_input):
        """Тест команди hello."""
        mock_input.side_effect = ["hello", "exit"]
        main()

        # Перевіряємо що було викликано print з правильними повідомленнями
        print_calls = [str(call) for call in mock_print.call_args_list]
        assert any("Welcome to the assistant bot!" in str(call) for call in print_calls)
        assert any("How can I help you?" in str(call) for call in print_calls)
        assert any("Good bye!" in str(call) for call in print_calls)

    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_exit_command(self, mock_print, mock_input):
        """Тест команди exit."""
        mock_input.side_effect = ["exit"]
        main()

        print_calls = [str(call) for call in mock_print.call_args_list]
        assert any("Good bye!" in str(call) for call in print_calls)

    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_close_command(self, mock_print, mock_input):
        """Тест команди close."""
        mock_input.side_effect = ["close"]
        main()

        print_calls = [str(call) for call in mock_print.call_args_list]
        assert any("Good bye!" in str(call) for call in print_calls)

    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_add_command(self, mock_print, mock_input):
        """Тест команди add."""
        mock_input.side_effect = ["add John 1234567890", "exit"]
        main()

        print_calls = [str(call) for call in mock_print.call_args_list]
        assert any("Contact added." in str(call) for call in print_calls)

    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_change_command(self, mock_print, mock_input):
        """Тест команди change."""
        mock_input.side_effect = [
            "add John 1234567890",
            "change John 9999999999",
            "exit"
        ]
        main()

        print_calls = [str(call) for call in mock_print.call_args_list]
        assert any("Contact updated." in str(call) for call in print_calls)

    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_phone_command(self, mock_print, mock_input):
        """Тест команди phone."""
        mock_input.side_effect = [
            "add John 1234567890",
            "phone John",
            "exit"
        ]
        main()

        print_calls = [str(call) for call in mock_print.call_args_list]
        assert any("1234567890" in str(call) for call in print_calls)

    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_all_command(self, mock_print, mock_input):
        """Тест команди all."""
        mock_input.side_effect = [
            "add John 1234567890",
            "add Alice 0987654321",
            "all",
            "exit"
        ]
        main()

        print_calls = [str(call) for call in mock_print.call_args_list]
        # Перевіряємо що виведено обидва контакти
        output = " ".join([str(call) for call in print_calls])
        assert "John: 1234567890" in output
        assert "Alice: 0987654321" in output

    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_invalid_command(self, mock_print, mock_input):
        """Тест невалідної команди."""
        mock_input.side_effect = ["invalid", "exit"]
        main()

        print_calls = [str(call) for call in mock_print.call_args_list]
        assert any("Invalid command." in str(call) for call in print_calls)

    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_multiple_commands(self, mock_print, mock_input):
        """Тест виконання кількох команд підряд."""
        mock_input.side_effect = [
            "hello",
            "add John 1234567890",
            "add Alice 0987654321",
            "phone John",
            "change John 9999999999",
            "phone John",
            "all",
            "exit"
        ]
        main()

        print_calls = [str(call) for call in mock_print.call_args_list]
        output = " ".join([str(call) for call in print_calls])

        assert "How can I help you?" in output
        assert "Contact added." in output
        assert "1234567890" in output
        assert "Contact updated." in output
        assert "9999999999" in output
        assert "Good bye!" in output

    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_case_insensitive_commands(self, mock_print, mock_input):
        """Тест що команди не чутливі до регістру."""
        mock_input.side_effect = [
            "HELLO",
            "ADD John 1234567890",
            "PHONE John",
            "EXIT"
        ]
        main()

        print_calls = [str(call) for call in mock_print.call_args_list]
        output = " ".join([str(call) for call in print_calls])

        assert "How can I help you?" in output
        assert "Contact added." in output
        assert "1234567890" in output

    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_empty_contact_book_all(self, mock_print, mock_input):
        """Тест команди all на порожній книзі контактів."""
        mock_input.side_effect = ["all", "exit"]
        main()

        print_calls = [str(call) for call in mock_print.call_args_list]
        assert any("No contacts saved." in str(call) for call in print_calls)

    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_phone_non_existing_contact(self, mock_print, mock_input):
        """Тест команди phone для неіснуючого контакту."""
        mock_input.side_effect = ["phone John", "exit"]
        main()

        print_calls = [str(call) for call in mock_print.call_args_list]
        assert any("Error: Contact 'John' not found." in str(call) for call in print_calls)

    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_change_non_existing_contact(self, mock_print, mock_input):
        """Тест команди change для неіснуючого контакту."""
        mock_input.side_effect = ["change John 9999999999", "exit"]
        main()

        print_calls = [str(call) for call in mock_print.call_args_list]
        assert any("Error: Contact 'John' not found." in str(call) for call in print_calls)