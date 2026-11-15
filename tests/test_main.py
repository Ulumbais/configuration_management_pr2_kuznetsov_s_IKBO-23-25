"""Тесты обработки аргументов командной строки."""

import unittest

from src.main import (
    validate_file,
    validate_package,
    validate_url,
    create_parser
)

class TestPackageValidation(unittest.TestCase):
    """Проверки имени анализируемого пакета."""

    def test_valid_package(self):
        """Корректное имя пакета принимается."""
        result = validate_package("requests")
        self.assertEqual(result, "requests")

    def test_empty_package(self):
        """Пустое имя пакета должно вызывать ValueError."""
        with self.assertRaises(ValueError):
            validate_package("   ")

    def test_invalid_package(self):
        """Отклонить имя с недопустимыми символами."""
        with self.assertRaises(ValueError):
            validate_package("requests!!!")

class TestRepositoryValidation(unittest.TestCase):
    """Проверки адреса репозитория и пути к файлу."""

    def test_invalid_url(self):
        """Отклонить неподдерживаемый протокол."""
        with self.assertRaises(ValueError):
            validate_url("ftp://example.com")

    def test_missing_file(self):
        """Отклонить путь к отсутствующему файлу."""
        with self.assertRaises(ValueError):
            validate_file("missing_graph_12345.txt")

    def test_valid_url(self):
        """Принять корректный URL репозитория."""
        url = "https://pypi.org/pypi"
        result = validate_url(url)
        self.assertEqual(result, url)

    def test_existing_file(self):
        """Принять путь к существующему тестовому файлу."""
        from pathlib import Path

        file_path = Path(__file__).parent / "graph.txt"
        result = validate_file(str(file_path))

        self.assertEqual(result, str(file_path))

class TestArgumentParser(unittest.TestCase):
    """Проверки аргументов командной строки."""

    def test_required_arguments(self):
        """Проверить обязательность имени пакета."""
        parser = create_parser()

        with self.assertRaises(SystemExit):
            parser.parse_args([
                "--repository",
                "https://pypi.org/pypi",
            ])
    def test_boolean_flags(self):
        """Проверить включение тестового режима и ASCII-дерева."""
        parser = create_parser()

        args = parser.parse_args([
            "--package", "requests",
            "--repository", "https://pypi.org/pypi",
            "--test-mode",
            "--ascii-tree",
        ])

        self.assertTrue(args.test_mode)
        self.assertTrue(args.ascii_tree)