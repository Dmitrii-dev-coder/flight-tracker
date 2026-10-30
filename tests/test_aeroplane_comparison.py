# -*- coding: utf-8 -*-
"""Тесты для сравнения самолётов по скорости и высоте."""

import pytest


# ============================================================================
# 0. Проверка сравнения самолётов по скорости и высоте.
# ============================================================================

# Тест 001: Проверка что самолёты сравниваются по скорости (меньше).
def test_less_than_by_velocity():
    from src.aeroplane import Aeroplane
    plane1 = Aeroplane(callsign="FLIGHT1", country="USA", velocity=100.0, altitude=1000.0)
    plane2 = Aeroplane(callsign="FLIGHT2", country="USA", velocity=200.0, altitude=1000.0)
    assert plane1 < plane2


# Тест 002: Проверка что самолёты сравниваются по скорости (больше).
def test_greater_than_by_velocity():
    from src.aeroplane import Aeroplane
    plane1 = Aeroplane(callsign="FLIGHT1", country="USA", velocity=200.0, altitude=1000.0)
    plane2 = Aeroplane(callsign="FLIGHT2", country="USA", velocity=100.0, altitude=1000.0)
    assert plane1 > plane2


# Тест 003: Проверка что самолёты сравниваются по скорости (меньше или равно).
def test_less_equal_by_velocity():
    from src.aeroplane import Aeroplane
    plane1 = Aeroplane(callsign="FLIGHT1", country="USA", velocity=100.0, altitude=1000.0)
    plane2 = Aeroplane(callsign="FLIGHT2", country="USA", velocity=100.0, altitude=1000.0)
    assert plane1 <= plane2


# Тест 004: Проверка что самолёты сравниваются по скорости (больше или равно).
def test_greater_equal_by_velocity():
    from src.aeroplane import Aeroplane
    plane1 = Aeroplane(callsign="FLIGHT1", country="USA", velocity=200.0, altitude=1000.0)
    plane2 = Aeroplane(callsign="FLIGHT2", country="USA", velocity=100.0, altitude=1000.0)
    assert plane1 >= plane2


# Тест 005: Проверка что самолёты с одинаковой скоростью равны по сравнению.
def test_equal_velocity_comparison():
    from src.aeroplane import Aeroplane
    plane1 = Aeroplane(callsign="FLIGHT1", country="USA", velocity=150.0, altitude=1000.0)
    plane2 = Aeroplane(callsign="FLIGHT2", country="USA", velocity=150.0, altitude=2000.0)
    assert plane1 >= plane2
    assert plane1 <= plane2
    assert not (plane1 < plane2)
    assert not (plane1 > plane2)


# Тест 006: Проверка что сравнение с не-Aeroplane возвращает NotImplemented.
def test_comparison_with_non_aeroplane():
    from src.aeroplane import Aeroplane
    plane = Aeroplane(callsign="FLIGHT1", country="USA", velocity=100.0, altitude=1000.0)
    assert plane.__lt__("not an aeroplane") is NotImplemented
    assert plane.__gt__("not an aeroplane") is NotImplemented
    assert plane.__le__("not an aeroplane") is NotImplemented
    assert plane.__ge__("not an aeroplane") is NotImplemented
