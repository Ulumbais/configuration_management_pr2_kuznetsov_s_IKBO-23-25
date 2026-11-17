"""Тесты построения и обхода графа зависимостей."""

import unittest
from src.graph import (
    depth_first_search,
    parse_test_graph,
    build_dependency_graph,
    get_install_order,
)
from unittest.mock import patch


class TestDependencyGraph(unittest.TestCase):
    """Проверки алгоритма DFS и тестового графа."""

    def test_parse_graph(self):
        """Преобразовать текст в словарь зависимостей."""
        content = "A: B C\nB: D\nC: D\nD:"
        graph = parse_test_graph(content)

        expected = {
            "A": ["B", "C"],
            "B": ["D"],
            "C": ["D"],
            "D": [],
        }

        self.assertEqual(graph, expected)

    def test_dfs_without_cycles(self):
        """Обойти граф без циклических зависимостей."""
        graph = {
            "A": ["B", "C"],
            "B": ["D"],
            "C": ["D"],
            "D": [],
        }

        result, cycles = depth_first_search(graph, "A")

        self.assertEqual(result, ["A", "B", "D", "C"])
        self.assertEqual(cycles, [])

    def test_dfs_with_cycle(self):
        """Обнаружить циклическую зависимость."""
        graph = {
            "A": ["B"],
            "B": ["C"],
            "C": ["A"],
        }

        result, cycles = depth_first_search(graph, "A")

        self.assertEqual(result, ["A", "B", "C"])
        self.assertEqual(cycles, ["A"])

    def test_build_dependency_graph(self):
        """Построить граф с транзитивными зависимостями."""
        metadata = {
            "a": {"info": {"requires_dist": ["B", "C"]}},
            "b": {"info": {"requires_dist": ["D"]}},
            "c": {"info": {"requires_dist": ["D"]}},
            "d": {"info": {"requires_dist": []}},
        }

        def fake_fetch(package, repository):
            """Вернуть тестовые метаданные вместо ответа PyPI."""
            return metadata[package]

        with patch(
            "src.graph.fetch_package_metadata",
            side_effect=fake_fetch,
        ):
            graph = build_dependency_graph(
                "a", "https://pypi.org/pypi"
            )

        expected = {
            "a": ["b", "c"],
            "b": ["d"],
            "d": [],
            "c": ["d"],
        }

        self.assertEqual(graph, expected)

    def test_install_order(self):
        """Проверить порядок загрузки зависимостей."""
        graph = {
            "A": ["B", "C"],
            "B": ["D"],
            "C": ["D"],
            "D": [],
        }

        result = get_install_order(graph, "A")
        self.assertEqual(result, ["D", "B", "C", "A"])

    def test_install_order_single(self):
        """Проверить пакет без зависимостей."""
        result = get_install_order({"A": []}, "A")
        self.assertEqual(result, ["A"])

    def test_install_order_cycle(self):
        """Проверить обнаружение цикла."""
        graph = {
            "A": ["B"],
            "B": ["C"],
            "C": ["A"],
        }

        with self.assertRaisesRegex(
            ValueError, "Циклическая зависимость"
        ):
            get_install_order(graph, "A")

    def test_install_order_missing(self):
        """Проверить отсутствие пакета в графе."""
        graph = {"A": ["B"]}

        with self.assertRaises(ValueError):
            get_install_order(graph, "A")

    def test_shared_dependency(self):
        """Общая зависимость не должна создавать лишнюю вершину."""
        graph = {
            "flask": ["jinja2", "werkzeug"],
            "jinja2": ["markupsafe"],
            "werkzeug": ["markupsafe"],
            "markupsafe": [],
        }

        result, cycles = depth_first_search(graph, "flask")

        self.assertEqual(len(result), 4)
        self.assertEqual(result.count("markupsafe"), 1)
        self.assertEqual(cycles, [])
