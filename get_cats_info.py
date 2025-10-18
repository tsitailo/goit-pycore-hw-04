def get_cats_info(path):
    """
    Читає файл з інформацією про котів та повертає список словників.

    Функція читає текстовий файл, де кожен рядок містить інформацію про одного кота
    у форматі: id,name,age (значення розділені комами).

    Args:
        path (str): Шлях до текстового файлу з даними про котів

    Returns:
        list: Список словників з інформацією про котів.
              Кожен словник містить ключі: "id", "name", "age"
              Повертає порожній список у разі помилки або якщо файл порожній

    Example:
        >>> cats_info = get_cats_info("cats_file.txt")
        >>> print(cats_info)
        [
            {"id": "60b90c1c13067a15887e1ae1", "name": "Tayson", "age": "3"},
            {"id": "60b90c2413067a15887e1ae2", "name": "Vika", "age": "1"}
        ]

    Raises:
        Функція не викидає винятки, але виводить повідомлення про помилки:
        - FileNotFoundError: якщо файл не знайдено
        - PermissionError: якщо немає прав доступу до файлу
        - Exception: для інших непередбачених помилок
    """
    cats_list = []

    try:
        # Відкриваємо файл з явним вказанням кодування UTF-8
        with open(path, 'r', encoding='utf-8') as file:
            # Читаємо файл построково
            for line_number, line in enumerate(file, 1):
                # Видаляємо зайві пробіли та символи нового рядка
                line = line.strip()

                # Пропускаємо порожні рядки
                if not line:
                    continue

                try:
                    # Розділяємо рядок на частини
                    parts = line.split(',')

                    # Перевіряємо, чи є всі необхідні дані
                    if len(parts) == 3:
                        cat_id, name, age = parts

                        # Створюємо словник з інформацією про кота
                        cat_info = {
                            "id": cat_id.strip(),
                            "name": name.strip(),
                            "age": age.strip()
                        }

                        # Додаємо словник до списку
                        cats_list.append(cat_info)
                    else:
                        print(f"Попередження (рядок {line_number}): "
                              f"Рядок має неправильний формат: {line}")

                except ValueError as e:
                    print(f"Помилка обробки рядка {line_number} '{line}': {e}")
                    continue

    except FileNotFoundError:
        print(f"Помилка: Файл '{path}' не знайдено.")
    except PermissionError:
        print(f"Помилка: Немає прав доступу до файлу '{path}'.")
    except Exception as e:
        print(f"Неочікувана помилка при читанні файлу: {e}")

    return cats_list


def main():
    """
    Основна функція для демонстрації роботи модуля.
    """
    # Приклад використання
    print("=== Демонстрація роботи get_cats_info ===\n")

    # Читаємо дані про котів
    cats_info = get_cats_info("cats_file.txt")

    # Виводимо результат
    if cats_info:
        print(f"Знайдено котів: {len(cats_info)}\n")
        for i, cat in enumerate(cats_info, 1):
            print(f"{i}. {cat['name']} (ID: {cat['id']}, Вік: {cat['age']})")
    else:
        print("Котів не знайдено або виникла помилка.")


if __name__ == "__main__":
    main()