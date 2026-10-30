# -*- coding: utf-8 -*-
"""Тесты для модуля src.user_interface."""

import pytest
import io
import sys
from unittest.mock import patch


# ============================================================================
# 0. Проверка функции: user_interaction из модуля src.user_interface.
# ============================================================================

# Тест 001: Проверка что функция существует и принимает список самолётов.
def test_user_interaction_exists():
    from src.application.user_interface import user_interaction
    assert callable(user_interaction)


# Тест 002: Проверка что функция не вызывает ошибок при пустом списке.
def test_user_interaction_empty_list():
    from src.application.user_interface import user_interaction

    old_stdout = sys.stdout
    sys.stdout = io.StringIO()

    try:
        with patch("builtins.input", side_effect=["0", "", "0 - 1000"]):
            user_interaction([])
    except Exception as e:
        pytest.fail(f"user_interaction вызвал исключение: {e}")
    finally:
        sys.stdout = old_stdout


# Тест 003: Проверка что функция корректно обрабатывает ввод топ N.
def test_user_interaction_top_n():
    from src.application.user_interface import user_interaction
    from src.application.aeroplane import Aeroplane

    planes = [
        Aeroplane(callsign="FLIGHT1", country="Spain", velocity=100.0, altitude=1000.0),
        Aeroplane(callsign="FLIGHT2", country="USA", velocity=200.0, altitude=5000.0),
        Aeroplane(callsign="FLIGHT3", country="France", velocity=150.0, altitude=3000.0),
    ]

    old_stdout = sys.stdout
    sys.stdout = io.StringIO()

    try:
        with patch("builtins.input", side_effect=["2", "", "0 - 1000"]):
            user_interaction(planes)
    except Exception as e:
        pytest.fail(f"user_interaction вызвал исключение: {e}")
    finally:
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout

    # Проверяем что вывод содержит заголовок
    assert "Трекер самолётов" in output


# Тест 004: Проверка что функция корректно обрабатывает ввод страны.
def test_user_interaction_country_filter():
    from src.application.user_interface import user_interaction
    from src.application.aeroplane import Aeroplane

    planes = [
        Aeroplane(callsign="FLIGHT1", country="Spain", velocity=100.0, altitude=1000.0),
        Aeroplane(callsign="FLIGHT2", country="USA", velocity=200.0, altitude=5000.0),
    ]

    old_stdout = sys.stdout
    sys.stdout = io.StringIO()

    try:
        with patch("builtins.input", side_effect=["0", "Spain", "0 - 1000"]):
            user_interaction(planes)
    except Exception as e:
        pytest.fail(f"user_interaction вызвал исключение: {e}")
    finally:
        sys.stdout = old_stdout


# Тест 005: Проверка что функция корректно обрабатывает ввод диапазона высот.
def test_user_interaction_altitude_range():
    from src.application.user_interface import user_interaction
    from src.application.aeroplane import Aeroplane

    planes = [
        Aeroplane(callsign="FLIGHT1", country="Spain", velocity=100.0, altitude=1000.0),
        Aeroplane(callsign="FLIGHT2", country="USA", velocity=200.0, altitude=5000.0),
    ]

    old_stdout = sys.stdout
    sys.stdout = io.StringIO()

    try:
        with patch("builtins.input", side_effect=["0", "", "1000 - 5000"]):
            user_interaction(planes)
    except Exception as e:
        pytest.fail(f"user_interaction вызвал исключение: {e}")
    finally:
        sys.stdout = old_stdout


# Тест 006: Проверка что функция обрабатывает некорректный ввод топ N.
def test_user_interaction_invalid_top_n():
    from src.application.user_interface import user_interaction

    old_stdout = sys.stdout
    sys.stdout = io.StringIO()

    try:
        with patch("builtins.input", side_effect=["abc", "", "0 - 1000"]):
            user_interaction([])
    except Exception as e:
        pytest.fail(f"user_interaction вызвал исключение: {e}")
    finally:
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout

    # Проверяем что выведено сообщение об ошибке
    assert "Ошибка" in output or "не найдены" in output


# Тест 007: Проверка что функция обрабатывает некорректный диапазон высот.
def test_user_interaction_invalid_altitude():
    from src.application.user_interface import user_interaction

    old_stdout = sys.stdout
    sys.stdout = io.StringIO()

    try:
        with patch("builtins.input", side_effect=["0", "", "abc"]):
            user_interaction([])
    except Exception as e:
        pytest.fail(f"user_interaction вызвал исключение: {e}")
    finally:
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout

    # Проверяем что выведено сообщение об ошибке
    assert "Ошибка" in output or "не найдены" in output
