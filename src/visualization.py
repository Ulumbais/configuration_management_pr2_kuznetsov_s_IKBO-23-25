"""Визуализация графа зависимостей через PlantUML."""

from pathlib import Path
import os
import subprocess


def generate_plantuml(graph):
    """Преобразовать граф зависимостей в PlantUML."""
    lines = ["@startuml", "left to right direction", "scale 4"]
    names = list(dict.fromkeys(
        list(graph) + [
            dependency
            for dependencies in graph.values()
            for dependency in dependencies
        ]
    ))
    identifiers = {
        name: f"p{index}"
        for index, name in enumerate(names)
    }

    for name in names:
        label = name.replace('"', '\\"')
        lines.append(
            f'rectangle "{label}" as {identifiers[name]}'
        )

    for name, dependencies in graph.items():
        for dependency in dependencies:
            lines.append(
                f"{identifiers[name]} --> {identifiers[dependency]}"
            )

    lines.append("@enduml")
    return "\n".join(lines)


def save_plantuml(graph, output_path):
    """Сохранить описание графа в формате PlantUML."""
    path = Path(output_path)

    path.parent.mkdir(parents=True, exist_ok=True)

    content = generate_plantuml(graph)
    path.write_text(content, encoding="utf-8")

    return path


def render_png(plantuml_path, jar_path):
    """Создать PNG-изображение через PlantUML."""
    command = [
        "java",
        "-jar",
        str(jar_path),
        "-tpng",
        str(plantuml_path),
    ]

    subprocess.run(
        command,
        check=True,
        text=True,
    )

    return Path(plantuml_path).with_suffix(".png")


def open_image(image_path):
    """Открыть изображение стандартным приложением Windows."""
    os.startfile(str(Path(image_path).resolve()))


def generate_ascii_tree(graph, start):
    """Построить текстовое дерево зависимостей."""
    lines = [start]
    visited = {start}

    def visit(package, prefix):
        """Рекурсивно вывести зависимости пакета."""
        dependencies = graph.get(package, [])

        for index, dependency in enumerate(dependencies):
            last = index == len(dependencies) - 1
            branch = "`-- " if last else "|-- "
            repeated = dependency in visited

            label = dependency + (" (повтор)" if repeated else "")
            lines.append(prefix + branch + label)

            if not repeated:
                visited.add(dependency)
                extension = "    " if last else "|   "
                visit(dependency, prefix + extension)

    visit(start, "")
    return "\n".join(lines)
