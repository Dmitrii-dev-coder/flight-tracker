# -*- coding: utf-8 -*-
"""Тесты для модуля src.aeroplane."""

import pytest

from src.application.aeroplane import Aeroplane


# ============================================================================
# 0. Проверка класса: Aeroplane из модуля src.aeroplane.
# ============================================================================

# Тест 001: Проверка, что можно создать экземпляр Aeroplane.
def test_can_create_aeroplane(test_plane):
    """
    Проверяет, что объект Aeroplane создаётся без ошибок и является экземпляром класса.

    Использует фикстуру test_plane, которая возвращает готовый объект Aeroplane.
    """
    assert test_plane is not None
    assert isinstance(test_plane, Aeroplane)


# Тест 002: Проверка, что все атрибуты сохранены корректно.
def test_attributes_stored_correctly(detailed_plane):
    """
    Проверяет, что все 10 атрибутов самолёта сохранены с правильными значениями.

    Использует фикстуру detailed_plane, которая возвращает объект со всеми атрибутами.
    """
    assert detailed_plane.callsign == "SWR438A"
    assert detailed_plane.country == "Switzerland"
    assert detailed_plane.velocity == 189.7
    assert detailed_plane.altitude == 4267.2
    assert detailed_plane.latitude == 51.0888
    assert detailed_plane.longitude == -0.0168
    assert detailed_plane.on_ground is False
    assert detailed_plane.geo_altitude == 4282.44
    assert detailed_plane.vertical_rate == 14.63
    assert detailed_plane.true_track == 129.39


# Тест 003: Проверка, что приватные атрибуты доступны через _ (соглашение Python).
def test_private_attributes(test_plane):
    """
    Проверяет, что приватные атрибуты с одним подчёркиванием доступны внутри класса.

    В проекте используется _callsign (один подчёркивание) — это соглашение Python.
    Атрибут доступен, но это не рекомендуется использовать напрямую.
    """
    assert hasattr(test_plane, "_callsign")
    assert test_plane._callsign == "TEST"


# Тест 004: Проверка, что callsign не может быть пустым.
def test_empty_callsign_raises_error():
    """
    Проверяет, что создание самолёта с пустым позывным вызывает ValueError.

    Пустая строка "" не является допустимым позывным.
    """
    with pytest.raises(ValueError):
        Aeroplane(
            callsign="",
            country="Test",
            velocity=100.0,
            altitude=1000.0
        )


# Тест 005: Проверка, что velocity не может быть отрицательным.
def test_negative_velocity_raises_error():
    """
    Проверяет, что создание самолёта с отрицательной скоростью вызывает ValueError.

    Скорость не может быть меньше нуля.
    """
    with pytest.raises(ValueError):
        Aeroplane(
            callsign="TEST",
            country="Test",
            velocity=-50.0,
            altitude=1000.0
        )


# Тест 006: Проверка, что altitude не может быть отрицательным.
def test_negative_altitude_raises_error():
    """
    Проверяет, что создание самолёта с отрицательной высотой вызывает ValueError.

    Барометрическая высота не может быть меньше нуля.
    """
    with pytest.raises(ValueError):
        Aeroplane(
            callsign="TEST",
            country="Test",
            velocity=100.0,
            altitude=-500.0
        )


# Тест 007: Проверка, что geo_altitude не может быть отрицательным.
def test_negative_geo_altitude_raises_error():
    """
    Проверяет, что создание самолёта с отрицательной геометрической высотой вызывает ValueError.

    Геометрическая высота не может быть меньше нуля.
    """
    with pytest.raises(ValueError):
        Aeroplane(
            callsign="TEST",
            country="Test",
            velocity=100.0,
            altitude=1000.0,
            geo_altitude=-100.0
        )


# Тест 008: Проверка магического метода __str__.
def test_str_method(test_plane):
    """
    Проверяет, что метод __str__ возвращает строку с позывным самолёта.

    Метод __str__ используется для человекочитаемого представления объекта.
    """
    result = str(test_plane)
    assert isinstance(result, str)
    assert "TEST" in result


# Тест 009: Проверка магического метода __repr__.
def test_repr_method(test_plane):
    """
    Проверяет, что метод __repr__ возвращает строку с позывным самолёта.

    Метод __repr__ используется для детального представления объекта для отладки.
    """
    result = repr(test_plane)
    assert isinstance(result, str)
    assert "TEST" in result


# Тест 010: Проверка, что __eq__ сравнивает по callsign.
def test_eq_method():
    """
    Проверяет, что оператор == сравнивает самолёты по позывному.

    Два самолёта с одинаковым позывным считаются равными,
    даже если у них разные страна, скорость и высота.
    """
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


# Тест 011: Проверка, что __eq__ возвращает NotImplemented для несовместимых типов.
def test_eq_method_with_incompatible_type():
    """
    Проверяет, что оператор == возвращает False при сравнении с несовместимым типом.

    При сравнении самолёта со строкой метод __eq__ возвращает NotImplemented,
    что приводит к результату False.
    """
    plane = Aeroplane(
        callsign="UAL1621",
        country="United States",
        velocity=268.79,
        altitude=10203.18
    )
    assert plane != "UAL1621"
    assert plane != 123
    assert plane is not None


# Тест 012: Проверка что cast_to_object_list преобразует JSON в объекты.
def test_cast_to_object_list(json_data):
    """
    Проверяет, что статический метод cast_to_object_list корректно преобразует JSON-данные в объекты Aeroplane.

    JSON-данные содержат список списков с 17 полями о самолёте.
    Метод должен создать один объект Aeroplane с правильными атрибутами.
    """
    result = Aeroplane.cast_to_object_list(json_data)
    assert isinstance(result, list)
    assert len(result) == 1
    assert isinstance(result[0], Aeroplane)
    assert result[0].callsign == "SWR438A"
    assert result[0].country == "Switzerland"
    assert result[0].velocity == 189.7
    assert result[0].altitude == 4267.2


# Тест 013: Проверка что cast_to_object_list обрабатывает пустой список.
def test_cast_to_object_list_empty():
    """
    Проверяет, что cast_to_object_list возвращает пустой список при пустом входе.

    Пустой список JSON-данных не должен вызывать ошибок.
    """
    result = Aeroplane.cast_to_object_list([])
    assert isinstance(result, list)
    assert len(result) == 0


# Тест 014: Проверка что cast_to_object_list обрабатывает None элементы.
def test_cast_to_object_list_with_none(json_data_with_none):
    """
    Проверяет, что cast_to_object_list пропускает None элементы в списке данных.

    JSON-данные содержат None в начале списка. Метод должен создать объект только для валидной записи.
    """
    result = Aeroplane.cast_to_object_list(json_data_with_none)
    assert len(result) == 1
    assert isinstance(result[0], Aeroplane)


# Тест 015: Проверка, что самолёты без позывных пропускаются.
def test_cast_to_object_list_skips_empty_callsign(json_data_empty_callsign):
    """
    Проверяет, что самолёты с пустым или None позывным пропускаются при преобразовании.

    JSON-данные содержат три записи: одна с пустым позывным, одна с позывным FLT1, одна с None.
    Должен остаться только один самолёт с позывным FLT1.
    """
    result = Aeroplane.cast_to_object_list(json_data_empty_callsign)
    assert len(result) == 1
    assert result[0].callsign == "FLT1"


# Тест 016: Проверка, что отрицательная высота заменяется на 0.
def test_cast_to_object_list_negative_altitude(json_data_negative_altitude):
    """
    Проверяет, что отрицательная барометрическая высота заменяется на 0.0 при преобразовании.

    JSON-данные содержат два самолёта: один с отрицательной высотой (-121.92), другой с нормальной (6000.0).
    Первый должен получить высоту 0.0, второй — сохранить своё значение.
    """
    result = Aeroplane.cast_to_object_list(json_data_negative_altitude)
    assert len(result) == 2
    assert result[0].altitude == 0.0
    assert result[1].altitude == 6000.0


# Тест 017: Проверка, что отрицательная geo_altitude заменяется на 0.
def test_cast_to_object_list_negative_geo_altitude(json_data_negative_geo_altitude):
    """
    Проверяет, что отрицательная геометрическая высота заменяется на 0.0 при преобразовании.

    JSON-данные содержат два самолёта: один с отрицательной geo_altitude (-7.62), другой с нормальной (6000.0).
    Первый должен получить geo_altitude 0.0, второй — сохранить своё значение.
    """
    result = Aeroplane.cast_to_object_list(json_data_negative_geo_altitude)
    assert len(result) == 2
    assert result[0].geo_altitude == 0.0
    assert result[1].geo_altitude == 6000.0
