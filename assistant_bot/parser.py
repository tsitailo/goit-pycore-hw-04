"""
Модуль для парсингу команд користувача.
"""

def parse_input(user_input):
    """
    Розбирає введений користувачем рядок на команду та аргументи.

    Args:
        user_input (str): Рядок введений користувачем

    Returns:
        tuple: Кортеж з команди та списку аргументів
    """
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args