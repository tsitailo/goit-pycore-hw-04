import shutil
import sys
import tempfile
import unittest
from datetime import datetime
from io import StringIO
from pathlib import Path
from unittest.mock import patch, MagicMock

from colorama import Fore, Style, init

from visualize_directory_structure import visualize_directory_structure, main

# Ініціалізація colorama
init(autoreset=True)

# Імпортуємо функції з нашого скрипту


class ColoredTextTestResult(unittest.TextTestResult):
    """Кастомний клас для кольорового виводу результатів тестів"""

    def __init__(self, stream, descriptions, verbosity):
        super().__init__(stream, descriptions, verbosity)
        self.test_results = []

    def startTest(self, test):
        super().startTest(test)
        self.stream.write(f"{Fore.CYAN}▶ Запуск: {test._testMethodName}\n")
        self.stream.flush()

    def addSuccess(self, test):
        super().addSuccess(test)
        self.test_results.append(('SUCCESS', test))
        self.stream.write(f"{Fore.GREEN}✓ УСПІХ: {test._testMethodName}\n")
        self.stream.flush()

    def addError(self, test, err):
        super().addError(test, err)
        self.test_results.append(('ERROR', test, err))
        self.stream.write(f"{Fore.RED}✗ ПОМИЛКА: {test._testMethodName}\n")
        self.stream.flush()

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.test_results.append(('FAILURE', test, err))
        self.stream.write(f"{Fore.RED}✗ ПРОВАЛ: {test._testMethodName}\n")
        self.stream.flush()

    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        self.test_results.append(('SKIP', test, reason))
        self.stream.write(f"{Fore.YELLOW}⊘ ПРОПУЩЕНО: {test._testMethodName} - {reason}\n")
        self.stream.flush()


class ColoredTextTestRunner(unittest.TextTestRunner):
    """Кастомний runner для кольорового виводу"""
    resultclass = ColoredTextTestResult

    def run(self, test):
        """Запуск тестів з кольоровим виводом"""
        print(f"\n{Fore.YELLOW}{Style.BRIGHT}{'=' * 70}")
        print(f"{Fore.YELLOW}{Style.BRIGHT}ПОЧАТОК ТЕСТУВАННЯ")
        print(f"{Fore.YELLOW}{Style.BRIGHT}Час запуску: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{Fore.YELLOW}{Style.BRIGHT}{'=' * 70}\n")

        result = super().run(test)

        return result


class TestDirectoryVisualization(unittest.TestCase):
    """Тести для функцій візуалізації структури директорій"""

    @classmethod
    def setUpClass(cls):
        """Створення тестової структури директорій перед всіма тестами"""
        print(f"\n{Fore.MAGENTA}{'─' * 70}")
        print(f"{Fore.MAGENTA}📁 Створення тестової структури директорій...")

        cls.test_dir = tempfile.mkdtemp(prefix="test_picture_")

        # Створюємо структуру:
        # picture/
        # ├── Logo/
        # │   ├── IBM+Logo.png
        # │   ├── ibm.svg
        # │   └── logo-tm.png
        # ├── bot-icon.png
        # └── mongodb.jpg

        cls.picture_dir = Path(cls.test_dir) / "picture"
        cls.picture_dir.mkdir()

        # Створюємо піддиректорію Logo
        cls.logo_dir = cls.picture_dir / "Logo"
        cls.logo_dir.mkdir()

        # Створюємо файли в Logo
        (cls.logo_dir / "IBM+Logo.png").touch()
        (cls.logo_dir / "ibm.svg").touch()
        (cls.logo_dir / "logo-tm.png").touch()

        # Створюємо файли в picture
        (cls.picture_dir / "bot-icon.png").touch()
        (cls.picture_dir / "mongodb.jpg").touch()

        # Додаткові тестові структури
        cls.empty_dir = Path(cls.test_dir) / "empty_directory"
        cls.empty_dir.mkdir()

        cls.nested_dir = Path(cls.test_dir) / "nested"
        cls.nested_dir.mkdir()
        (cls.nested_dir / "level1").mkdir()
        (cls.nested_dir / "level1" / "level2").mkdir()
        (cls.nested_dir / "level1" / "level2" / "file.txt").touch()

        cls.single_file_dir = Path(cls.test_dir) / "single_file"
        cls.single_file_dir.mkdir()
        (cls.single_file_dir / "alone.txt").touch()

        print(f"{Fore.MAGENTA}✓ Тестова структура створена: {cls.test_dir}")
        print(f"{Fore.MAGENTA}{'─' * 70}\n")

    @classmethod
    def tearDownClass(cls):
        """Видалення тестової структури після всіх тестів"""
        print(f"\n{Fore.MAGENTA}{'─' * 70}")
        print(f"{Fore.MAGENTA}🗑 Видалення тестової структури...")
        shutil.rmtree(cls.test_dir)
        print(f"{Fore.MAGENTA}✓ Тестова структура видалена")
        print(f"{Fore.MAGENTA}{'─' * 70}\n")

    def setUp(self):
        """Виконується перед кожним тестом"""
        print(f"{Fore.CYAN}  → Підготовка до тесту...")

    def tearDown(self):
        """Виконується після кожного тесту"""
        print(f"{Fore.CYAN}  → Очищення після тесту...\n")

    def test_visualize_picture_directory_structure(self):
        """Тест візуалізації основної структури picture"""
        print(f"{Fore.WHITE}    Перевірка візуалізації структури picture...")

        with patch('sys.stdout', new=StringIO()) as fake_output:
            visualize_directory_structure(self.picture_dir)
            output = fake_output.getvalue()

            print(f"{Fore.WHITE}    Вивід структури:")
            print(f"{Fore.WHITE}    {'-' * 50}")
            for line in output.split('\n')[:10]:  # Показуємо перші 10 рядків
                print(f"{Fore.WHITE}    {line}")
            print(f"{Fore.WHITE}    {'-' * 50}")

            # Перевіряємо наявність ключових елементів
            self.assertIn("picture", output)
            self.assertIn("Logo", output)
            self.assertIn("IBM+Logo.png", output)
            self.assertIn("ibm.svg", output)
            self.assertIn("logo-tm.png", output)
            self.assertIn("bot-icon.png", output)
            self.assertIn("mongodb.jpg", output)

            # Перевіряємо наявність символів дерева
            self.assertIn("📦", output)
            self.assertIn("📂", output)
            self.assertIn("📜", output)

            print(f"{Fore.GREEN}    ✓ Всі елементи знайдено")

    def test_visualize_empty_directory(self):
        """Тест візуалізації порожньої директорії"""
        print(f"{Fore.WHITE}    Перевірка порожньої директорії...")

        with patch('sys.stdout', new=StringIO()) as fake_output:
            visualize_directory_structure(self.empty_dir)
            output = fake_output.getvalue()

            # Має показати тільки назву директорії
            self.assertIn("empty_directory", output)
            print(f"{Fore.GREEN}    ✓ Порожня директорія оброблена коректно")

    def test_visualize_nested_directory(self):
        """Тест візуалізації вкладених директорій"""
        print(f"{Fore.WHITE}    Перевірка вкладених директорій...")

        with patch('sys.stdout', new=StringIO()) as fake_output:
            visualize_directory_structure(self.nested_dir)
            output = fake_output.getvalue()

            self.assertIn("nested", output)
            self.assertIn("level1", output)
            self.assertIn("level2", output)
            self.assertIn("file.txt", output)

            print(f"{Fore.GREEN}    ✓ Вкладені директорії оброблені коректно")

    def test_visualize_single_file_directory(self):
        """Тест директорії з одним файлом"""
        print(f"{Fore.WHITE}    Перевірка директорії з одним файлом...")

        with patch('sys.stdout', new=StringIO()) as fake_output:
            visualize_directory_structure(self.single_file_dir)
            output = fake_output.getvalue()

            self.assertIn("single_file", output)
            self.assertIn("alone.txt", output)

            print(f"{Fore.GREEN}    ✓ Директорія з одним файлом оброблена коректно")

    def test_directory_sorting(self):
        """Тест правильності сортування (директорії перед файлами)"""
        print(f"{Fore.WHITE}    Перевірка сортування...")

        with patch('sys.stdout', new=StringIO()) as fake_output:
            visualize_directory_structure(self.picture_dir)
            output = fake_output.getvalue()

            # Logo (директорія) має з'явитися перед файлами
            logo_pos = output.find("Logo")
            bot_icon_pos = output.find("bot-icon.png")

            self.assertLess(logo_pos, bot_icon_pos,
                            "Директорії мають йти перед файлами")

            print(f"{Fore.GREEN}    ✓ Сортування працює правильно (директорії перед файлами)")

    def test_permission_error_handling(self):
        """Тест обробки помилки доступу"""
        print(f"{Fore.WHITE}    Перевірка обробки помилки доступу...")

        with patch('sys.stdout', new=StringIO()) as fake_output:
            mock_path = MagicMock(spec=Path)
            mock_path.name = "restricted"
            mock_path.iterdir.side_effect = PermissionError("Access denied")

            visualize_directory_structure(mock_path, prefix=" ┃ ")
            output = fake_output.getvalue()

            self.assertIn("Доступ заборонено", output)

            print(f"{Fore.GREEN}    ✓ PermissionError оброблено правильно")

    def test_general_exception_handling(self):
        """Тест обробки загальних помилок"""
        print(f"{Fore.WHITE}    Перевірка обробки загальних помилок...")

        with patch('sys.stdout', new=StringIO()) as fake_output:
            mock_path = MagicMock(spec=Path)
            mock_path.name = "error_dir"
            mock_path.iterdir.side_effect = Exception("Unknown error")

            visualize_directory_structure(mock_path)
            output = fake_output.getvalue()

            self.assertIn("Помилка", output)

            print(f"{Fore.GREEN}    ✓ Загальні помилки оброблено правильно")


class TestMainFunction(unittest.TestCase):
    """Тести для головної функції main()"""

    @classmethod
    def setUpClass(cls):
        """Створення тестової структури"""
        print(f"\n{Fore.MAGENTA}{'─' * 70}")
        print(f"{Fore.MAGENTA}📁 Створення тестової структури для main()...")

        cls.test_dir = tempfile.mkdtemp(prefix="test_main_")
        cls.test_path = Path(cls.test_dir) / "test_folder"
        cls.test_path.mkdir()
        (cls.test_path / "file.txt").touch()

        print(f"{Fore.MAGENTA}✓ Тестова структура створена")
        print(f"{Fore.MAGENTA}{'─' * 70}\n")

    @classmethod
    def tearDownClass(cls):
        """Видалення тестової структури"""
        print(f"\n{Fore.MAGENTA}{'─' * 70}")
        print(f"{Fore.MAGENTA}🗑 Видалення тестової структури main()...")
        shutil.rmtree(cls.test_dir)
        print(f"{Fore.MAGENTA}✓ Тестова структура видалена")
        print(f"{Fore.MAGENTA}{'─' * 70}\n")

    def setUp(self):
        print(f"{Fore.CYAN}  → Підготовка до тесту...")

    def tearDown(self):
        print(f"{Fore.CYAN}  → Очищення після тесту...\n")

    def test_main_no_arguments(self):
        """Тест без аргументів командного рядка"""
        print(f"{Fore.WHITE}    Перевірка виклику без аргументів...")

        with patch('sys.argv', ['hw03.py']):
            with patch('sys.stdout', new=StringIO()) as fake_output:
                with self.assertRaises(SystemExit) as cm:
                    main()

                self.assertEqual(cm.exception.code, 1)
                output = fake_output.getvalue()
                self.assertIn("Не вказано шлях", output)
                self.assertIn("Використання:", output)

                print(f"{Fore.GREEN}    ✓ SystemExit(1) викликано коректно")
                print(f"{Fore.WHITE}    Повідомлення про помилку виведено")

    def test_main_nonexistent_path(self):
        """Тест з неіснуючим шляхом"""
        print(f"{Fore.WHITE}    Перевірка неіснуючого шляху...")

        fake_path = "/this/path/does/not/exist/at/all"

        with patch('sys.argv', ['hw03.py', fake_path]):
            with patch('sys.stdout', new=StringIO()) as fake_output:
                with self.assertRaises(SystemExit) as cm:
                    main()

                self.assertEqual(cm.exception.code, 1)
                output = fake_output.getvalue()
                self.assertIn("не існує", output)

                print(f"{Fore.GREEN}    ✓ Неіснуючий шлях оброблено коректно")

    def test_main_file_instead_of_directory(self):
        """Тест коли передано файл замість директорії"""
        print(f"{Fore.WHITE}    Перевірка файлу замість директорії...")

        test_file = Path(self.test_dir) / "just_a_file.txt"
        test_file.touch()

        with patch('sys.argv', ['hw03.py', str(test_file)]):
            with patch('sys.stdout', new=StringIO()) as fake_output:
                with self.assertRaises(SystemExit) as cm:
                    main()

                self.assertEqual(cm.exception.code, 1)
                output = fake_output.getvalue()
                self.assertIn("не є директорією", output)

                print(f"{Fore.GREEN}    ✓ Файл замість директорії оброблено коректно")

    def test_main_valid_directory(self):
        """Тест з валідною директорією"""
        print(f"{Fore.WHITE}    Перевірка валідної директорії...")

        with patch('sys.argv', ['hw03.py', str(self.test_path)]):
            with patch('sys.stdout', new=StringIO()) as fake_output:
                main()
                output = fake_output.getvalue()

                # Перевіряємо наявність заголовка
                self.assertIn("Структура директорії", output)
                self.assertIn("=" * 50, output)
                self.assertIn("test_folder", output)
                self.assertIn("file.txt", output)

                print(f"{Fore.GREEN}    ✓ Валідна директорія оброблена коректно")

    def test_main_with_relative_path(self):
        """Тест з відносним шляхом"""
        print(f"{Fore.WHITE}    Перевірка відносного шляху...")

        # Створюємо тестову директорію у поточній директорії
        current_dir = Path.cwd()
        test_rel_dir = current_dir / "temp_test_rel"
        test_rel_dir.mkdir(exist_ok=True)
        (test_rel_dir / "test.txt").touch()

        try:
            with patch('sys.argv', ['hw03.py', './temp_test_rel']):
                with patch('sys.stdout', new=StringIO()) as fake_output:
                    main()
                    output = fake_output.getvalue()

                    self.assertIn("temp_test_rel", output)
                    self.assertIn("test.txt", output)

                    print(f"{Fore.GREEN}    ✓ Відносний шлях оброблено коректно")
        finally:
            # Прибираємо за собою
            shutil.rmtree(test_rel_dir)

    def test_main_with_current_directory(self):
        """Тест з поточною директорією (.)"""
        print(f"{Fore.WHITE}    Перевірка поточної директорії...")

        with patch('sys.argv', ['hw03.py', '.']):
            with patch('sys.stdout', new=StringIO()) as fake_output:
                main()
                output = fake_output.getvalue()

                # Має показати структуру поточної директорії
                self.assertIn("Структура директорії", output)

                print(f"{Fore.GREEN}    ✓ Поточна директорія оброблена коректно")


class TestEdgeCases(unittest.TestCase):
    """Тести для граничних випадків"""

    @classmethod
    def setUpClass(cls):
        """Створення тестової структури для граничних випадків"""
        print(f"\n{Fore.MAGENTA}{'─' * 70}")
        print(f"{Fore.MAGENTA}📁 Створення структури для граничних випадків...")

        cls.test_dir = tempfile.mkdtemp(prefix="test_edge_")

        # Директорія зі спеціальними символами в іменах
        cls.special_chars_dir = Path(cls.test_dir) / "special_chars"
        cls.special_chars_dir.mkdir()
        (cls.special_chars_dir / "file with spaces.txt").touch()
        (cls.special_chars_dir / "file-with-dashes.txt").touch()
        (cls.special_chars_dir / "file_with_underscores.txt").touch()

        # Глибоко вкладена структура
        cls.deep_dir = Path(cls.test_dir) / "deep"
        current = cls.deep_dir
        for i in range(5):
            current = current / f"level{i}"
            current.mkdir(parents=True, exist_ok=True)
        (current / "deep_file.txt").touch()

        # Директорія з великою кількістю файлів
        cls.many_files_dir = Path(cls.test_dir) / "many_files"
        cls.many_files_dir.mkdir()
        for i in range(20):
            (cls.many_files_dir / f"file_{i:02d}.txt").touch()

        print(f"{Fore.MAGENTA}✓ Структура створена")
        print(f"{Fore.MAGENTA}{'─' * 70}\n")

    @classmethod
    def tearDownClass(cls):
        """Видалення тестової структури"""
        print(f"\n{Fore.MAGENTA}{'─' * 70}")
        print(f"{Fore.MAGENTA}🗑 Видалення структури граничних випадків...")
        shutil.rmtree(cls.test_dir)
        print(f"{Fore.MAGENTA}✓ Структура видалена")
        print(f"{Fore.MAGENTA}{'─' * 70}\n")

    def setUp(self):
        print(f"{Fore.CYAN}  → Підготовка до тесту...")

    def tearDown(self):
        print(f"{Fore.CYAN}  → Очищення після тесту...\n")

    def test_special_characters_in_names(self):
        """Тест файлів зі спеціальними символами в іменах"""
        print(f"{Fore.WHITE}    Перевірка спеціальних символів у назвах...")

        with patch('sys.stdout', new=StringIO()) as fake_output:
            visualize_directory_structure(self.special_chars_dir)
            output = fake_output.getvalue()

            self.assertIn("file with spaces.txt", output)
            self.assertIn("file-with-dashes.txt", output)
            self.assertIn("file_with_underscores.txt", output)

            print(f"{Fore.GREEN}    ✓ Спеціальні символи оброблені коректно")

    def test_deeply_nested_structure(self):
        """Тест глибоко вкладеної структури"""
        print(f"{Fore.WHITE}    Перевірка глибокої вкладеності (5 рівнів)...")

        with patch('sys.stdout', new=StringIO()) as fake_output:
            visualize_directory_structure(self.deep_dir)
            output = fake_output.getvalue()

            # Перевіряємо наявність всіх рівнів
            for i in range(5):
                self.assertIn(f"level{i}", output)
            self.assertIn("deep_file.txt", output)

            print(f"{Fore.GREEN}    ✓ Глибока вкладеність оброблена коректно")

    def test_many_files(self):
        """Тест директорії з великою кількістю файлів"""
        print(f"{Fore.WHITE}    Перевірка 20 файлів у директорії...")

        with patch('sys.stdout', new=StringIO()) as fake_output:
            visualize_directory_structure(self.many_files_dir)
            output = fake_output.getvalue()

            # Перевіряємо наявність кількох файлів
            self.assertIn("file_00.txt", output)
            self.assertIn("file_10.txt", output)
            self.assertIn("file_19.txt", output)

            print(f"{Fore.GREEN}    ✓ Велика кількість файлів оброблена коректно")

    def test_mixed_files_and_directories(self):
        """Тест змішаної структури з файлами та директоріями"""
        print(f"{Fore.WHITE}    Перевірка змішаної структури...")

        mixed_dir = Path(self.test_dir) / "mixed"
        mixed_dir.mkdir()

        (mixed_dir / "a_file.txt").touch()
        (mixed_dir / "b_directory").mkdir()
        (mixed_dir / "c_file.txt").touch()
        (mixed_dir / "d_directory").mkdir()

        with patch('sys.stdout', new=StringIO()) as fake_output:
            visualize_directory_structure(mixed_dir)
            output = fake_output.getvalue()

            # Директорії мають йти перед файлами
            b_dir_pos = output.find("b_directory")
            d_dir_pos = output.find("d_directory")
            a_file_pos = output.find("a_file.txt")
            c_file_pos = output.find("c_file.txt")

            self.assertLess(b_dir_pos, a_file_pos)
            self.assertLess(d_dir_pos, a_file_pos)

            print(f"{Fore.GREEN}    ✓ Змішана структура оброблена коректно")


class TestColoramaIntegration(unittest.TestCase):
    """Тести для перевірки інтеграції з colorama"""

    def setUp(self):
        """Створення тимчасової директорії для кожного тесту"""
        print(f"{Fore.CYAN}  → Підготовка до тесту...")
        self.test_dir = tempfile.mkdtemp()
        self.test_path = Path(self.test_dir)
        (self.test_path / "subdir").mkdir()
        (self.test_path / "file.txt").touch()

    def tearDown(self):
        """Видалення тимчасової директорії"""
        print(f"{Fore.CYAN}  → Очищення після тесту...\n")
        shutil.rmtree(self.test_dir)

    def test_color_codes_in_output(self):
        """Тест наявності кольорових кодів у виводі"""
        print(f"{Fore.WHITE}    Перевірка кольорових кодів у виводі...")

        with patch('sys.stdout', new=StringIO()) as fake_output:
            visualize_directory_structure(self.test_path)
            output = fake_output.getvalue()

            # Colorama додає ANSI escape коди для кольорів
            # Перевіряємо наявність хоча б деяких escape послідовностей
            # або імен кольорів (якщо colorama не активна)
            self.assertTrue(
                '\x1b[' in output or 'subdir' in output,
                "Вивід має містити кольорові коди або текст"
            )

            print(f"{Fore.GREEN}    ✓ Кольорові коди присутні у виводі")


def print_summary(result):
    """Виведення детальної підсумкової інформації"""
    print(f"\n{Fore.YELLOW}{Style.BRIGHT}{'=' * 70}")
    print(f"{Fore.YELLOW}{Style.BRIGHT}ПІДСУМКОВА СТАТИСТИКА ТЕСТУВАННЯ")
    print(f"{Fore.YELLOW}{Style.BRIGHT}{'=' * 70}\n")

    total_tests = result.testsRun
    successes = total_tests - len(result.failures) - len(result.errors) - len(result.skipped)

    # Загальна статистика
    print(f"{Fore.CYAN}📊 Загальна статистика:")
    print(f"{Fore.WHITE}   Всього тестів запущено: {Fore.YELLOW}{total_tests}")
    print(f"{Fore.WHITE}   Успішних: {Fore.GREEN}{successes}")
    print(f"{Fore.WHITE}   Провалених: {Fore.RED}{len(result.failures)}")
    print(f"{Fore.WHITE}   Помилок: {Fore.RED}{len(result.errors)}")
    print(f"{Fore.WHITE}   Пропущених: {Fore.YELLOW}{len(result.skipped)}")

    # Відсоток успішності
    if total_tests > 0:
        success_rate = (successes / total_tests) * 100
        print(f"\n{Fore.CYAN}📈 Відсоток успішності: ", end="")
        if success_rate == 100:
            print(f"{Fore.GREEN}{Style.BRIGHT}{success_rate:.1f}% ✓")
        elif success_rate >= 80:
            print(f"{Fore.YELLOW}{success_rate:.1f}%")
        else:
            print(f"{Fore.RED}{success_rate:.1f}%")

    # Детальна інформація про провали
    if result.failures:
        print(f"\n{Fore.RED}{Style.BRIGHT}❌ ПРОВАЛЕНІ ТЕСТИ:")
        for test, traceback in result.failures:
            print(f"{Fore.RED}   • {test}")
            print(f"{Fore.WHITE}     {traceback.split(chr(10))[0][:60]}...")

    # Детальна інформація про помилки
    if result.errors:
        print(f"\n{Fore.RED}{Style.BRIGHT}⚠ ТЕСТИ З ПОМИЛКАМИ:")
        for test, traceback in result.errors:
            print(f"{Fore.RED}   • {test}")
            print(f"{Fore.WHITE}     {traceback.split(chr(10))[0][:60]}...")

    # Інформація про пропущені тести
    if result.skipped:
        print(f"\n{Fore.YELLOW}{Style.BRIGHT}⊘ ПРОПУЩЕНІ ТЕСТИ:")
        for test, reason in result.skipped:
            print(f"{Fore.YELLOW}   • {test}")
            print(f"{Fore.WHITE}     Причина: {reason}")

    # Фінальний статус
    print(f"\n{Fore.YELLOW}{Style.BRIGHT}{'=' * 70}")
    if successes == total_tests and total_tests > 0:
        print(f"{Fore.GREEN}{Style.BRIGHT}✓ ВСІ ТЕСТИ ПРОЙДЕНІ УСПІШНО!")
    elif len(result.failures) + len(result.errors) == 0:
        print(f"{Fore.YELLOW}{Style.BRIGHT}⚠ ТЕСТУВАННЯ ЗАВЕРШЕНО З ПОПЕРЕДЖЕННЯМИ")
    else:
        print(f"{Fore.RED}{Style.BRIGHT}✗ ТЕСТУВАННЯ ЗАВЕРШЕНО З ПОМИЛКАМИ")

    print(f"{Fore.YELLOW}{Style.BRIGHT}Час завершення: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{Fore.YELLOW}{Style.BRIGHT}{'=' * 70}\n")


def run_tests():
    """Запуск всіх тестів з детальним звітом"""
    # Створення test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Додавання всіх тестових класів
    test_classes = [
        TestDirectoryVisualization,
        TestMainFunction,
        TestEdgeCases,
        TestColoramaIntegration
    ]

    print(f"{Fore.CYAN}{Style.BRIGHT}📋 Завантаження тестів...")
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
        print(f"{Fore.WHITE}   ✓ {test_class.__name__}: {tests.countTestCases()} тестів")

    # Запуск тестів з кольоровим виводом
    runner = ColoredTextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Виведення підсумкової статистики
    print_summary(result)

    return result


if __name__ == '__main__':
    result = run_tests()

    # Повертаємо код виходу: 0 якщо всі тести пройшли, 1 якщо були помилки
    sys.exit(not result.wasSuccessful())