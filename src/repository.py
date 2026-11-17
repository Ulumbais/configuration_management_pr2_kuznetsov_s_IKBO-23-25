"""Получение зависимостей Python-пакетов из репозитория."""

from urllib.error import HTTPError, URLError
import json
from urllib.parse import quote
from urllib.request import urlopen
import re


def normalize_package_name(name):
    """Привести имя Python-пакета к стандартному виду."""
    return re.sub(r"[-_.]+", "-", name).lower()


def fetch_package_metadata(package, repository):
    """Получить JSON-метаданные пакета по URL репозитория."""
    package_name = quote(package, safe="")
    url = f"{repository.rstrip('/')}/{package_name}/json"

    try:
        with urlopen(url, timeout=10) as response:
            return json.load(response)
    except HTTPError as error:
        if error.code == 404:
            raise ValueError("Пакет не найден в репозитории") from error
        raise ValueError(f"Ошибка HTTP: {error.code}") from error
    except (URLError, TimeoutError) as error:
        raise ValueError("Не удалось подключиться к репозиторию") from error


def get_direct_dependencies(metadata):
    """Получить список прямых зависимостей из метаданных."""
    dependencies = metadata["info"].get("requires_dist")
    return dependencies or []


def extract_dependency_names(dependencies):
    """Извлечь имена зависимостей без дополнительных extras."""
    names = []

    for dependency in dependencies:
        if ";" in dependency:
            continue

        match = re.match(r"^[A-Za-z0-9][A-Za-z0-9._-]*", dependency)

        if match:
            name = normalize_package_name(match.group())
            names.append(name)

    return names
