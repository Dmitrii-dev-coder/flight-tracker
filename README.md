# Трекер самолётов

**Версия:** 0.1.0 | **Дата создания:** 2026-11-03

Python-приложение для сбора и анализа данных о самолётах в воздушных пространствах выбранных стран через внешние API.

## Содержание

- [Возможности](#возможности)
- [Требования](#требования)
- [Установка](#установка)
- [Запуск](#запуск)
- [Тесты](#тесты)
- [Структура проекта](#структура-проекта)
- [Основные классы](#основные-классы)
  - [Aeroplane](#aeroplane-srcapplicationaeroplanepy)
  - [AeroplanesAPI](#aeroplanesapisrcinfrastructureaeroplanes_apipy)
  - [CircuitBreaker](#circuitbreakersrcinfrastructureapi_utilsipy)
  - [JSONSaver](#jsonsaversrcinfrastructurejson_saveripy)
  - [country_normalizer](#country_normalizersrcapplicationcountry_normalizerpy)
  - [filters](#filterssrcapplicationfilterspy)
- [Используемые технологии](#используемые-технологии)
- [Паттерны устойчивости API](#паттерны-устойчивости-api)
- [Лицензия](#лицензия)

> **Примечание:** Для перехода к конкретному классу используйте ссылки на подразделы выше.

---

## Возможности

- Получение географических координат стран через OpenStreetMap Nominatim API
- Запрос данных о самолётах в реальном времени через OpenSky Network API
- Нормализация названий стран (русский, английский, ISO коды) через pycountry
- Пользовательский словарь переводов стран (сохранение в JSON)
- Фильтрация самолётов по стране регистрации и диапазону высот
- Сортировка по высоте (по убыванию)
- Получение топ N самых высоких самолётов
- Сохранение данных в JSON-файл
- Консольный пользовательский интерфейс с рекомендациями ресурсов для нераспознанных стран

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
├── tests/                   # Тесты (171 тест, покрытие ≥70%)
│   ├── test_aeroplane.py
│   ├── test_aeroplane_comparison.py
│   ├── test_aeroplanes_api.py
│   ├── test_api_base.py
│   ├── test_api_utils.py
│   ├── test_country_normalizer.py   # Тесты нормализации стран
│   ├── test_csv_saver.py            # Тесты CSV-коннектора
│   ├── test_dip_http_requestor.py   # DIP тесты
│   ├── test_file_connector.py
│   ├── test_filters.py
│   ├── test_integration.py
│   ├── test_json_saver.py
│   ├── test_main.py                 # Тесты main.py
│   ├── test_requests_http_client.py # Тесты HTTP-клиента
│   ├── test_txt_saver.py            # Тесты TXT-коннектора
│   └── test_user_interface.py
├── main.py                  # Точка входа
├── pyproject.toml           # Зависимости Poetry
└── .gitignore
```

## Основные классы

### Aeroplane (src/application/aeroplane.py)

Класс для хранения и обработки информации о самолёте.

**Атрибуты:**
- `callsign` — позывной рейса
- `country` — страна регистрации
- `velocity` — горизонтальная скорость (м/с)
- `altitude` — барометрическая высота (м)
- `latitude` — широта
- `longitude` — долгота
- `on_ground` — на земле
- `geo_altitude` — геометрическая высота (м)
- `vertical_rate` — вертикальная скорость (м/с)
- `true_track` — курс (градусы)

**Методы:**
- `__init__()` — инициализация с валидацией
- `_validate()` — валидация входных данных
- `cast_to_object_list()` — создание списка объектов из словарей
- `__lt__()`, `__gt__()`, `__le__()`, `__ge__()` — сравнение по скорости и высоте

**Наследование:** `Aeroplane` — самостоятельный класс с инкапсуляцией данных и методов сравнения

### AeroplanesAPI (src/infrastructure/aeroplanes_api.py)

Конкретный API-коннектор для работы с Nominatim и OpenSky.

**Методы:**
- `get_aeroplanes(country)` — получение самолётов по стране
- `_get_bounding_box(country)` — получение координат страны через Nominatim
- `_fetch_aeroplanes(bounding_box)` — получение данных через OpenSky

### CircuitBreaker (src/infrastructure/api_utils.py)

Паттерн устойчивого подключения.

**Состояния:** CLOSED → OPEN → HALF_OPEN

**Методы:**
- `record_success()` — зафиксировать успешный запрос
- `record_failure()` — зафиксировать ошибку
- `allow_request()` — проверить возможность запроса

### JSONSaver (src/infrastructure/json_saver.py)

Сохранение данных о самолётах в JSON-файл.

**Методы:**
- `add_aeroplane(aeroplane)` — добавить самолёт
- `get_aeroplanes()` — получить все самолёты
- `delete_aeroplane(aeroplane)` — удалить самолёт

### country_normalizer (src/application/country_normalizer.py)

Нормализация названий стран.

**Функции:**
- `normalize_country(name)` — нормализовать название страны
- `normalize_countries(names)` — нормализовать список стран
- `save_translation(ru_name, en_name)` — сохранить перевод в JSON
- `_load_user_dict()` — загрузить пользовательский словарь

### filters (src/application/filters.py)

Фильтрация и сортировка самолётов.

**Функции:**
- `filter_by_country(aeroplanes, countries)` — фильтр по стране
- `filter_by_altitude_range(aeroplanes, min_alt, max_alt)` — фильтр по высоте
- `sort_by_altitude_desc(aeroplanes)` — сортировка по убыванию
- `get_top_n(aeroplanes, n)` — получить топ N

## Используемые технологии

- **ООП:** абстрактные классы, наследование, инкапсуляция, магические методы, множественное наследование
- **Принципы SOLID:**
  - SRP — единственная ответственность (каждый класс отвечает за свою область)
  - OCP — открытость/закрытость (расширение без модификации)
  - LSP — подстановка наследников (корректная замена абстракций)
  - DIP — инверсия зависимостей (HTTPRequestor абстракция)
- **TDD:** тесты написаны до реализации кода
- **API интеграция:** requests, JSON-ответы, обработка исключений
- **Устойчивость API:** Circuit Breaker, Retry с Jitter (tenacity)
- **Нормализация данных:** pycountry (русские/английские названия, ISO коды)
- **Пользовательский словарь:** JSON-файл для добавления переводов стран с интерфейсом пополнения
- **Паттерны:** Adapter (HTTPRequestor → RequestsHTTPClient), Strategy (Circuit Breaker states)

## Паттерны устойчивости API

Проект реализует паттерны для устойчивого подключения к внешним API:

- **Circuit Breaker** — предотвращает повторные запросы к недоступному API (CLOSED → OPEN → HALF_OPEN)
- **Retry с Jitter** — повтор запросов с увеличивающейся задержкой и случайным разбросом
- **Timeout** — таймаут для всех HTTP-запросов (10 секунд)
- **Пользовательский словарь** — сохранение новых переводов стран в JSON-файл с повторным запросом API

## Лицензия

MIT
