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


# Тест 009: Проверка что не распознанная страна возвращает None.
def test_normalize_unknown_country():
    from src.application.country_normalizer import normalize_country
    result = normalize_country("НеизвестнаяСтрана")
    assert result is None


# Тест 010: Проверка что пустая строка возвращает None.
def test_normalize_empty_string():
    from src.application.country_normalizer import normalize_country
    result = normalize_country("")
    assert result is None


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
    assert normalized == ["Russia", "Germany"]
    assert unknown == ["Неизвестная"]


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
