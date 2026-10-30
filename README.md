# Трекер самолётов

Python-приложение для сбора и анализа данных о самолётах в воздушных пространствах выбранных стран через внешние API.

## Возможности

- Получение географических координат стран через OpenStreetMap Nominatim API
- Запрос данных о самолётах в реальном времени через OpenSky Network API
- Фильтрация самолётов по стране регистрации и диапазону высот
- Сортировка по высоте (по убыванию)
- Получение топ N самых высоких самолётов
- Сохранение данных в JSON-файл
- Консольный пользовательский интерфейс

## Требования

- Python 3.10+
- Poetry (управление зависимостями)

## Установка

```bash
# Установка зависимостей
poetry install
```

## Запуск

```bash
# Запуск приложения
poetry run python main.py
```

## Тесты

```bash
# Запуск всех тестов
poetry run pytest

# Запуск с отчётом о покрытии
poetry run pytest --cov=src --cov-report=html

# HTML-отчёт доступен в папке htmlcov/index.html
```

## Структура проекта

```
flight_tracker/
├── data/                    # JSON-файлы с данными
├── src/                     # Исходный код
│   ├── api_base.py          # Абстрактный базовый класс API
│   ├── aeroplanes_api.py    # Конкретный API-коннектор
│   ├── aeroplane.py         # Класс самолёта
│   ├── file_connector.py    # Абстрактный файловый коннектор
│   ├── json_saver.py        # Сохранение в JSON
│   ├── csv_saver.py         # Заглушка CSV
│   ├── txt_saver.py         # Заглушка TXT
│   ├── filters.py           # Фильтрация и сортировка
│   └── user_interface.py    # Пользовательский интерфейс
├── tests/                   # Тесты
│   ├── test_api_base.py
│   ├── test_aeroplanes_api.py
│   ├── test_aeroplane.py
│   ├── test_aeroplane_comparison.py
│   ├── test_file_connector.py
│   ├── test_json_saver.py
│   ├── test_filters.py
│   ├── test_user_interface.py
│   └── test_integration.py
├── main.py                  # Точка входа
├── pyproject.toml           # Зависимости Poetry
└── .gitignore
```

## Используемые технологии

- **ООП:** абстрактные классы, наследование, инкапсуляция, магические методы
- **Принципы SOLID:** SRP (единственная ответственность), OCP (открытость/закрытость)
- **TDD:** тесты написаны до реализации кода
- **API интеграция:** requests, JSON-ответы, обработка исключений
- **Устойчивость API:** Circuit Breaker, Retry с Jitter (tenacity)

## Паттерны устойчивости API

Проект реализует паттерны для устойчивого подключения к внешним API:

- **Circuit Breaker** — предотвращает повторные запросы к недоступному API (CLOSED → OPEN → HALF_OPEN)
- **Retry с Jitter** — повтор запросов с увеличивающейся задержкой и случайным разбросом
- **Timeout** — таймаут для всех HTTP-запросов (10 секунд)

## Лицензия

MIT
