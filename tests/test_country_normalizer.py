# -*- coding: utf-8 -*-
"""Тесты для модуля нормализации названий стран."""

import pytest


# ============================================================================
# 0. Проверка функции: normalize_country, normalize_countries из модуля
#    src.application.country_normalizer.
# ============================================================================

# Тест 001: Проверка что модуль импортируется.
def test_module_importable():
    from src.application import country_normalizer
    assert hasattr(country_normalizer, 'normalize_country')
    assert hasattr(country_normalizer, 'normalize_countries')


# Тест 002: Проверка нормализации русского названия "Россия".
def test_normalize_russia_russian():
    from src.application.country_normalizer import normalize_country
    result = normalize_country("Россия")
    assert result == "Russia"


# Тест 003: Проверка нормализации английского названия "Russia".
def test_normalize_russia_english():
    from src.application.country_normalizer import normalize_country
    result = normalize_country("Russia")
    assert result == "Russian Federation"


# Тест 004: Проверка нормализации "США".
def test_normalize_usa_russian():
    from src.application.country_normalizer import normalize_country
    result = normalize_country("США")
    assert result == "United States"


# Тест 005: Проверка нормализации "USA".
def test_normalize_usa_english():
    from src.application.country_normalizer import normalize_country
    result = normalize_country("USA")
    assert result == "United States"


# Тест 006: Проверка нормализации "Германия".
def test_normalize_germany_russian():
    from src.application.country_normalizer import normalize_country
    result = normalize_country("Германия")
    assert result == "Germany"


# Тест 007: Проверка нормализации "Germany".
def test_normalize_germany_english():
    from src.application.country_normalizer import normalize_country
    result = normalize_country("Germany")
    assert result == "Germany"


# Тест 008: Проверка нормализации с разными регистрами.
def test_normalize_case_insensitive():
    from src.application.country_normalizer import normalize_country
    assert normalize_country("РОССИЯ") == "Russia"
    assert normalize_country("россия") == "Russia"
    assert normalize_country("RUSSIA") == "Russian Federation"


# Тест 009: Проверка что не распознанная страна возвращает оригинальное название.
def test_normalize_unknown_country():
    from src.application.country_normalizer import normalize_country
    result = normalize_country("НеизвестнаяСтрана")
    assert result == "НеизвестнаяСтрана"


# Тест 010: Проверка что пустая строка возвращает пустую строку.
def test_normalize_empty_string():
    from src.application.country_normalizer import normalize_country
    result = normalize_country("")
    assert result == ""


# Тест 011: Проверка normalize_countries с валидными странами.
def test_normalize_countries_valid():
    from src.application.country_normalizer import normalize_countries
    countries = ["Россия", "Германия", "France"]
    normalized, unknown = normalize_countries(countries)
    assert normalized == ["Russia", "Germany", "France"]
    assert unknown == []


# Тест 012: Проверка normalize_countries с нераспознанными странами.
def test_normalize_countries_with_unknown():
    from src.application.country_normalizer import normalize_countries
    countries = ["Россия", "Неизвестная", "Germany"]
    normalized, unknown = normalize_countries(countries)
    assert normalized == ["Russia", "Неизвестная", "Germany"]
    assert unknown == []


# Тест 013: Проверка normalize_countries с пустым списком.
def test_normalize_countries_empty():
    from src.application.country_normalizer import normalize_countries
    normalized, unknown = normalize_countries([])
    assert normalized == []
    assert unknown == []


# Тест 014: Проверка normalize_countries с пробелами.
def test_normalize_countries_with_spaces():
    from src.application.country_normalizer import normalize_countries
    countries = ["  Россия  ", "  Германия  "]
    normalized, unknown = normalize_countries(countries)
    assert normalized == ["Russia", "Germany"]
    assert unknown == []


# Тест 015: Проверка что pycountry доступен.
def test_pycountry_available():
    import pycountry
    assert pycountry is not None


# Тест 016: Проверка нормализации "ЮАР".
def test_normalize_south_africa_abbreviation():
    from src.application.country_normalizer import normalize_country
    result = normalize_country("ЮАР")
    assert result == "South Africa"


# ============================================================================
# 1. Проверка функций: save_translation, _load_user_dict из модуля
#    src.application.country_normalizer.
# ============================================================================

# Тест 017: Проверка сохранения перевода в пользовательский словарь.
def test_save_translation_creates_file(tmp_path, monkeypatch):
    """Проверка что save_translation создаёт JSON-файл с переводом."""
    from src.application import country_normalizer
    # Подменяем путь к файлу на временный
    temp_file = tmp_path / "country_translations.json"
    monkeypatch.setattr(country_normalizer, "_USER_DICT_PATH", temp_file)
    
    from src.application.country_normalizer import save_translation
    result = save_translation("Испытание", "TestCountry")
    
    assert result is True
    assert temp_file.exists()
    import json
    data = json.load(open(temp_file, "r", encoding="utf-8"))
    assert "испытание" in data
    assert data["испытание"] == "TestCountry"


# Тест 018: Проверка что _load_user_dict загружает существующий файл.
def test_load_user_dict_existing(tmp_path, monkeypatch):
    """Проверка что _load_user_dict читает существующий JSON."""
    from src.application import country_normalizer
    temp_file = tmp_path / "country_translations.json"
    import json
    json.dump({"тест": "TestLand"}, open(temp_file, "w", encoding="utf-8"), ensure_ascii=False)
    monkeypatch.setattr(country_normalizer, "_USER_DICT_PATH", temp_file)
    
    from src.application.country_normalizer import _load_user_dict
    result = _load_user_dict()
    
    assert result == {"тест": "TestLand"}


# Тест 019: Проверка что _load_user_dict возвращает {} при отсутствии файла.
def test_load_user_dict_missing(tmp_path, monkeypatch):
    """Проверка что _load_user_dict возвращает пустой словарь если файл отсутствует."""
    from src.application import country_normalizer
    temp_file = tmp_path / "nonexistent.json"
    monkeypatch.setattr(country_normalizer, "_USER_DICT_PATH", temp_file)
    
    from src.application.country_normalizer import _load_user_dict
    result = _load_user_dict()
    
    assert result == {}


# Тест 020: Проверка что normalize_country использует пользовательский словарь.
def test_normalize_uses_user_dict(tmp_path, monkeypatch):
    """Проверка что normalize_country сначала ищет в пользовательском словаре."""
    from src.application.country_normalizer import _load_user_dict, normalize_country
    
    temp_file = tmp_path / "country_translations.json"
    import json
    json.dump({"польская": "Poland"}, open(temp_file, "w", encoding="utf-8"), ensure_ascii=False)
    monkeypatch.setattr("src.application.country_normalizer._USER_DICT_PATH", temp_file)
    
    # Проверяем что словарь загружается
    user_dict = _load_user_dict()
    assert user_dict.get("польская") == "Poland"
    
    # Проверяем что normalize_country находит перевод
    result = normalize_country("польская")
    assert result == "Poland"
