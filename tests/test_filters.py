# -*- coding: utf-8 -*-
"""Тесты для модуля src.filters."""

import pytest

from src.application.aeroplane import Aeroplane
from src.application.filters import (
    filter_by_country,
    filter_by_altitude_range,
    sort_by_altitude_desc,
    get_top_n
)
from src.application.user_interface import print_aeroplanes
import io
import sys


# ============================================================================
# 0. Проверка функций: filter_by_country, filter_by_altitude_range,
#    sort_by_altitude_desc, get_top_n, print_aeroplanes
#    из модуля src.filters.
# ============================================================================

# Тест 001: Проверка filter_by_country — позитивный тест.
def test_filter_by_country_positive(planes_for_filtering):
    """Проверяет что фильтрация по стране возвращает только самолёты указанной страны.

    Фильтрует список planes_for_filtering по стране "Spain" и проверяет,
    что возвращаются ровно 2 самолёта и у всех страна равна "Spain".
    """
    result = filter_by_country(planes_for_filtering, ["Spain"])
    assert len(result) == 2
    for plane in result:
        assert plane.country == "Spain"


# Тест 002: Проверка filter_by_country — несколько стран.
def test_filter_by_country_multiple(planes_for_filtering):
    """Проверяет что фильтрация по списку стран возвращает самолёты всех указанных стран.

    Фильтрует по странам ["Spain", "France"] и проверяет что возвращается 3 самолёта:
    два из Испании (FLIGHT2, FLIGHT3) и один из Франции (FLIGHT4).
    """
    result = filter_by_country(planes_for_filtering, ["Spain", "France"])
    # Spain: FLIGHT2, FLIGHT3; France: FLIGHT4 = 3 самолёта
    assert len(result) == 3


# Тест 003: Проверка filter_by_country — пустой список.
def test_filter_by_country_empty(planes_for_filtering):
    """Проверяет что фильтрация по несуществующей стране возвращает пустой список.

    Фильтрует по стране "Germany" которой нет в списке и проверяет,
    что возвращается пустой список результатов.
    """
    result = filter_by_country(planes_for_filtering, ["Germany"])
    assert len(result) == 0


# Тест 004: Проверка filter_by_altitude_range — позитивный тест.
def test_filter_by_altitude_range_positive(planes_for_filtering):
    """Проверяет что фильтрация по диапазону высот возвращает самолёты в заданных пределах.

    Фильтрует самолёты по диапазону высот 1000.0-5000.0 и проверяет что
    возвращаются 3 самолёта с высотами 1000м, 2000м и 3000м.
    """
    # USA 1000, Spain 2000, Spain 3000, France 8000
    # В диапазоне 1000-5000: 1000, 2000, 3000 = 3 самолёта
    result = filter_by_altitude_range(planes_for_filtering, 1000.0, 5000.0)
    assert len(result) == 3


# Тест 005: Проверка filter_by_altitude_range — ошибка при min > max.
def test_filter_by_altitude_range_invalid():
    """Проверяет что фильтрация с min > max вызывает ValueError.

    Создаёт тестовый самолёт и пытается отфильтровать по диапазону
    где минимальная высота больше максимальной, ожидая исключения ValueError.
    """
    planes = [Aeroplane(callsign="TEST", country="Test", velocity=100.0, altitude=1000.0)]
    with pytest.raises(ValueError):
        filter_by_altitude_range(planes, 5000.0, 1000.0)


# Тест 006: Проверка sort_by_altitude_desc — сортировка по убыванию.
def test_sort_by_altitude_desc(planes_for_sorting):
    """Проверяет что сортировка по убыванию высоты возвращает правильный порядок.

    Сортирует самолёты из planes_for_sorting и проверяет что первый самолёт
    имеет высоту 5000м, второй — 3000м, третий — 1000м.
    """
    result = sort_by_altitude_desc(planes_for_sorting)
    assert result[0].altitude == 5000.0
    assert result[1].altitude == 3000.0
    assert result[2].altitude == 1000.0


# Тест 007: Проверка sort_by_altitude_desc — пустой список.
def test_sort_by_altitude_desc_empty():
    """Проверяет что сортировка пустого списка возвращает пустой список.

    Вызывает sort_by_altitude_desc с пустым списком и проверяет,
    что возвращается пустой список без ошибок.
    """
    result = sort_by_altitude_desc([])
    assert result == []


# Тест 008: Проверка get_top_n — возврат N элементов.
def test_get_top_n(planes_for_sorting):
    """Проверяет что функция get_top_n возвращает ровно N элементов с наибольшими высотами.

    Сортирует самолёты по убыванию высоты и получает топ-2, проверяя что
    это самолёты с высотами 5000м и 3000м.
    """
    sorted_planes = sort_by_altitude_desc(planes_for_sorting)
    result = get_top_n(sorted_planes, 2)
    assert len(result) == 2
    assert result[0].altitude == 5000.0
    assert result[1].altitude == 3000.0


# Тест 009: Проверка get_top_n — ошибка при отрицательном N.
def test_get_top_n_negative():
    """Проверяет что get_top_n с отрицательным N вызывает ValueError.

    Вызывает get_top_n с N=-1 и ожидает исключения ValueError.
    """
    with pytest.raises(ValueError):
        get_top_n([], -1)


# Тест 010: Проверка print_aeroplanes — вывод не вызывает ошибок.
def test_print_aeroplanes_no_error(test_plane):
    """Проверяет что print_aeroplanes корректно выводит информацию о самолёте.

    Перехватывает stdout и вызывает print_aeroplanes с тестовым самолётом,
    убеждаясь что функция не вызывает исключений при выводе.
    """
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()

    try:
        print_aeroplanes([test_plane])
    except Exception:
        pytest.fail("print_aeroplanes вызвал исключение")
    finally:
        sys.stdout = old_stdout


# Тест 011: Проверка print_aeroplanes — пустой список.
def test_print_aeroplanes_empty():
    """Проверяет что print_aeroplanes корректно обрабатывает пустой список.

    Вызывает print_aeroplanes с пустым списком и убеждается что
    функция не вызывает исключений при выводе пустого списка.
    """
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()

    try:
        print_aeroplanes([])
    except Exception:
        pytest.fail("print_aeroplanes вызвал исключение для пустого списка")
    finally:
        sys.stdout = old_stdout
