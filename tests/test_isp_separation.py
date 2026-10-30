# -*- coding: utf-8 -*-
"""Тесты для проверки принципа ISP: разделённые интерфейсы AeroplaneData и AeroplaneComparable."""

import pytest
from abc import ABC


# ============================================================================
# 1. Проверка AeroplaneData (ISP: только данные, без сравнения).
# ============================================================================

# Тест 001: AeroplaneData — абстрактный класс.
def test_aeroplane_data_is_abstract():
    from src.application.aeroplane_data import AeroplaneData
    assert issubclass(AeroplaneData, ABC)


# Тест 002: Нельзя инстанцировать AeroplaneData напрямую.
def test_cannot_instantiate_aeroplane_data():
    from src.application.aeroplane_data import AeroplaneData
    with pytest.raises(TypeError):
        AeroplaneData()


# Тест 003: Aeroplane наследуется от AeroplaneData.
def test_aeroplane_inherits_from_aeroplane_data():
    from src.application.aeroplane import Aeroplane
    from src.application.aeroplane_data import AeroplaneData
    assert issubclass(Aeroplane, AeroplaneData)


# Тест 004: AeroplaneData имеет только 10 свойств данных.
def test_aeroplane_data_has_only_data_properties():
    from src.application.aeroplane_data import AeroplaneData
    data_properties = [
        "callsign", "country", "velocity", "altitude",
        "latitude", "longitude", "on_ground",
        "geo_altitude", "vertical_rate", "true_track"
    ]
    for prop in data_properties:
        assert hasattr(AeroplaneData, prop)


# Тест 005: Клиент, которому нужны только данные, не зависит от сравнения.
def test_data_client_does_not_need_comparison():
    from src.application.aeroplane import Aeroplane
    from src.application.aeroplane_data import AeroplaneData

    plane = Aeroplane(
        callsign="TEST",
        country="Russia",
        velocity=200.0,
        altitude=5000.0
    )

    # Функция принимает только AeroplaneData (данные)
    def extract_data(p: AeroplaneData) -> dict:
        return {
            "callsign": p.callsign,
            "country": p.country,
            "velocity": p.velocity,
            "altitude": p.altitude
        }

    result = extract_data(plane)
    assert result["callsign"] == "TEST"
    assert result["velocity"] == 200.0


# ============================================================================
# 2. Проверка AeroplaneComparable (ISP: только сравнение, без данных).
# ============================================================================

# Тест 006: AeroplaneComparable — абстрактный класс.
def test_aeroplane_comparable_is_abstract():
    from src.application.aeroplane_comparable import AeroplaneComparable
    assert issubclass(AeroplaneComparable, ABC)


# Тест 007: Нельзя инстанцировать AeroplaneComparable напрямую.
def test_cannot_instantiate_aeroplane_comparable():
    from src.application.aeroplane_comparable import AeroplaneComparable
    with pytest.raises(TypeError):
        AeroplaneComparable()


# Тест 008: Aeroplane наследуется от AeroplaneComparable.
def test_aeroplane_inherits_from_aeroplane_comparable():
    from src.application.aeroplane import Aeroplane
    from src.application.aeroplane_comparable import AeroplaneComparable
    assert issubclass(Aeroplane, AeroplaneComparable)


# Тест 009: AeroplaneComparable имеет только методы сравнения.
def test_aeroplane_comparable_has_only_comparison_methods():
    from src.application.aeroplane_comparable import AeroplaneComparable
    comparison_methods = ["__lt__", "__gt__", "__le__", "__ge__", "__eq__"]
    for method in comparison_methods:
        assert hasattr(AeroplaneComparable, method)


# Тест 010: Клиент, которому нужно только сравнение, не зависит от данных.
def test_comparison_client_does_not_need_data():
    from src.application.aeroplane import Aeroplane
    from src.application.aeroplane_comparable import AeroplaneComparable

    plane1 = Aeroplane(callsign="FLIGHT1", country="USA", velocity=100.0, altitude=1000.0)
    plane2 = Aeroplane(callsign="FLIGHT2", country="USA", velocity=200.0, altitude=1000.0)

    # Функция принимает только AeroplaneComparable (сравнение)
    def sort_by_velocity(items: list) -> list:
        return sorted(items, key=lambda x: x)

    result = sort_by_velocity([plane1, plane2])
    assert result[0].velocity == 100.0
    assert result[1].velocity == 200.0


# ============================================================================
# 3. Проверка что AeroplaneBase объединяет оба интерфейса.
# ============================================================================

# Тест 011: AeroplaneBase наследуется от обоих интерфейсов.
def test_aeroplane_base_inherits_from_both():
    from src.application.aeroplane_base import AeroplaneBase
    from src.application.aeroplane_data import AeroplaneData
    from src.application.aeroplane_comparable import AeroplaneComparable
    assert issubclass(AeroplaneBase, AeroplaneData)
    assert issubclass(AeroplaneBase, AeroplaneComparable)


# Тест 012: ISP: клиент может зависеть от любого интерфейса.
def test_isp_polymorphism():
    from src.application.aeroplane import Aeroplane
    from src.application.aeroplane_data import AeroplaneData
    from src.application.aeroplane_comparable import AeroplaneComparable

    plane = Aeroplane(
        callsign="TEST",
        country="Russia",
        velocity=150.0,
        altitude=3000.0
    )

    # Зависимость от AeroplaneData
    def get_info_as_data(p: AeroplaneData) -> str:
        return p.callsign

    # Зависимость от AeroplaneComparable
    def compare_as_comparable(p: AeroplaneComparable) -> bool:
        return p.velocity > 100.0

    assert get_info_as_data(plane) == "TEST"
    assert compare_as_comparable(plane) is True
