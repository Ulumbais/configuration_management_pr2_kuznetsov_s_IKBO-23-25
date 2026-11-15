"""Консольный анализатор зависимостей Python-пакетов."""

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

def main():
    """Запустить консольное приложение."""
    parser = create_parser()
    args = parser.parse_args()
    try:
        validate_repository(args.repository, args.test_mode)
    except ValueError as error:
        parser.error(str(error))

    print(f"package: {args.package}")
    print(f"repository: {args.repository}")
    print(f"test_mode: {args.test_mode}")
    print(f"ascii_tree: {args.ascii_tree}")


if __name__ == "__main__":
    main()