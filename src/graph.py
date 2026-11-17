"""Построение графа зависимостей пакетов."""

from src.repository import (
    extract_dependency_names,
    fetch_package_metadata,
    get_direct_dependencies,
)

def parse_test_graph(content):
    """Преобразовать текстовый граф в словарь зависимостей."""
    graph = {}

    for line in content.splitlines():
        line = line.strip()

        if not line:
            continue

        package, dependencies = line.split(":", 1)
        graph[package.strip()] = dependencies.split()

    return graph


def depth_first_search(graph, start):
    """Обойти граф зависимостей поиском в глубину."""
    visited = set()
    active = set()
    result = []
    cycles = []

    def visit(package):
        """Рекурсивно посетить пакет и его зависимости."""
        if package in active:
            cycles.append(package)
            return

        if package in visited:
            return

        active.add(package)
        result.append(package)

        for dependency in graph.get(package, []):
            visit(dependency)

        active.remove(package)
        visited.add(package)

    visit(start)
    return result, cycles


def build_dependency_graph(package, repository, max_packages=50):
    """Рекурсивно построить граф зависимостей из PyPI."""
    graph = {}

    def collect(name):
        """Получить зависимости пакета и обработать дочерние узлы."""
        if name in graph:
            return

        if len(graph) >= max_packages:
            raise ValueError("Превышен лимит пакетов в графе")

        metadata = fetch_package_metadata(name, repository)
        dependencies = get_direct_dependencies(metadata)
        names = extract_dependency_names(dependencies)

        graph[name] = names

        for dependency in names:
            collect(dependency)

    collect(package)
    return graph
