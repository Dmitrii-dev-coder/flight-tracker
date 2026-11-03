# -*- coding: utf-8 -*-
"""Тесты для сравнения самолётов по скорости и высоте."""

from src.application.aeroplane import Aeroplane


# ============================================================================
# 0. Проверка сравнения самолётов по скорости и высоте.
# ============================================================================

# Тест 001: Проверка, что самолёты сравниваются по скорости (меньше).
def test_less_than_by_velocity(fast_plane, slow_plane):
    """
    Проверяет, что оператор < сравнивает самолёты по скорости.

    Медленный самолёт (100 м/с) должен быть меньше быстрого (200 м/с).
    """
    assert slow_plane < fast_plane


# Тест 002: Проверка, что самолёты сравниваются по скорости (больше).
def test_greater_than_by_velocity(fast_plane, slow_plane):
    """
    Проверяет, что оператор > сравнивает самолёты по скорости.

    Быстрый самолёт (200 м/с) должен быть больше медленного (100 м/с).
    """
    assert fast_plane > slow_plane


# Тест 003: Проверка, что самолёты сравниваются по скорости (меньше или равно).
def test_less_equal_by_velocity(fast_plane, slow_plane):
    """
    Проверяет, что оператор <= работает корректно для разных случаев.

    Медленный самолёт меньше быстрого, а быстрый равен самому себе.
    """
    assert slow_plane <= fast_plane
    assert fast_plane <= fast_plane


# Тест 004: Проверка, что самолёты сравниваются по скорости (больше или равно).
def test_greater_equal_by_velocity(fast_plane, slow_plane):
    """
    Проверяет, что оператор >= работает корректно для разных случаев.

    Быстрый самолёт больше медленного, а медленный равен самому себе.
    """
    assert fast_plane >= slow_plane
    assert slow_plane >= slow_plane


# Тест 005: Проверка, что самолёты с одинаковой скоростью сравниваются как равные.
def test_equal_velocity_comparison():
    """
    Проверяет, что самолёты с одинаковой скоростью не меньше и не больше друг друга.

    Два самолёта с одинаковой скоростью (150 м/с) должны быть равны по скорости.
    """
    plane1 = Aeroplane(callsign="FLIGHT1", country="USA", velocity=150.0, altitude=1000.0)
    plane2 = Aeroplane(callsign="FLIGHT2", country="USA", velocity=150.0, altitude=2000.0)
    assert plane1 >= plane2
    assert plane1 <= plane2
    assert not (plane1 < plane2)
    assert not (plane1 > plane2)


# Тест 006: Проверка, что сравнение с не-Aeroplane возвращает NotImplemented.
def test_comparison_with_non_aeroplane(slow_plane):
    """
    Проверяет, что сравнение самолёта со строкой возвращает NotImplemented.

    NotImplemented говорит Python попробовать обратное сравнение у другого объекта.
    """
    assert slow_plane.__lt__("not an aeroplane") is NotImplemented
    assert slow_plane.__gt__("not an aeroplane") is NotImplemented
    assert slow_plane.__le__("not an aeroplane") is NotImplemented
    assert slow_plane.__ge__("not an aeroplane") is NotImplemented
