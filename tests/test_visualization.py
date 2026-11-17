
"""Тесты визуализации графа зависимостей."""

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from src.visualization import (
    generate_ascii_tree,
    generate_plantuml,
    render_png,
    save_plantuml,
)


class TestVisualization(unittest.TestCase):
    """Проверки PlantUML, ASCII и генерации PNG."""

    def setUp(self):
        """Подготовить тестовый граф."""
        self.graph = {
            "A": ["B", "C"],
            "B": ["D"],
            "C": ["D"],
            "D": [],
        }

    def test_generate_plantuml(self):
        """Проверить вершины и связи PlantUML."""
        result = generate_plantuml(self.graph)

        self.assertIn("@startuml", result)
        self.assertIn('rectangle "A" as p0', result)
        self.assertIn("p0 --> p1", result)
        self.assertIn("p2 --> p3", result)
        self.assertIn("@enduml", result)

    def test_ascii_tree(self):
        """Проверить ASCII-дерево с повторной вершиной."""
        result = generate_ascii_tree(self.graph, "A")

        self.assertIn("|-- B", result)
        self.assertIn("`-- C", result)
        self.assertIn("D (повтор)", result)

    def test_save_plantuml(self):
        """Проверить сохранение диаграммы во временный файл."""
        with TemporaryDirectory() as folder:
            path = Path(folder) / "graph.puml"
            result = save_plantuml(self.graph, path)

            self.assertEqual(result, path)
            self.assertTrue(path.is_file())
            self.assertIn("@startuml", path.read_text("utf-8"))

    def test_render_png(self):
        """Проверить команду рендеринга без запуска Java."""
        with patch("src.visualization.subprocess.run") as run:
            result = render_png("graph.puml", "plantuml.jar")

        run.assert_called_once()
        command = run.call_args.args[0]

        self.assertEqual(
            command,
            ["java", "-jar", "plantuml.jar", "-tpng", "graph.puml"],
        )
        self.assertEqual(result, Path("graph.png"))
