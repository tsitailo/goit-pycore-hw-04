# hw03.py
import sys
from pathlib import Path
from colorama import Fore, Style, init


# Ініціалізація colorama для підтримки кольорів у Windows
init(autoreset=True)


def visualize_directory_structure(directory_path, prefix="", is_last=True):
    """
    Рекурсивно візуалізує структуру директорії з кольоровим виведенням.

    Args:
        directory_path: Path об'єкт директорії для візуалізації
        prefix: Рядок префіксу для форматування дерева
        is_last: Чи є поточний елемент останнім у списку
    """
    try:
        # Визначаємо символи для гілок дерева
        connector = "┗ " if is_last else "┣ "

        # Виводимо ім'я поточної директорії
        if prefix == "":
            # Корінь дерева
            print(f"{Fore.BLUE}{Style.BRIGHT}📦 {directory_path.name}")

        # Отримуємо всі елементи в директорії
        try:
            items = sorted(directory_path.iterdir(),
                           key=lambda x: (not x.is_dir(), x.name.lower()))
        except PermissionError:
            print(f"{prefix}{connector}{Fore.RED}[Доступ заборонено]")
            return

        # Обробляємо кожен елемент
        for index, item in enumerate(items):
            is_last_item = index == len(items) - 1

            if item.is_dir():
                # Директорія - синій колір
                print(f"{prefix}{connector}{Fore.CYAN}{Style.BRIGHT}📂 {item.name}")

                # Визначаємо новий префікс для вкладених елементів
                extension = "   " if is_last_item else " ┃ "
                visualize_directory_structure(
                    item,
                    prefix + extension,
                    is_last=True
                )
            else:
                # Файл - зелений колір
                print(f"{prefix}{connector}{Fore.GREEN}📜 {item.name}")

            # Оновлюємо connector для наступних елементів
            connector = "┗ " if is_last_item else "┣ "

    except Exception as e:
        print(f"{Fore.RED}Помилка при обробці {directory_path}: {str(e)}")


def main():
    """
    Головна функція скрипту.
    Обробляє аргументи командного рядка та запускає візуалізацію.
    """
    # Перевірка наявності аргументів
    if len(sys.argv) < 2:
        print(f"{Fore.RED}Помилка: Не вказано шлях до директорії!")
        print(f"{Fore.YELLOW}Використання: python hw03.py <шлях_до_директорії>")
        print(f"{Fore.YELLOW}Приклад: python hw03.py ./picture")
        sys.exit(1)

    # Отримання шляху з аргументів
    directory_path = Path(sys.argv[1])

    # Перевірка існування шляху
    if not directory_path.exists():
        print(f"{Fore.RED}Помилка: Шлях '{directory_path}' не існує!")
        sys.exit(1)

    # Перевірка, чи це директорія
    if not directory_path.is_dir():
        print(f"{Fore.RED}Помилка: '{directory_path}' не є директорією!")
        sys.exit(1)

    # Виведення заголовка
    print(f"\n{Fore.YELLOW}{Style.BRIGHT}{'=' * 50}")
    print(f"{Fore.YELLOW}{Style.BRIGHT}Структура директорії: {directory_path.absolute()}")
    print(f"{Fore.YELLOW}{Style.BRIGHT}{'=' * 50}\n")

    # Візуалізація структури
    visualize_directory_structure(directory_path)

    print(f"\n{Fore.YELLOW}{Style.BRIGHT}{'=' * 50}\n")


if __name__ == "__main__":
    main()