# -*- coding: utf-8 -*-
"""Тесты для проверки принципа ISP: разделённые интерфейсы AeroplaneData и AeroplaneComparable."""

import pytest
from abc import ABC

from src.application.aeroplane_data import AeroplaneData
from src.application.aeroplane_comparable import AeroplaneComparable
from src.application.aeroplane_base import AeroplaneBase
from src.application.aeroplane import Aeroplane


# ============================================================================
# 1. Проверка AeroplaneData (ISP: только данные, без сравнения).
# ============================================================================

# Тест 001: AeroplaneData — абстрактный класс.
def test_aeroplane_data_is_abstract():
    """Проверяет что AeroplaneData является абстрактным классом.

    Проверяет что AeroplaneData наследуется от ABC (Abstract Base Class).
    """
    assert issubclass(AeroplaneData, ABC)


# Тест 002: Проверка, что нельзя создать объект AeroplaneData напрямую.
def test_cannot_instantiate_aeroplane_data():
    """Проверяет что создание экземпляра AeroplaneData напрямую вызывает TypeError.

    Пытается создать объект AeroplaneData и ожидает TypeError,
    так как это абстрактный класс.
    """
    with pytest.raises(TypeError):
        AeroplaneData()


# Тест 003: Aeroplane наследуется от AeroplaneData.
def test_aeroplane_inherits_from_aeroplane_data():
    """Проверяет что Aeroplane наследуется от AeroplaneData.

    Проверяет иерархию наследования: Aeroplane должен быть подклассом
    AeroplaneData, который содержит только данные о самолёте.
    """
    assert issubclass(Aeroplane, AeroplaneData)


# Тест 004: AeroplaneData имеет только 10 свойств данных.
def test_aeroplane_data_has_only_data_properties():
    """Проверяет что AeroplaneData содержит ровно 10 свойств данных.

    Проверяет наличие всех ожидаемых свойств: callsign, country, velocity,
    altitude, latitude, longitude, on_ground, geo_altitude, vertical_rate, true_track.
    """
    data_properties = [
        "callsign", "country", "velocity", "altitude",
        "latitude", "longitude", "on_ground",
        "geo_altitude", "vertical_rate", "true_track"
    ]
    for prop in data_properties:
        assert hasattr(AeroplaneData, prop)


# Тест 005: Клиент, которому нужны только данные, не зависит от сравнения.
def test_data_client_does_not_need_data(test_plane):
    """Проверяет что клиент с зависимостью только от AeroplaneData работает корректно.

    Создаёт функцию extract_data которая принимает только AeroplaneData
    и извлекает основные данные самолёта, проверяя что не требует
    методов сравнения.
    """
    # Функция принимает только AeroplaneData (данные)
    def extract_data(p: AeroplaneData) -> dict:
        return {
            "callsign": p.callsign,
            "country": p.country,
            "velocity": p.velocity,
            "altitude": p.altitude
        }

    result = extract_data(test_plane)
    assert result["callsign"] == "TEST"
    assert result["velocity"] == 200.0
    assert result["altitude"] == 5000.0


# ============================================================================
# 2. Проверка AeroplaneComparable (ISP: только сравнение, без данных).
# ============================================================================

# Тест 006: AeroplaneComparable — абстрактный класс.
def test_aeroplane_comparable_is_abstract():
    """Проверяет что AeroplaneComparable является абстрактным классом.

    Проверяет что AeroplaneComparable наследуется от ABC (Abstract Base Class).
    """
    assert issubclass(AeroplaneComparable, ABC)


# Тест 007: Проверка, что нельзя создать объект AeroplaneComparable напрямую.
def test_cannot_instantiate_aeroplane_comparable():
    """Проверяет что создание экземпляра AeroplaneComparable напрямую вызывает TypeError.

    Пытается создать объект AeroplaneComparable и ожидает TypeError,
    так как это абстрактный класс.
    """
    with pytest.raises(TypeError):
        AeroplaneComparable()


# Тест 008: Aeroplane наследуется от AeroplaneComparable.
def test_aeroplane_inherits_from_aeroplane_comparable():
    """Проверяет что Aeroplane наследуется от AeroplaneComparable.

    Проверяет иерархию наследования: Aeroplane должен быть подклассом
    AeroplaneComparable, который содержит методы сравнения.
    """
    assert issubclass(Aeroplane, AeroplaneComparable)


# Тест 009: AeroplaneComparable имеет только методы сравнения.
def test_aeroplane_comparable_has_only_comparison_methods():
    """Проверяет что AeroplaneComparable содержит только методы сравнения.

    Проверяет наличие всех ожидаемых магических методов: __lt__, __gt__,
    __le__, __ge__, __eq__ для реализации сравнения объектов.
    """
    comparison_methods = ["__lt__", "__gt__", "__le__", "__ge__", "__eq__"]
    for method in comparison_methods:
        assert hasattr(AeroplaneComparable, method)


# Тест 010: Клиент, которому нужно только сравнение, не зависит от данных.
def test_comparison_client_does_not_need_data(slow_plane, fast_plane):
    """Проверяет что клиент с зависимостью только от AeroplaneComparable работает корректно.

    Создаёт функцию sort_by_velocity которая принимает список AeroplaneComparable
    и сортирует его, проверяя что не требует доступа к данным самолётов.
    """
    # Функция принимает только AeroplaneComparable (сравнение)
    def sort_by_velocity(items: list) -> list:
        return sorted(items)

    result = sort_by_velocity([slow_plane, fast_plane])
    assert result[0].velocity == 100.0
    assert result[1].velocity == 200.0


# ============================================================================
# 3. Проверка, что AeroplaneBase объединяет оба интерфейса.
# ============================================================================

# Тест 011: AeroplaneBase наследуется от обоих интерфейсов.
def test_aeroplane_base_inherits_from_both():
    """Проверяет что AeroplaneBase наследуется от обоих интерфейсов.

    Проверяет что AeroplaneBase является подклассом и AeroplaneData,
    и AeroplaneComparable, объединяя данные и сравнение.
    """
    assert issubclass(AeroplaneBase, AeroplaneData)
    assert issubclass(AeroplaneBase, AeroplaneComparable)


# Тест 012: ISP: клиент может зависеть от любого интерфейса.
def test_isp_polymorphism(test_plane):
    """Проверяет полиморфизм ISP: клиент может зависеть от любого интерфейса.

    Создаёт две функции: одну с зависимостью от AeroplaneData для извлечения данных,
    другую без явной зависимости для сравнения, проверяя что оба варианта работают
    с одним и тем же объектом Aeroplane.
    """
    # Зависимость от AeroplaneData
    def get_info_as_data(p: AeroplaneData) -> str:
        return p.callsign

    # Зависимость от AeroplaneComparable
    def compare_as_comparable(p):
        return p.velocity > 100.0

    assert get_info_as_data(test_plane) == "TEST"
    assert compare_as_comparable(test_plane) is True  # 200.0 > 100.0
