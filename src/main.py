"""Консольный анализатор зависимостей Python-пакетов."""

from src.graph import (
    depth_first_search, 
    parse_test_graph,
    build_dependency_graph,
    get_install_order,
)

from src.repository import (
    fetch_package_metadata,
    get_direct_dependencies,
)

import argparse
import re
from urllib.parse import urlparse
from pathlib import Path

"""Создать парсер аргументов командной строки."""
def create_parser():
    parser = argparse.ArgumentParser(
        description="Анализ зависимостей Python-пакетов"
    )

    parser.add_argument(
    "--package",
    required=True,
    type=validate_package,
    help="Имя анализируемого Python-пакета"
    )

    parser.add_argument(
    "--repository",
    required=True,
    help="URL репозитория или путь к тестовому файлу"
    )

    parser.add_argument(
        "--test-mode",
        action="store_true",
        help="Использовать тестовый репозиторий"
    )

    parser.add_argument(
        "--ascii-tree",
        action="store_true",
        help="Вывести зависимости в формате ASCII-дерева"
    )

    return parser

def validate_package(package):
    """Проверить имя анализируемого пакета."""
    if not package.strip():
        raise ValueError("Имя пакета не может быть пустым")

    if not re.fullmatch(r"[A-Za-z0-9](?:[A-Za-z0-9._-]*[A-Za-z0-9])?", package):
        raise ValueError("Недопустимое имя пакета")

    return package

def validate_url(url):
    """Проверить корректность URL репозитория."""
    parsed = urlparse(url)

    if parsed.scheme not in ("http", "https"):
        raise ValueError("URL должен использовать HTTP или HTTPS")

    if not parsed.netloc:
        raise ValueError("URL должен содержать имя сервера")

    return url

def validate_file(file_path):
    """Проверить путь к тестовому файлу."""
    path = Path(file_path)

    if not path.is_file():
        raise ValueError("Тестовый файл не найден")

    return file_path

def validate_repository(repository, test_mode):
    """Проверить репозиторий с учётом режима работы."""
    if test_mode:
        return validate_file(repository)

    return validate_url(repository)

def show_dependencies(package, repository):
    """Получить и вывести прямые зависимости пакета."""
    metadata = fetch_package_metadata(package, repository)
    dependencies = get_direct_dependencies(metadata)

    print(f"Прямые зависимости пакета {package}:")

    if not dependencies:
        print("Зависимости отсутствуют")
        return

    for dependency in dependencies:
        print(f"- {dependency}")

def show_test_graph(package, repository):
    """Прочитать тестовый граф и выполнить обход DFS."""
    content = Path(repository).read_text(encoding="utf-8")
    graph = parse_test_graph(content)

    result, cycles = depth_first_search(graph, package)

    print("Порядок обхода:", " -> ".join(result))

    if cycles:
        print("Обнаружены циклы:", ", ".join(cycles))
    else:
        print("Циклы не обнаружены")

def show_full_graph(package, repository):
    """Построить и вывести полный граф зависимостей."""
    graph = build_dependency_graph(package, repository)
    result, cycles = depth_first_search(graph, package)

    print(f"Граф зависимостей пакета {package}:")

    for name in result:
        dependencies = graph.get(name, [])
        print(f"{name}: {', '.join(dependencies) or 'нет'}")

    if cycles:
        print("Обнаружены циклы:", ", ".join(cycles))
    else:
        print("Циклы не обнаружены")

def show_install_order(package, repository, test_mode):
    """Вывести порядок установки пакетов."""
    if test_mode:
        content = Path(repository).read_text(encoding="utf-8")
        graph = parse_test_graph(content)
    else:
        graph = build_dependency_graph(package, repository)

    order = get_install_order(graph, package)

    print(f"Порядок установки для {package}:")

    for number, name in enumerate(order, 1):
        print(f"{number}. {name}")

def main():
    """Запустить консольное приложение."""
    parser = create_parser()
    args = parser.parse_args()

    try:
        validate_repository(args.repository, args.test_mode)

        show_install_order(
            args.package,
            args.repository,
            args.test_mode,
        )

    except (ValueError, OSError) as error:
        parser.error(str(error))

if __name__ == "__main__":
    main()