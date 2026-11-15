# configuration_management_pr2_kuznetsov_s_IKBO-23-25
Репозиторий с практическим заданием № 2 по дисциплине "Конфигурационное управление", студента группы ИКБО-23-25 Кузнецов С.

## Практическая работа №2. Вариант 11

Инструмент анализа зависимостей Python-пакетов.

### Этап 1. Минимальный прототип

Реализовано CLI-приложение с аргументами:

- `--package` — имя анализируемого пакета (обязательный).
- `--repository` — URL репозитория или путь к тестовому файлу
  (обязательный).
- `--test-mode` — использовать локальный тестовый репозиторий.
- `--ascii-tree` — включить режим ASCII-дерева.

В первом этапе приложение выводит значения параметров.
Реализована проверка имени пакета, URL и тестового файла.

### Запуск

```bash
python src/main.py --package requests --repository https://pypi.org/pypi
```

На Windows также можно использовать:

```bat
run.bat --package requests --repository https://pypi.org/pypi
```

### Запуск тестов

```bash
python -m unittest discover -s tests -v
```

### Тестовый режим

```bash
python src/main.py --package A --repository tests/graph.txt --test-mode
```

### Требования

Python 3.10 или новее. Сторонние библиотеки не используются.
