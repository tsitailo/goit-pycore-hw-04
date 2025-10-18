import unittest
import os
import tempfile
from pathlib import Path

from get_cats_info import get_cats_info


class TestGetCatsInfo(unittest.TestCase):
    """Тести для функції get_cats_info з максимальним покриттям"""

    def setUp(self):
        """Підготовка перед кожним тестом"""
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Очищення після кожного тесту"""
        # Видаляємо всі тестові файли
        for file in Path(self.test_dir).glob('*'):
            try:
                file.unlink()
            except:
                pass
        try:
            os.rmdir(self.test_dir)
        except:
            pass

    def create_test_file(self, filename, content):
        """Допоміжна функція для створення тестових файлів"""
        filepath = os.path.join(self.test_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return filepath

    # ========== ПОЗИТИВНІ ТЕСТИ ==========

    def test_valid_data_all_cats(self):
        """Тест 1: Валідні дані - всі коти з базових даних"""
        content = """60b90c1c13067a15887e1ae1,Tayson,3
60b90c2413067a15887e1ae2,Vika,1
60b90c2e13067a15887e1ae3,Barsik,2
60b90c3b13067a15887e1ae4,Simon,12
60b90c4613067a15887e1ae5,Tessi,5"""

        filepath = self.create_test_file('cats_valid.txt', content)
        result = get_cats_info(filepath)

        expected = [
            {"id": "60b90c1c13067a15887e1ae1", "name": "Tayson", "age": "3"},
            {"id": "60b90c2413067a15887e1ae2", "name": "Vika", "age": "1"},
            {"id": "60b90c2e13067a15887e1ae3", "name": "Barsik", "age": "2"},
            {"id": "60b90c3b13067a15887e1ae4", "name": "Simon", "age": "12"},
            {"id": "60b90c4613067a15887e1ae5", "name": "Tessi", "age": "5"},
        ]

        self.assertEqual(result, expected)
        self.assertEqual(len(result), 5)

    def test_single_cat(self):
        """Тест 2: Файл з одним котом"""
        content = "60b90c1c13067a15887e1ae1,Tayson,3"
        filepath = self.create_test_file('single_cat.txt', content)
        result = get_cats_info(filepath)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "Tayson")
        self.assertEqual(result[0]["age"], "3")

    def test_data_with_spaces(self):
        """Тест 3: Дані з пробілами (повинні видалятися)"""
        content = """60b90c1c13067a15887e1ae1, Tayson , 3
60b90c2413067a15887e1ae2,  Vika,1  """

        filepath = self.create_test_file('cats_spaces.txt', content)
        result = get_cats_info(filepath)

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["name"], "Tayson")
        self.assertEqual(result[0]["age"], "3")
        self.assertEqual(result[1]["name"], "Vika")

    def test_empty_lines_in_file(self):
        """Тест 4: Файл з порожніми рядками"""
        content = """60b90c1c13067a15887e1ae1,Tayson,3

60b90c2413067a15887e1ae2,Vika,1

"""
        filepath = self.create_test_file('cats_empty_lines.txt', content)
        result = get_cats_info(filepath)

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["name"], "Tayson")
        self.assertEqual(result[1]["name"], "Vika")

    def test_age_variations(self):
        """Тест 5: Різні значення віку"""
        content = """60b90c1c13067a15887e1ae1,Young,0
60b90c2413067a15887e1ae2,Old,20
60b90c2e13067a15887e1ae3,Middle,5"""

        filepath = self.create_test_file('cats_ages.txt', content)
        result = get_cats_info(filepath)

        self.assertEqual(len(result), 3)
        self.assertEqual(result[0]["age"], "0")
        self.assertEqual(result[1]["age"], "20")
        self.assertEqual(result[2]["age"], "5")

    def test_special_characters_in_names(self):
        """Тест 6: Спеціальні символи в іменах"""
        content = """60b90c1c13067a15887e1ae1,Mr.Whiskers,3
60b90c2413067a15887e1ae2,Муся,5
60b90c2e13067a15887e1ae3,Cat-123,2"""

        filepath = self.create_test_file('cats_special_names.txt', content)
        result = get_cats_info(filepath)

        self.assertEqual(len(result), 3)
        self.assertEqual(result[0]["name"], "Mr.Whiskers")
        self.assertEqual(result[1]["name"], "Муся")
        self.assertEqual(result[2]["name"], "Cat-123")

    def test_long_ids(self):
        """Тест 7: Довгі ID"""
        content = """60b90c1c13067a15887e1ae1ffffffffff,LongID,3"""
        filepath = self.create_test_file('cats_long_id.txt', content)
        result = get_cats_info(filepath)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["id"], "60b90c1c13067a15887e1ae1ffffffffff")

    # ========== НЕГАТИВНІ ТЕСТИ ==========

    def test_file_not_found(self):
        """Тест 8: Файл не існує"""
        result = get_cats_info('non_existent_file.txt')
        self.assertEqual(result, [])

    def test_empty_file(self):
        """Тест 9: Порожній файл"""
        filepath = self.create_test_file('empty.txt', '')
        result = get_cats_info(filepath)

        self.assertEqual(result, [])
        self.assertEqual(len(result), 0)

    def test_invalid_format_too_few_fields(self):
        """Тест 10: Недостатньо полів (менше 3)"""
        content = """60b90c1c13067a15887e1ae1,Tayson
60b90c2413067a15887e1ae2,Vika,1"""

        filepath = self.create_test_file('cats_invalid_few.txt', content)
        result = get_cats_info(filepath)

        # Повинен повернути тільки валідний запис
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "Vika")

    def test_invalid_format_too_many_fields(self):
        """Тест 11: Забагато полів (більше 3)"""
        content = """60b90c1c13067a15887e1ae1,Tayson,3,extra
60b90c2413067a15887e1ae2,Vika,1"""

        filepath = self.create_test_file('cats_invalid_many.txt', content)
        result = get_cats_info(filepath)

        # Повинен повернути тільки валідний запис
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "Vika")

    def test_mixed_valid_invalid_data(self):
        """Тест 12: Змішані валідні та невалідні дані"""
        content = """60b90c1c13067a15887e1ae1,Tayson,3
invalid_line_without_commas
60b90c2413067a15887e1ae2,Vika,1
,empty_id,5
60b90c2e13067a15887e1ae3,Barsik,2"""

        filepath = self.create_test_file('cats_mixed.txt', content)
        result = get_cats_info(filepath)

        # Повинно бути 4 валідні записи (включно з порожнім ID)
        self.assertEqual(len(result), 4)
        self.assertEqual(result[0]["name"], "Tayson")
        self.assertEqual(result[1]["name"], "Vika")

    def test_only_whitespace_lines(self):
        """Тест 13: Файл тільки з пробілами"""
        content = """   

\t\t
"""
        filepath = self.create_test_file('whitespace.txt', content)
        result = get_cats_info(filepath)

        self.assertEqual(result, [])

    def test_missing_values(self):
        """Тест 14: Відсутні значення в полях"""
        content = """60b90c1c13067a15887e1ae1,,3
,Vika,1
60b90c2e13067a15887e1ae3,Barsik,"""

        filepath = self.create_test_file('cats_missing.txt', content)
        result = get_cats_info(filepath)

        # Всі три рядки технічно валідні (є 3 поля)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0]["name"], "")
        self.assertEqual(result[1]["id"], "")
        self.assertEqual(result[2]["age"], "")

    # ========== КРАЙНІ ВИПАДКИ ==========

    def test_very_long_line(self):
        """Тест 15: Дуже довгий рядок"""
        long_name = "A" * 1000
        content = f"60b90c1c13067a15887e1ae1,{long_name},3"

        filepath = self.create_test_file('long_line.txt', content)
        result = get_cats_info(filepath)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], long_name)

    def test_unicode_characters(self):
        """Тест 16: Unicode символи"""
        content = """60b90c1c13067a15887e1ae1,Котик🐱,3
60b90c2413067a15887e1ae2,猫,5
60b90c2e13067a15887e1ae3,قطة,2"""

        filepath = self.create_test_file('unicode_cats.txt', content)
        result = get_cats_info(filepath)

        self.assertEqual(len(result), 3)
        self.assertIn("🐱", result[0]["name"])

    def test_newline_variations(self):
        """Тест 17: Різні типи переносу рядків"""
        content = "60b90c1c13067a15887e1ae1,Tayson,3\n60b90c2413067a15887e1ae2,Vika,1\r\n60b90c2e13067a15887e1ae3,Barsik,2"

        filepath = self.create_test_file('cats_newlines.txt', content)
        result = get_cats_info(filepath)

        self.assertEqual(len(result), 3)

    def test_large_file(self):
        """Тест 18: Великий файл (100+ записів)"""
        lines = []
        for i in range(150):
            lines.append(f"id{i:05d},Cat{i},{i % 20}")
        content = '\n'.join(lines)

        filepath = self.create_test_file('large_file.txt', content)
        result = get_cats_info(filepath)

        self.assertEqual(len(result), 150)
        self.assertEqual(result[0]["name"], "Cat0")
        self.assertEqual(result[149]["name"], "Cat149")

    def test_commas_in_values(self):
        """Тест 19: Коми в значеннях (крайній випадок)"""
        content = """60b90c1c13067a15887e1ae1,Tayson,Junior,3"""

        filepath = self.create_test_file('cats_comma.txt', content)
        result = get_cats_info(filepath)

        # Повинен відхилити через 4 поля
        self.assertEqual(len(result), 0)

    def test_numeric_names(self):
        """Тест 20: Числові імена"""
        content = """60b90c1c13067a15887e1ae1,123,3
60b90c2413067a15887e1ae2,456,5"""

        filepath = self.create_test_file('numeric_names.txt', content)
        result = get_cats_info(filepath)

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["name"], "123")
        self.assertEqual(result[1]["name"], "456")

    # ========== ТЕСТИ СТРУКТУРИ ДАНИХ ==========

    def test_return_type(self):
        """Тест 21: Перевірка типу даних, що повертається"""
        content = "60b90c1c13067a15887e1ae1,Tayson,3"
        filepath = self.create_test_file('type_test.txt', content)
        result = get_cats_info(filepath)

        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], dict)

    def test_dictionary_keys(self):
        """Тест 22: Перевірка наявності всіх ключів"""
        content = "60b90c1c13067a15887e1ae1,Tayson,3"
        filepath = self.create_test_file('keys_test.txt', content)
        result = get_cats_info(filepath)

        self.assertIn("id", result[0])
        self.assertIn("name", result[0])
        self.assertIn("age", result[0])
        self.assertEqual(len(result[0].keys()), 3)

    def test_values_are_strings(self):
        """Тест 23: Всі значення повинні бути рядками"""
        content = "60b90c1c13067a15887e1ae1,Tayson,3"
        filepath = self.create_test_file('string_test.txt', content)
        result = get_cats_info(filepath)

        self.assertIsInstance(result[0]["id"], str)
        self.assertIsInstance(result[0]["name"], str)
        self.assertIsInstance(result[0]["age"], str)

    def test_order_preservation(self):
        """Тест 24: Порядок записів повинен зберігатися"""
        content = """60b90c1c13067a15887e1ae1,Tayson,3
60b90c2413067a15887e1ae2,Vika,1
60b90c2e13067a15887e1ae3,Barsik,2"""

        filepath = self.create_test_file('order_test.txt', content)
        result = get_cats_info(filepath)

        self.assertEqual(result[0]["name"], "Tayson")
        self.assertEqual(result[1]["name"], "Vika")
        self.assertEqual(result[2]["name"], "Barsik")

    def test_immutability(self):
        """Тест 25: Кожен виклик повинен повертати новий список"""
        content = "60b90c1c13067a15887e1ae1,Tayson,3"
        filepath = self.create_test_file('immutable_test.txt', content)

        result1 = get_cats_info(filepath)
        result2 = get_cats_info(filepath)

        self.assertIsNot(result1, result2)
        self.assertEqual(result1, result2)


# ========== ДОДАТКОВІ ІНТЕГРАЦІЙНІ ТЕСТИ ==========

class TestIntegration(unittest.TestCase):
    """Інтеграційні тести"""

    def test_full_workflow(self):
        """Тест 26: Повний робочий процес з реальними даними"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as f:
            f.write("""60b90c1c13067a15887e1ae1,Tayson,3
60b90c2413067a15887e1ae2,Vika,1
60b90c2e13067a15887e1ae3,Barsik,2
60b90c3b13067a15887e1ae4,Simon,12
60b90c4613067a15887e1ae5,Tessi,5""")
            filepath = f.name

        try:
            result = get_cats_info(filepath)

            # Перевірка загальної кількості
            self.assertEqual(len(result), 5)

            # Перевірка конкретних значень
            tayson = next(cat for cat in result if cat["name"] == "Tayson")
            self.assertEqual(tayson["age"], "3")

            simon = next(cat for cat in result if cat["name"] == "Simon")
            self.assertEqual(simon["age"], "12")

            # Перевірка унікальності ID
            ids = [cat["id"] for cat in result]
            self.assertEqual(len(ids), len(set(ids)))

        finally:
            os.unlink(filepath)


def run_tests():
    """Запуск всіх тестів з детальним звітом"""
    # Створення test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Додавання всіх тестів
    suite.addTests(loader.loadTestsFromTestCase(TestGetCatsInfo))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))

    # Запуск тестів з детальним виводом
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Підсумковий звіт
    print("\n" + "=" * 70)
    print("ПІДСУМКОВИЙ ЗВІТ")
    print("=" * 70)
    print(f"Всього тестів виконано: {result.testsRun}")
    print(f"Успішних: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Провалених: {len(result.failures)}")
    print(f"Помилок: {len(result.errors)}")
    print(f"Пропущених: {len(result.skipped)}")
    print("=" * 70)

    return result


if __name__ == '__main__':
    run_tests()
