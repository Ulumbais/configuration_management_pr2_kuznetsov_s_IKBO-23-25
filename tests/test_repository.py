"""Тесты получения метаданных Python-пакетов."""

import unittest
from unittest.mock import patch

from src.repository import (
    fetch_package_metadata,
    get_direct_dependencies,
)

import io
import json

from urllib.error import HTTPError

class TestRepository(unittest.TestCase):
    """Проверки работы с репозиторием пакетов."""

    def test_direct_dependencies(self):
        """Извлечь прямые зависимости из метаданных."""
        metadata = {
            "info": {
                "requires_dist": ["requests>=2", "numpy>=1"]
            }
        }

        result = get_direct_dependencies(metadata)

        self.assertEqual(result, ["requests>=2", "numpy>=1"])

    def test_no_dependencies(self):
        """Вернуть пустой список при отсутствии зависимостей."""
        metadata = {"info": {"requires_dist": None}}

        result = get_direct_dependencies(metadata)

        self.assertEqual(result, [])

    def test_fetch_metadata(self):
        """Получить метаданные из подменённого HTTP-ответа."""
        metadata = {
            "info": {
                "name": "requests",
                "requires_dist": ["urllib3>=1.26"],
            }
        }
        response = io.BytesIO(json.dumps(metadata).encode("utf-8"))

        with patch("src.repository.urlopen", return_value=response):
            result = fetch_package_metadata(
                "requests", "https://pypi.org/pypi"
            )

        self.assertEqual(result, metadata)

    def test_package_not_found(self):
        """Сообщить об отсутствии пакета в репозитории."""
        error = HTTPError(
            "https://pypi.org/pypi/missing/json",
            404,
            "Not Found",
            None,
            None,
        )

        with patch("src.repository.urlopen", side_effect=error):
            with self.assertRaisesRegex(
                ValueError, "Пакет не найден"
            ):
                fetch_package_metadata(
                    "missing", "https://pypi.org/pypi"
                )