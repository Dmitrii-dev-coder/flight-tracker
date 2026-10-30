# -*- coding: utf-8 -*-
"""Тесты для модуля src.aeroplane."""

import pytest


# ============================================================================
# 0. Проверка класса: Aeroplane из модуля src.aeroplane.
# ============================================================================

# Тест 001: Проверка что можно создать экземпляр Aeroplane.
def test_can_create_aeroplane():
    from src.aeroplane import Aeroplane
    plane = Aeroplane(
        callsign="UAL1621",
        country="United States",
        velocity=268.79,
        altitude=10203.18
    )
    assert plane is not None
    assert isinstance(plane, Aeroplane)


# Тест 002: Проверка что все атрибуты сохранены корректно.
def test_attributes_stored_correctly():
    from src.aeroplane import Aeroplane
    plane = Aeroplane(
        callsign="SWR438A",
        country="Switzerland",
        velocity=189.7,
        altitude=4267.2,
        latitude=51.0888,
        longitude=-0.0168,
        on_ground=False,
        geo_altitude=4282.44,
        vertical_rate=14.63,
        true_track=129.39
    )
    assert plane.callsign == "SWR438A"
    assert plane.country == "Switzerland"
    assert plane.velocity == 189.7
    assert plane.altitude == 4267.2
    assert plane.latitude == 51.0888
    assert plane.longitude == -0.0168
    assert plane.on_ground is False
    assert plane.geo_altitude == 4282.44
    assert plane.vertical_rate == 14.63
    assert plane.true_track == 129.39


# Тест 003: Проверка что приватные атрибуты недоступны напрямую.
def test_private_attributes():
    from src.aeroplane import Aeroplane
    plane = Aeroplane(
        callsign="TEST",
        country="Test",
        velocity=100.0,
        altitude=1000.0
    )
    with pytest.raises(AttributeError):
        _ = plane.__callsign


# Тест 004: Проверка что callsign не может быть пустым.
def test_empty_callsign_raises_error():
    from src.aeroplane import Aeroplane
    with pytest.raises(ValueError):
        Aeroplane(
            callsign="",
            country="Test",
            velocity=100.0,
            altitude=1000.0
        )


# Тест 005: Проверка что velocity не может быть отрицательным.
def test_negative_velocity_raises_error():
    from src.aeroplane import Aeroplane
    with pytest.raises(ValueError):
        Aeroplane(
            callsign="TEST",
            country="Test",
            velocity=-50.0,
            altitude=1000.0
        )


# Тест 006: Проверка что altitude не может быть отрицательным.
def test_negative_altitude_raises_error():
    from src.aeroplane import Aeroplane
    with pytest.raises(ValueError):
        Aeroplane(
            callsign="TEST",
            country="Test",
            velocity=100.0,
            altitude=-500.0
        )


# Тест 007: Проверка что geo_altitude не может быть отрицательным.
def test_negative_geo_altitude_raises_error():
    from src.aeroplane import Aeroplane
    with pytest.raises(ValueError):
        Aeroplane(
            callsign="TEST",
            country="Test",
            velocity=100.0,
            altitude=1000.0,
            geo_altitude=-100.0
        )


# Тест 008: Проверка магического метода __str__.
def test_str_method():
    from src.aeroplane import Aeroplane
    plane = Aeroplane(
        callsign="UAL1621",
        country="United States",
        velocity=268.79,
        altitude=10203.18
    )
    result = str(plane)
    assert isinstance(result, str)
    assert "UAL1621" in result


# Тест 009: Проверка магического метода __repr__.
def test_repr_method():
    from src.aeroplane import Aeroplane
    plane = Aeroplane(
        callsign="TEST",
        country="Test",
        velocity=100.0,
        altitude=1000.0
    )
    result = repr(plane)
    assert isinstance(result, str)
    assert "TEST" in result


# Тест 010: Проверка что __eq__ сравнивает по callsign.
def test_eq_method():
    from src.aeroplane import Aeroplane
    plane1 = Aeroplane(
        callsign="UAL1621",
        country="United States",
        velocity=268.79,
        altitude=10203.18
    )
    plane2 = Aeroplane(
        callsign="UAL1621",
        country="Germany",
        velocity=300.0,
        altitude=9000.0
    )
    plane3 = Aeroplane(
        callsign="DIFFERENT",
        country="Test",
        velocity=100.0,
        altitude=1000.0
    )
    assert plane1 == plane2
    assert plane1 != plane3


# Тест 011: Проверка что cast_to_object_list преобразует JSON в объекты.
def test_cast_to_object_list():
    from src.aeroplane import Aeroplane
    json_data = [
        [
            "4b1812", "SWR438A ", "Switzerland", 1766166618, 1766166618,
            -0.0168, 51.0888, 4267.2, False, 189.7, 129.39, 14.63,
            None, 4282.44, "2061", False, 0
        ]
    ]
    result = Aeroplane.cast_to_object_list(json_data)
    assert isinstance(result, list)
    assert len(result) == 1
    assert isinstance(result[0], Aeroplane)
    assert result[0].callsign == "SWR438A"
    assert result[0].country == "Switzerland"
    assert result[0].velocity == 189.7
    assert result[0].altitude == 4267.2


# Тест 012: Проверка что cast_to_object_list обрабатывает пустой список.
def test_cast_to_object_list_empty():
    from src.aeroplane import Aeroplane
    result = Aeroplane.cast_to_object_list([])
    assert isinstance(result, list)
    assert len(result) == 0


# Тест 013: Проверка что cast_to_object_list обрабатывает None элементы.
def test_cast_to_object_list_with_none():
    from src.aeroplane import Aeroplane
    json_data = [None, ["4b1812", "TEST", "Test", 0, 0, 0.0, 0.0, 1000.0, False, 100.0, 0.0, 0.0, None, 1000.0, "0000", False, 0]]
    result = Aeroplane.cast_to_object_list(json_data)
    assert len(result) == 1
    assert isinstance(result[0], Aeroplane)
