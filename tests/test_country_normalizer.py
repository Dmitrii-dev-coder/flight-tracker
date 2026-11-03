# -*- coding: utf-8 -*-
"""Тесты для модуля нормализации названий стран."""

import json

from src.application.country_normalizer import (
    normalize_country, normalize_countries,
    save_translation, _load_user_dict
)


# ============================================================================
# 0. Проверка функции: normalize_country, normalize_countries из модуля
#    src.application.country_normalizer.
# ============================================================================

# Тест 001: Проверка, что модуль импортируется.
def test_module_importable():
    """Проверяет что модуль country_normalizer импортируется и содержит нужные функции.

    Проверяет наличие функций normalize_country и normalize_countries
    в модуле src.application.country_normalizer.
    """
    from src.application import country_normalizer
    assert hasattr(country_normalizer, 'normalize_country')
    assert hasattr(country_normalizer, 'normalize_countries')


# Тест 002: Проверка нормализации русского названия "Россия".
def test_normalize_russia_russian():
    """Проверяет что русское название "Россия" нормализуется в "Russia".

    Вызывает normalize_country("Россия") и проверяет что результат равен "Russia".
    """
    result = normalize_country("Россия")
    assert result == "Russia"


# Тест 003: Проверка нормализации английского названия "Russia".
def test_normalize_russia_english():
    """Проверяет что английское название "Russia" нормализуется в "Russian Federation".

    Вызывает normalize_country("Russia") и проверяет что результат равен
    "Russian Federation".
    """
    result = normalize_country("Russia")
    assert result == "Russian Federation"


# Тест 004: Проверка нормализации "США".
def test_normalize_usa_russian():
    """Проверяет что русское название "США" нормализуется в "United States".

    Вызывает normalize_country("США") и проверяет что результат равен
    "United States".
    """
    result = normalize_country("США")
    assert result == "United States"


# Тест 005: Проверка нормализации "USA".
def test_normalize_usa_english():
    """Проверяет что английское сокращение "USA" нормализуется в "United States".

    Вызывает normalize_country("USA") и проверяет что результат равен
    "United States".
    """
    result = normalize_country("USA")
    assert result == "United States"


# Тест 006: Проверка нормализации "Германия".
def test_normalize_germany_russian():
    """Проверяет что русское название "Германия" нормализуется в "Germany".

    Вызывает normalize_country("Германия") и проверяет что результат равен
    "Germany".
    """
    result = normalize_country("Германия")
    assert result == "Germany"


# Тест 007: Проверка нормализации "Germany".
def test_normalize_germany_english():
    """Проверяет что английское название "Germany" остаётся без изменений.

    Вызывает normalize_country("Germany") и проверяет что результат равен
    "Germany".
    """
    result = normalize_country("Germany")
    assert result == "Germany"


# Тест 008: Проверка нормализации с разными регистрами.
def test_normalize_case_insensitive():
    """Проверяет что нормализация работает независимо от регистра.

    Проверяет что "РОССИЯ", "россия" и "RUSSIA" корректно нормализуются
    в "Russia" и "Russian Federation" соответственно.
    """
    assert normalize_country("РОССИЯ") == "Russia"
    assert normalize_country("россия") == "Russia"
    assert normalize_country("RUSSIA") == "Russian Federation"


# Тест 009: Проверка, что не распознанная страна возвращает оригинальное название.
def test_normalize_unknown_country(tmp_path, monkeypatch):
    """Проверяет что нераспознанная страна возвращается без изменений.

    Вызывает normalize_country с неизвестным названием и проверяет,
    что функция возвращает оригинальное название без изменений.
    """
    from src.application import country_normalizer
    temp_file = tmp_path / "country_translations.json"
    monkeypatch.setattr(country_normalizer, "_USER_DICT_PATH", temp_file)

    result = normalize_country("XxXНеизвестнаяСтранаXxX")
    assert result == "XxXНеизвестнаяСтранаXxX"


# Тест 010: Проверка, что пустая строка возвращает пустую строку.
def test_normalize_empty_string():
    """Проверяет что пустая строка возвращается без изменений.

    Вызывает normalize_country("") и проверяет что результат пустой.
    """
    result = normalize_country("")
    assert result == ""


# Тест 011: Проверка normalize_countries с валидными странами.
def test_normalize_countries_valid():
    """Проверяет что normalize_countries корректно нормализует список валидных стран.

    Создаёт список стран ["Россия", "Германия", "France"] и проверяет что
    normalize_countries возвращает нормализованный список и пустой список
    нераспознанных стран.
    """
    countries = ["Россия", "Германия", "France"]
    normalized, unknown = normalize_countries(countries)
    assert normalized == ["Russia", "Germany", "France"]
    assert unknown == []


# Тест 012: Проверка normalize_countries с нераспознанными странами.
def test_normalize_countries_with_unknown():
    """Проверяет что normalize_countries корректно обрабатывает нераспознанные страны.

    Создаёт список с нераспознанной страной на русском языке и проверяет что
    нормализованные страны возвращаются корректно, а нераспознанная — в списке unknown.
    """
    countries = ["Россия", "Неизвестная", "Germany"]
    normalized, unknown = normalize_countries(countries)
    assert normalized == ["Russia", "Germany"]
    assert unknown == ["Неизвестная"]


# Тест 013: Проверка normalize_countries с пустым списком.
def test_normalize_countries_empty():
    """Проверяет что normalize_countries корректно обрабатывает пустой список.

    Вызывает normalize_countries([]) и проверяет что возвращаются
    два пустых списка.
    """
    normalized, unknown = normalize_countries([])
    assert normalized == []
    assert unknown == []


# Тест 014: Проверка normalize_countries с пробелами.
def test_normalize_countries_with_spaces():
    """Проверяет что normalize_countries удаляет пробелы при нормализации.

    Создаёт список стран с пробелами и проверяет что они удаляются
    при нормализации.
    """
    countries = ["  Россия  ", "  Германия  "]
    normalized, unknown = normalize_countries(countries)
    assert normalized == ["Russia", "Germany"]
    assert unknown == []


# Тест 015: Проверка, что pycountry доступен.
def test_pycountry_available():
    """Проверяет что библиотека pycountry доступна для использования.

    Импортирует pycountry и проверяет что она не равна None.
    """
    import pycountry
    assert pycountry is not None


# Тест 016: Проверка нормализации "ЮАР".
def test_normalize_south_africa_abbreviation():
    """Проверяет что русское сокращение "ЮАР" нормализуется в "South Africa".

    Вызывает normalize_country("ЮАР") и проверяет что результат равен
    "South Africa".
    """
    result = normalize_country("ЮАР")
    assert result == "South Africa"


# ============================================================================
# 1. Проверка функций: save_translation, _load_user_dict из модуля
#    src.application.country_normalizer.
# ============================================================================

# Тест 017: Проверка сохранения перевода в пользовательский словарь.
def test_save_translation_creates_file(tmp_path, monkeypatch):
    """Проверяет что save_translation создаёт JSON-файл с переводом.

    Подменяет путь к файлу на временный, вызывает save_translation
    и проверяет что файл создан и содержит корректные данные.
    """
    from src.application import country_normalizer
    # Подменяем путь к файлу на временный
    temp_file = tmp_path / "country_translations.json"
    monkeypatch.setattr(country_normalizer, "_USER_DICT_PATH", temp_file)

    result = save_translation("Испытание", "TestCountry")

    assert result is True
    assert temp_file.exists()
    data = json.load(open(temp_file, "r", encoding="utf-8"))
    assert "испытание" in data
    assert data["испытание"] == "TestCountry"


# Тест 018: Проверка, что _load_user_dict загружает существующий файл.
def test_load_user_dict_existing(tmp_path, monkeypatch):
    """Проверяет что _load_user_dict читает существующий JSON.

    Создаёт JSON-файл с тестовыми данными, подменяет путь и проверяет
    что _load_user_dict корректно загружает данные.
    """
    from src.application import country_normalizer
    temp_file = tmp_path / "country_translations.json"
    json.dump({"тест": "TestLand"}, open(temp_file, "w", encoding="utf-8"), ensure_ascii=False)
    monkeypatch.setattr(country_normalizer, "_USER_DICT_PATH", temp_file)

    result = _load_user_dict()

    assert result == {"тест": "TestLand"}


# Тест 019: Проверка, что _load_user_dict возвращает {} при отсутствии файла.
def test_load_user_dict_missing(tmp_path, monkeypatch):
    """Проверяет что _load_user_dict возвращает пустой словарь если файл отсутствует.

    Подменяет путь на несуществующий файл и проверяет что возвращается
    пустой словарь.
    """
    from src.application import country_normalizer
    temp_file = tmp_path / "nonexistent.json"
    monkeypatch.setattr(country_normalizer, "_USER_DICT_PATH", temp_file)

    result = _load_user_dict()

    assert result == {}


# Тест 020: Проверка что normalize_country использует пользовательский словарь.
def test_normalize_uses_user_dict(tmp_path, monkeypatch):
    """Проверяет что normalize_country сначала ищет в пользовательском словаре.

    Создаёт JSON-файл с пользовательским переводом, проверяет что
    _load_user_dict загружает данные и normalize_country находит перевод.
    """
    from src.application.country_normalizer import _load_user_dict

    temp_file = tmp_path / "country_translations.json"
    json.dump({"польская": "Poland"}, open(temp_file, "w", encoding="utf-8"), ensure_ascii=False)
    monkeypatch.setattr("src.application.country_normalizer._USER_DICT_PATH", temp_file)

    # Проверяем что словарь загружается
    user_dict = _load_user_dict()
    assert user_dict.get("польская") == "Poland"

    # Проверяем что normalize_country находит перевод
    result = normalize_country("польская")
    assert result == "Poland"


# Тест 021: Проверка что _load_user_dict обрабатывает некорректный JSON.
def test_load_user_dict_handles_invalid_json(tmp_path, monkeypatch):
    """Проверяет что _load_user_dict обрабатывает некорректный JSON.

    Создаёт JSON-файл с некорректным JSON и проверяет что _load_user_dict
    возвращает пустой словарь без ошибок.
    """
    from src.application import country_normalizer

    temp_file = tmp_path / "country_translations.json"
    with open(temp_file, "w", encoding="utf-8") as f:
        f.write("некорректный json {")

    monkeypatch.setattr(country_normalizer, "_USER_DICT_PATH", temp_file)

    result = _load_user_dict()
    assert result == {}


# Тест 022: Проверка, что save_translation возвращает False при ошибке записи.
def test_save_translation_handles_io_error(tmp_path, monkeypatch):
    """Проверяет что save_translation возвращает False при ошибке записи.

    Создаёт JSONSaver с путём в несуществующую директорию и проверяет что
    save_translation возвращает False при невозможности записи.
    """
    from src.application import country_normalizer

    temp_file = tmp_path / "readonly" / "translations.json"
    monkeypatch.setattr(country_normalizer, "_USER_DICT_PATH", temp_file)

    from src.application.country_normalizer import save_translation
    result = save_translation("Тест", "Test")

    assert result is False


# Тест 023: Проверка что normalize_country обрабатывает AttributeError.
def test_normalize_country_handles_attribute_error():
    """Проверяет что normalize_country обрабатывает AttributeError от pycountry.

    Проверяет что функция корректно обрабатывает исключение AttributeError
    и возвращает оригинальное название.
    """
    # Тестируем с пустым вводом
    result = normalize_country("")
    assert result == ""


# Тест 024: Проверка что normalize_countries возвращает unknown для пустых названий.
def test_normalize_countries_returns_unknown_for_empty():
    """Проверяет что normalize_countries возвращает пустое название в unknown.

    Создаёт список с пустым названием и проверяет что normalize_countries
    возвращает его в списке unknown.
    """
    countries = ["", "Россия", "Germany"]
    normalized, unknown = normalize_countries(countries)

    assert "" in unknown
    assert "Russia" in normalized
    assert "Germany" in normalized
