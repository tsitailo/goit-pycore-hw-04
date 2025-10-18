import os
import tempfile
import unittest
from io import StringIO
from unittest.mock import patch

from total_salary import total_salary


class TestTotalSalary(unittest.TestCase):
    """Тестовий клас для функції total_salary з максимальним покриттям коду"""

    def setUp(self):
        """Підготовка перед кожним тестом - створення тимчасової директорії"""
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Очищення після кожного тесту"""
        # Видаляємо всі файли з тимчасової директорії
        for file in os.listdir(self.test_dir):
            os.remove(os.path.join(self.test_dir, file))
        os.rmdir(self.test_dir)

    def create_test_file(self, filename, content):
        """Допоміжний метод для створення тестових файлів"""
        filepath = os.path.join(self.test_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return filepath

    # ==================== ТЕСТИ УСПІШНИХ СЦЕНАРІЇВ ====================

    def test_exact_example_from_task(self):
        """Тест 0: Точний приклад з умови завдання"""
        content = """Alex Korp,3000
Nikita Borisenko,2000
Sitarama Raju,1000
"""
        filepath = self.create_test_file("salary_file.txt", content)

        total, average = total_salary(filepath)

        self.assertEqual(total, 6000, "Загальна сума повинна бути 6000")
        self.assertEqual(average, 2000, "Середня зарплата повинна бути 2000")

        # Також перевіряємо вивід як в прикладі
        print(f"Загальна сума заробітної плати: {total}, Середня заробітна плата: {average}")

    def test_exact_example_without_trailing_newline(self):
        """Тест 0a: Точний приклад з умови завдання БЕЗ останнього переносу рядка"""
        content = """Alex Korp,3000
Nikita Borisenko,2000
Sitarama Raju,1000"""
        filepath = self.create_test_file("salary_file_no_newline.txt", content)

        total, average = total_salary(filepath)

        self.assertEqual(total, 6000, "Загальна сума повинна бути 6000")
        self.assertEqual(average, 2000, "Середня зарплата повинна бути 2000")

    def test_exact_example_with_extra_blank_lines(self):
        """Тест 0b: Точний приклад з умови завдання з порожніми рядками"""
        content = """Alex Korp,3000

Nikita Borisenko,2000

Sitarama Raju,1000

"""
        filepath = self.create_test_file("salary_file_blank_lines.txt", content)

        total, average = total_salary(filepath)

        self.assertEqual(total, 6000, "Загальна сума повинна бути 6000")
        self.assertEqual(average, 2000, "Середня зарплата повинна бути 2000")

    def test_exact_example_with_spaces(self):
        """Тест 0c: Точний приклад з пробілами після ком"""
        content = """Alex Korp, 3000
Nikita Borisenko, 2000
Sitarama Raju, 1000
"""
        filepath = self.create_test_file("salary_file_spaces.txt", content)

        total, average = total_salary(filepath)

        self.assertEqual(total, 6000, "Загальна сума повинна бути 6000")
        self.assertEqual(average, 2000, "Середня зарплата повинна бути 2000")

    def test_normal_case_three_employees(self):
        """Тест 1: Стандартний випадок з трьома працівниками"""
        content = "Alex Korp,3000\nNikita Borisenko,2000\nSitarama Raju,1000\n"
        filepath = self.create_test_file("test1.txt", content)

        total, average = total_salary(filepath)

        self.assertEqual(total, 6000)
        self.assertEqual(average, 2000)

    def test_single_employee(self):
        """Тест 2: Один працівник"""
        content = "John Doe,5000\n"
        filepath = self.create_test_file("test2.txt", content)

        total, average = total_salary(filepath)

        self.assertEqual(total, 5000)
        self.assertEqual(average, 5000)

    def test_float_salaries(self):
        """Тест 3: Зарплати з десятковими значеннями"""
        content = "Employee1,2500.50\nEmployee2,3000.75\nEmployee3,1500.25\n"
        filepath = self.create_test_file("test3.txt", content)

        total, average = total_salary(filepath)

        self.assertEqual(total, 7001)  # 2500.50 + 3000.75 + 1500.25 = 7001.50 -> 7001
        self.assertEqual(average, 2333)  # 7001.50 / 3 = 2333.83 -> 2333

    def test_spaces_in_salary(self):
        """Тест 4: Пробіли навколо значення зарплати"""
        content = "Employee1, 2000 \nEmployee2,  3000  \n"
        filepath = self.create_test_file("test4.txt", content)

        total, average = total_salary(filepath)

        self.assertEqual(total, 5000)
        self.assertEqual(average, 2500)

    def test_empty_lines_in_file(self):
        """Тест 5: Файл з порожніми рядками"""
        content = "Employee1,1000\n\nEmployee2,2000\n\n\nEmployee3,3000\n"
        filepath = self.create_test_file("test5.txt", content)

        total, average = total_salary(filepath)

        self.assertEqual(total, 6000)
        self.assertEqual(average, 2000)

    def test_unicode_names(self):
        """Тест 6: Імена з Unicode символами (кирилиця, спецсимволи)"""
        content = "Іван Петренко,2500\nМарія Коваль,3500\nÄäÖöÜü,1000\n"
        filepath = self.create_test_file("test6.txt", content)

        total, average = total_salary(filepath)

        self.assertEqual(total, 7000)
        self.assertEqual(average, 2333)

    def test_large_numbers(self):
        """Тест 7: Великі числа зарплат"""
        content = "CEO,1000000\nCTO,500000\nCFO,500000\n"
        filepath = self.create_test_file("test7.txt", content)

        total, average = total_salary(filepath)

        self.assertEqual(total, 2000000)
        self.assertEqual(average, 666666)

    # ==================== ТЕСТИ КРАЙОВИХ ВИПАДКІВ ====================

    def test_empty_file(self):
        """Тест 8: Порожній файл"""
        filepath = self.create_test_file("test8.txt", "")

        with patch('sys.stdout', new=StringIO()) as fake_out:
            total, average = total_salary(filepath)
            output = fake_out.getvalue()

        self.assertEqual(total, 0)
        self.assertEqual(average, 0)
        self.assertIn("не містить коректних даних", output)

    def test_only_empty_lines(self):
        """Тест 9: Файл тільки з порожніми рядками"""
        content = "\n\n\n\n"
        filepath = self.create_test_file("test9.txt", content)

        with patch('sys.stdout', new=StringIO()) as fake_out:
            total, average = total_salary(filepath)
            output = fake_out.getvalue()

        self.assertEqual(total, 0)
        self.assertEqual(average, 0)
        self.assertIn("не містить коректних даних", output)

    def test_zero_salary(self):
        """Тест 10: Нульова зарплата"""
        content = "Intern,0\nEmployee,2000\n"
        filepath = self.create_test_file("test10.txt", content)

        total, average = total_salary(filepath)

        self.assertEqual(total, 2000)
        self.assertEqual(average, 1000)

    def test_negative_salary(self):
        """Тест 11: Від'ємна зарплата (технічно валідна)"""
        content = "Employee1,-1000\nEmployee2,3000\n"
        filepath = self.create_test_file("test11.txt", content)

        total, average = total_salary(filepath)

        self.assertEqual(total, 2000)
        self.assertEqual(average, 1000)

    # ==================== ТЕСТИ ПОМИЛКОВИХ СИТУАЦІЙ ====================

    def test_file_not_found(self):
        """Тест 12: Файл не існує"""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            total, average = total_salary("nonexistent_file.txt")
            output = fake_out.getvalue()

        self.assertEqual(total, 0)
        self.assertEqual(average, 0)
        self.assertIn("не знайдено", output)

    def test_invalid_format_missing_comma(self):
        """Тест 13: Неправильний формат - відсутня кома"""
        content = "Employee1 2000\nEmployee2,3000\n"
        filepath = self.create_test_file("test13.txt", content)

        with patch('sys.stdout', new=StringIO()) as fake_out:
            total, average = total_salary(filepath)
            output = fake_out.getvalue()

        self.assertEqual(total, 3000)  # Обробився тільки другий рядок
        self.assertEqual(average, 3000)
        self.assertIn("Неправильний формат", output)

    def test_invalid_format_multiple_commas(self):
        """Тест 14: Неправильний формат - кілька ком"""
        content = "Employee1,2000,extra\nEmployee2,3000\n"
        filepath = self.create_test_file("test14.txt", content)

        with patch('sys.stdout', new=StringIO()) as fake_out:
            total, average = total_salary(filepath)
            output = fake_out.getvalue()

        self.assertEqual(total, 3000)  # Обробився тільки другий рядок
        self.assertEqual(average, 3000)
        self.assertIn("Неправильний формат", output)

    def test_invalid_salary_value_text(self):
        """Тест 15: Некоректне значення зарплати - текст"""
        content = "Employee1,abc\nEmployee2,2000\n"
        filepath = self.create_test_file("test15.txt", content)

        with patch('sys.stdout', new=StringIO()) as fake_out:
            total, average = total_salary(filepath)
            output = fake_out.getvalue()

        self.assertEqual(total, 2000)  # Обробився тільки другий рядок
        self.assertEqual(average, 2000)
        self.assertIn("Некоректне значення зарплати", output)

    def test_invalid_salary_value_special_chars(self):
        """Тест 16: Некоректне значення зарплати - спецсимволи"""
        content = "Employee1,@#$%\nEmployee2,1500\n"
        filepath = self.create_test_file("test16.txt", content)

        with patch('sys.stdout', new=StringIO()) as fake_out:
            total, average = total_salary(filepath)
            output = fake_out.getvalue()

        self.assertEqual(total, 1500)
        self.assertEqual(average, 1500)
        self.assertIn("Некоректне значення зарплати", output)

    def test_mixed_valid_invalid_lines(self):
        """Тест 17: Змішані валідні та невалідні рядки"""
        content = """Employee1,2000
Employee2 3000
Employee3,abc
Employee4,4000

InvalidLine
Employee5,1000
"""
        filepath = self.create_test_file("test17.txt", content)

        with patch('sys.stdout', new=StringIO()) as fake_out:
            total, average = total_salary(filepath)
            output = fake_out.getvalue()

        self.assertEqual(total, 7000)  # 2000 + 4000 + 1000
        self.assertEqual(average, 2333)
        self.assertIn("Неправильний формат", output)
        self.assertIn("Некоректне значення", output)

    def test_only_invalid_lines(self):
        """Тест 18: Тільки невалідні рядки"""
        content = "InvalidLine\nAnother Invalid\n12345\n"
        filepath = self.create_test_file("test18.txt", content)

        with patch('sys.stdout', new=StringIO()) as fake_out:
            total, average = total_salary(filepath)
            output = fake_out.getvalue()

        self.assertEqual(total, 0)
        self.assertEqual(average, 0)
        self.assertIn("не містить коректних даних", output)

    # ==================== ТЕСТИ РІЗНИХ КОДУВАНЬ ====================

    def test_different_line_endings_unix(self):
        """Тест 20: Unix line endings (LF)"""
        content = "Employee1,1000\nEmployee2,2000\nEmployee3,3000\n"
        filepath = self.create_test_file("test20.txt", content)

        total, average = total_salary(filepath)

        self.assertEqual(total, 6000)
        self.assertEqual(average, 2000)

    def test_different_line_endings_windows(self):
        """Тест 21: Windows line endings (CRLF)"""
        content = "Employee1,1000\r\nEmployee2,2000\r\nEmployee3,3000\r\n"
        filepath = self.create_test_file("test21.txt", content)

        total, average = total_salary(filepath)

        self.assertEqual(total, 6000)
        self.assertEqual(average, 2000)

    def test_no_trailing_newline(self):
        """Тест 22: Файл без завершального символу нового рядка"""
        content = "Employee1,1000\nEmployee2,2000"  # Немає \n в кінці
        filepath = self.create_test_file("test22.txt", content)

        total, average = total_salary(filepath)

        self.assertEqual(total, 3000)
        self.assertEqual(average, 1500)

    # ==================== ТЕСТИ ПРОДУКТИВНОСТІ ====================

    def test_large_file_performance(self):
        """Тест 23: Великий файл (1000 записів)"""
        content = "\n".join([f"Employee{i},{i * 1000}" for i in range(1, 1001)])
        filepath = self.create_test_file("test23.txt", content)

        total, average = total_salary(filepath)

        expected_total = sum(i * 1000 for i in range(1, 1001))
        expected_average = expected_total // 1000

        self.assertEqual(total, expected_total)
        self.assertEqual(average, expected_average)

    # ==================== ТЕСТИ СПЕЦІАЛЬНИХ ВИПАДКІВ ====================

    def test_comma_in_name(self):
        """Тест 24: Кома в імені (неправильний формат, але реальний сценарій)"""
        content = "Employee, Name,2000\nNormal Name,3000\n"
        filepath = self.create_test_file("test24.txt", content)

        with patch('sys.stdout', new=StringIO()) as fake_out:
            total, average = total_salary(filepath)
            output = fake_out.getvalue()

        self.assertEqual(total, 3000)  # Перший рядок не обробиться
        self.assertEqual(average, 3000)
        self.assertIn("Неправильний формат", output)

    def test_whitespace_only_name(self):
        """Тест 25: Тільки пробіли замість імені"""
        content = "   ,2000\nEmployee,3000\n"
        filepath = self.create_test_file("test25.txt", content)

        total, average = total_salary(filepath)

        # Технічно це валідний формат (ім'я може бути порожнім)
        self.assertEqual(total, 5000)
        self.assertEqual(average, 2500)

    def test_scientific_notation(self):
        """Тест 26: Наукова нотація для зарплати"""
        content = "Employee1,1e3\nEmployee2,2E3\n"  # 1000 та 2000
        filepath = self.create_test_file("test26.txt", content)

        total, average = total_salary(filepath)

        self.assertEqual(total, 3000)
        self.assertEqual(average, 1500)

    def test_very_long_name(self):
        """Тест 27: Дуже довге ім'я"""
        long_name = "A" * 1000
        content = f"{long_name},5000\n"
        filepath = self.create_test_file("test27.txt", content)

        total, average = total_salary(filepath)

        self.assertEqual(total, 5000)
        self.assertEqual(average, 5000)

    def test_salary_with_plus_sign(self):
        """Тест 28: Зарплата з знаком плюс"""
        content = "Employee1,+2000\nEmployee2,3000\n"
        filepath = self.create_test_file("test28.txt", content)

        total, average = total_salary(filepath)

        self.assertEqual(total, 5000)
        self.assertEqual(average, 2500)


# ==================== ЗАПУСК ТЕСТІВ ====================

if __name__ == '__main__':
    # Створюємо test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestTotalSalary)

    # Запускаємо тести з детальним виводом
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Виводимо статистику покриття
    print("\n" + "=" * 70)
    print("СТАТИСТИКА ТЕСТУВАННЯ")
    print("=" * 70)
    print(f"Всього тестів: {result.testsRun}")
    print(f"Успішних: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Провалених: {len(result.failures)}")
    print(f"Помилок: {len(result.errors)}")
    print(f"Пропущених: {len(result.skipped)}")
    print(f"Успішність: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.2f}%")
    print("=" * 70)