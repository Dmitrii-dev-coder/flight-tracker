# Трекер самолётов

Python-приложение для сбора и анализа данных о самолётах в воздушных пространствах выбранных стран через внешние API.

## Возможности

- Получение географических координат стран через OpenStreetMap Nominatim API
- Запрос данных о самолётах в реальном времени через OpenSky Network API
- Нормализация названий стран (русский, английский, ISO коды) через pycountry
- Фильтрация самолётов по стране регистрации и диапазону высот
- Сортировка по высоте (по убыванию)
- Получение топ N самых высоких самолётов
- Сохранение данных в JSON-файл
- Консольный пользовательский интерфейс с предупреждениями о нераспознанных странах

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
│   ├── application/         # Бизнес-логика
│   │   ├── aeroplane.py         # Класс самолёта
│   │   ├── aeroplane_base.py    # Абстрактный базовый класс
│   │   ├── aeroplane_data.py    # Абстракция данных (ISP)
│   │   ├── aeroplane_comparable.py  # Абстракция сравнения (ISP)
│   │   ├── country_normalizer.py    # Нормализация названий стран
│   │   ├── filters.py           # Фильтрация и сортировка
│   │   └── user_interface.py    # Пользовательский интерфейс
│   └── infrastructure/      # Инфраструктура
│       ├── api_base.py            # Абстрактный API-коннектор
│       ├── aeroplanes_api.py      # Конкретный API-коннектор
│       ├── api_utils.py         # Circuit Breaker, Retry с Jitter
│       ├── file_connector.py    # Абстрактный файловый коннектор
│       ├── http_requestor.py    # Абстракция HTTP-запросов (DIP)
│       ├── requests_http_client.py  # Реализация HTTP через requests
│       ├── json_saver.py        # Сохранение в JSON
│       ├── csv_saver.py         # Заглушка CSV
│       └── txt_saver.py         # Заглушка TXT
├── tests/                   # Тесты (126 тестов, покрытие ≥70%)
│   ├── test_aeroplane.py
│   ├── test_aeroplane_comparison.py
│   ├── test_aeroplanes_api.py
│   ├── test_api_base.py
│   ├── test_api_utils.py
│   ├── test_country_normalizer.py   # Тесты нормализации стран
│   ├── test_dip_http_requestor.py   # DIP тесты
│   ├── test_file_connector.py
│   ├── test_filters.py
│   ├── test_integration.py
│   ├── test_isp_separation.py       # ISP тесты
│   ├── test_json_saver.py
│   └── test_user_interface.py
├── main.py                  # Точка входа
├── pyproject.toml           # Зависимости Poetry
└── .gitignore
```

## Используемые технологии

- **ООП:** абстрактные классы, наследование, инкапсуляция, магические методы, множественное наследование
- **Принципы SOLID:**
  - SRP — единственная ответственность (каждый класс отвечает за свою область)
  - OCP — открытость/закрытость (расширение без модификации)
  - LSP — подстановка наследников (корректная замена абстракций)
  - ISP — разделение интерфейсов (AeroplaneData, AeroplaneComparable)
  - DIP — инверсия зависимостей (HTTPRequestor абстракция)
- **TDD:** тесты написаны до реализации кода
- **API интеграция:** requests, JSON-ответы, обработка исключений
- **Устойчивость API:** Circuit Breaker, Retry с Jitter (tenacity)
- **Нормализация данных:** pycountry (русские/английские названия, ISO коды)
- **Паттерны:** Adapter (HTTPRequestor → RequestsHTTPClient), Strategy (Circuit Breaker states)

## Паттерны устойчивости API

Проект реализует паттерны для устойчивого подключения к внешним API:

- **Circuit Breaker** — предотвращает повторные запросы к недоступному API (CLOSED → OPEN → HALF_OPEN)
- **Retry с Jitter** — повтор запросов с увеличивающейся задержкой и случайным разбросом
- **Timeout** — таймаут для всех HTTP-запросов (10 секунд)

## Лицензия

MIT
