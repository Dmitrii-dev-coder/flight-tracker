# -*- coding: utf-8 -*-
"""Тесты для модуля src.filters."""

import pytest


# ============================================================================
# 0. Проверка функций: filter_by_country, filter_by_altitude_range,
#    sort_by_altitude_desc, get_top_n, print_aeroplanes
#    из модуля src.filters.
# ============================================================================

# Тест 001: Проверка filter_by_country — позитивный тест.
def test_filter_by_country_positive():
    from src.filters import filter_by_country
    from src.aeroplane import Aeroplane

    planes = [
        Aeroplane(callsign="FLIGHT1", country="Spain", velocity=100.0, altitude=1000.0),
        Aeroplane(callsign="FLIGHT2", country="USA", velocity=200.0, altitude=2000.0),
        Aeroplane(callsign="FLIGHT3", country="Spain", velocity=150.0, altitude=1500.0),
    ]

    result = filter_by_country(planes, ["Spain"])
    assert len(result) == 2
    for plane in result:
        assert plane.country == "Spain"


# Тест 002: Проверка filter_by_country — несколько стран.
def test_filter_by_country_multiple():
    from src.filters import filter_by_country
    from src.aeroplane import Aeroplane

    planes = [
        Aeroplane(callsign="FLIGHT1", country="Spain", velocity=100.0, altitude=1000.0),
        Aeroplane(callsign="FLIGHT2", country="USA", velocity=200.0, altitude=2000.0),
        Aeroplane(callsign="FLIGHT3", country="France", velocity=150.0, altitude=1500.0),
    ]

    result = filter_by_country(planes, ["Spain", "France"])
    assert len(result) == 2


# Тест 003: Проверка filter_by_country — пустой список.
def test_filter_by_country_empty():
    from src.filters import filter_by_country
    from src.aeroplane import Aeroplane

    planes = [
        Aeroplane(callsign="FLIGHT1", country="Spain", velocity=100.0, altitude=1000.0),
    ]

    result = filter_by_country(planes, ["Germany"])
    assert len(result) == 0


# Тест 004: Проверка filter_by_altitude_range — позитивный тест.
def test_filter_by_altitude_range_positive():
    from src.filters import filter_by_altitude_range
    from src.aeroplane import Aeroplane

    planes = [
        Aeroplane(callsign="FLIGHT1", country="Spain", velocity=100.0, altitude=1000.0),
        Aeroplane(callsign="FLIGHT2", country="USA", velocity=200.0, altitude=5000.0),
        Aeroplane(callsign="FLIGHT3", country="France", velocity=150.0, altitude=10000.0),
    ]

    result = filter_by_altitude_range(planes, 1000.0, 5000.0)
    assert len(result) == 2


# Тест 005: Проверка filter_by_altitude_range — ошибка при min > max.
def test_filter_by_altitude_range_invalid():
    from src.filters import filter_by_altitude_range
    from src.aeroplane import Aeroplane

    planes = [
        Aeroplane(callsign="FLIGHT1", country="Spain", velocity=100.0, altitude=1000.0),
    ]

    with pytest.raises(ValueError):
        filter_by_altitude_range(planes, 5000.0, 1000.0)


# Тест 006: Проверка sort_by_altitude_desc — сортировка по убыванию.
def test_sort_by_altitude_desc():
    from src.filters import sort_by_altitude_desc
    from src.aeroplane import Aeroplane

    planes = [
        Aeroplane(callsign="FLIGHT1", country="Spain", velocity=100.0, altitude=1000.0),
        Aeroplane(callsign="FLIGHT2", country="USA", velocity=200.0, altitude=5000.0),
        Aeroplane(callsign="FLIGHT3", country="France", velocity=150.0, altitude=3000.0),
    ]

    result = sort_by_altitude_desc(planes)
    assert result[0].altitude == 5000.0
    assert result[1].altitude == 3000.0
    assert result[2].altitude == 1000.0


# Тест 007: Проверка sort_by_altitude_desc — пустой список.
def test_sort_by_altitude_desc_empty():
    from src.filters import sort_by_altitude_desc

    result = sort_by_altitude_desc([])
    assert result == []


# Тест 008: Проверка get_top_n — возврат N элементов.
def test_get_top_n():
    from src.filters import get_top_n, sort_by_altitude_desc
    from src.aeroplane import Aeroplane

    planes = [
        Aeroplane(callsign="FLIGHT1", country="Spain", velocity=100.0, altitude=1000.0),
        Aeroplane(callsign="FLIGHT2", country="USA", velocity=200.0, altitude=5000.0),
        Aeroplane(callsign="FLIGHT3", country="France", velocity=150.0, altitude=3000.0),
    ]

    sorted_planes = sort_by_altitude_desc(planes)
    result = get_top_n(sorted_planes, 2)
    assert len(result) == 2
    assert result[0].altitude == 5000.0
    assert result[1].altitude == 3000.0


# Тест 009: Проверка get_top_n — ошибка при отрицательном N.
def test_get_top_n_negative():
    from src.filters import get_top_n

    with pytest.raises(ValueError):
        get_top_n([], -1)


# Тест 010: Проверка print_aeroplanes — вывод не вызывает ошибок.
def test_print_aeroplanes_no_error():
    from src.filters import print_aeroplanes
    from src.aeroplane import Aeroplane
    import io
    import sys

    planes = [
        Aeroplane(callsign="FLIGHT1", country="Spain", velocity=100.0, altitude=1000.0),
    ]

    old_stdout = sys.stdout
    sys.stdout = io.StringIO()

    try:
        print_aeroplanes(planes)
    except Exception:
        pytest.fail("print_aeroplanes вызвал исключение")
    finally:
        sys.stdout = old_stdout


# Тест 011: Проверка print_aeroplanes — пустой список.
def test_print_aeroplanes_empty():
    from src.filters import print_aeroplanes
    import io
    import sys

    old_stdout = sys.stdout
    sys.stdout = io.StringIO()

    try:
        print_aeroplanes([])
    except Exception:
        pytest.fail("print_aeroplanes вызвал исключение для пустого списка")
    finally:
        sys.stdout = old_stdout
