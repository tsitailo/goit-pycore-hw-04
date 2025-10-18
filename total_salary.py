def total_salary(path):
    """
    Аналізує файл із зарплатами розробників та обчислює загальну і середню суму.

    Args:
        path (str): Шлях до текстового файлу з даними про зарплати

    Returns:
        tuple: Кортеж з двох чисел (загальна сума, середня зарплата)
        або (0, 0) у разі помилки
    """
    try:
        total = 0
        count = 0

        # Відкриваємо файл з явним вказанням кодування
        with open(path, 'r', encoding='utf-8') as file:
            for line in file:
                # Видаляємо зайві пробіли та символи нового рядка
                line = line.strip()

                # Пропускаємо порожні рядки
                if not line:
                    continue

                # Розділяємо рядок на ім'я та зарплату
                parts = line.split(',')

                # Перевіряємо, чи рядок має правильний формат
                if len(parts) != 2:
                    print(f"Попередження: Неправильний формат рядка: {line}")
                    continue

                try:
                    # Отримуємо зарплату (другий елемент)
                    salary = float(parts[1].strip())
                    total += salary
                    count += 1
                except ValueError:
                    print(f"Попередження: Некоректне значення зарплати в рядку: {line}")
                    continue

        # Обчислюємо середню зарплату
        if count > 0:
            average = total / count
            return (int(total), int(average))
        else:
            print("Файл не містить коректних даних про зарплати")
            return (0, 0)

    except FileNotFoundError:
        print(f"Помилка: Файл '{path}' не знайдено")
        return (0, 0)

    except PermissionError:
        print(f"Помилка: Немає прав доступу до файлу '{path}'")
        return (0, 0)

    except Exception as e:
        print(f"Непередбачена помилка: {e}")
        return (0, 0)


def main():
    """
    Основна функція для демонстрації роботи модуля.
    """
    # Приклад використання
    print("=== Демонстрація роботи total_salary ===\n")

    # Зчитуємо дані про зарплати
    total, average = total_salary("salary_file.txt")

    # Виводимо результат
    if total > 0:
        print(f"Загальна сума зарплат: {total}")
        print(f"Середня зарплата: {average}")
    else:
        print("Не вдалося отримати дані про зарплати.")


if __name__ == "__main__":
    main()
