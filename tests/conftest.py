# -*- coding: utf-8 -*-
"""
Конфигурация pytest — общие фикстуры для всех тестов.

Фикстуры позволяют избежать дублирования кода и упростить поддержку тестов.
"""

import pytest


# ============================================================================
# Фикстуры для Aeroplane
# ============================================================================

@pytest.fixture
def test_plane():
    """
    Базовый объект Aeroplane для тестов.

    Returns:
        Объект Aeroplane с минимальными параметрами.
    """
    from src.application.aeroplane import Aeroplane
    return Aeroplane(
        callsign="TEST",
        country="Russia",
        velocity=200.0,
        altitude=5000.0
    )


@pytest.fixture
def detailed_plane():
    """
    Объект Aeroplane со всеми атрибутами для тестов.

    Returns:
        Объект Aeroplane с полными параметрами.
    """
    from src.application.aeroplane import Aeroplane
    return Aeroplane(
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


@pytest.fixture
def slow_plane():
    """
    Медленный самолёт для тестов сравнения.

    Returns:
        Объект Aeroplane с низкой скоростью.
    """
    from src.application.aeroplane import Aeroplane
    return Aeroplane(callsign="SLOW", country="USA", velocity=100.0, altitude=1000.0)


@pytest.fixture
def fast_plane():
    """
    Быстрый самолёт для тестов сравнения.

    Returns:
        Объект Aeroplane с высокой скоростью.
    """
    from src.application.aeroplane import Aeroplane
    return Aeroplane(callsign="FAST", country="USA", velocity=200.0, altitude=1000.0)


@pytest.fixture
def planes_for_comparison():
    """
    Два самолёта для тестов сравнения.

    Returns:
        Кортеж (slow_plane, fast_plane).
    """
    from src.application.aeroplane import Aeroplane
    slow = Aeroplane(callsign="SLOW", country="USA", velocity=100.0, altitude=1000.0)
    fast = Aeroplane(callsign="FAST", country="USA", velocity=200.0, altitude=1000.0)
    return slow, fast


# ============================================================================
# Фикстуры для данных JSON
# ============================================================================

@pytest.fixture
def json_data():
    """
    Пример JSON-данных от OpenSky API.

    Returns:
        Список списков с данными о самолётах.
    """
    return [
        [
            "4b1812", "SWR438A ", "Switzerland", 1766166618, 1766166618,
            -0.0168, 51.0888, 4267.2, False, 189.7, 129.39, 14.63,
            None, 4282.44, "2061", False, 0
        ]
    ]


@pytest.fixture
def json_data_multiple():
    """
    Несколько самолётов в формате JSON.

    Returns:
        Список списков с данными о самолётах.
    """
    return [
        ["4b1812", "SWR438A ", "Switzerland", 1766166618, 1766166618,
         -0.0168, 51.0888, 4267.2, False, 189.7, 129.39, 14.63,
         None, 4282.44, "2061", False, 0],
        ["4b1813", "TEST", "Test", 0, 0, 0.0, 0.0, 1000.0, False, 100.0, 0.0, 0.0,
         None, 1000.0, "0000", False, 0]
    ]


@pytest.fixture
def json_data_with_none():
    """
    JSON-данные с None элементами.

    Returns:
        Список списков с данными о самолётах.
    """
    return [None, ["4b1812", "TEST", "Test", 0, 0, 0.0, 0.0,
                   1000.0, False, 100.0, 0.0, 0.0, None,
                   1000.0, "0000", False, 0]]


@pytest.fixture
def json_data_empty_callsign():
    """
    JSON-данные с пустым позывным.

    Returns:
        Список списков с данными о самолётах.
    """
    return [
        ["plane1", "", "Spain", 0, 0, 1.0, 41.0, 5000.0, False, 200.0, 0.0, 0.0, None, 5000.0, "0000", False, 0],
        ["plane2", "FLT1", "Spain", 0, 0, 2.0, 42.0, 6000.0, False, 250.0, 90.0, 0.0, None, 6000.0, "0001", False, 0],
        ["plane3", None, "Spain", 0, 0, 3.0, 43.0, 7000.0, False, 300.0, 180.0, 10.0, None, 7000.0, "0002", False, 0]
    ]


@pytest.fixture
def json_data_negative_altitude():
    """
    JSON-данные с отрицательной высотой.

    Returns:
        Список списков с данными о самолётах.
    """
    return [
        ["plane1", "FLT1", "Spain", 0, 0, 1.0, 41.0, -121.92, False, 200.0, 0.0, 0.0, None, 5000.0, "0000", False, 0],
        ["plane2", "FLT2", "Spain", 0, 0, 2.0, 42.0, 6000.0, False, 250.0, 90.0, 0.0, None, 6000.0, "0001", False, 0]
    ]


@pytest.fixture
def json_data_negative_geo_altitude():
    """
    JSON-данные с отрицательной геометрической высотой.

    Returns:
        Список списков с данными о самолётах.
    """
    return [
        ["plane1", "FLT1", "Spain", 0, 0, 1.0, 41.0, 5000.0, False, 200.0, 0.0, 0.0, None, -7.62, "0000", False, 0],
        ["plane2", "FLT2", "Spain", 0, 0, 2.0, 42.0, 6000.0, False, 250.0, 90.0, 0.0, None, 6000.0, "0001", False, 0]
    ]


# ============================================================================
# Фикстуры для JSONSaver
# ============================================================================

@pytest.fixture
def json_saver(tmp_path):
    """
    Фикстура для создания JSONSaver с временным файлом.

    Args:
        tmp_path: Фикстура pytest для временных файлов.

    Returns:
        Объект JSONSaver с временным файлом.
    """
    from src.infrastructure.json_saver import JSONSaver
    filepath = tmp_path / "test_aeroplanes.json"
    return JSONSaver(filepath=str(filepath))


@pytest.fixture
def test_planes():
    """
    Два тестовых самолёта для работы с JSONSaver.

    Returns:
        Список объектов Aeroplane.
    """
    from src.application.aeroplane import Aeroplane
    return [
        Aeroplane(callsign="FLIGHT1", country="USA", velocity=100.0, altitude=1000.0),
        Aeroplane(callsign="FLIGHT2", country="Spain", velocity=200.0, altitude=2000.0),
    ]


@pytest.fixture
def three_test_planes():
    """
    Три тестовых самолёта для работы с JSONSaver.

    Returns:
        Список объектов Aeroplane.
    """
    from src.application.aeroplane import Aeroplane
    return [
        Aeroplane(callsign="FLIGHT1", country="USA", velocity=100.0, altitude=1000.0),
        Aeroplane(callsign="FLIGHT2", country="Spain", velocity=200.0, altitude=2000.0),
        Aeroplane(callsign="FLIGHT3", country="Spain", velocity=150.0, altitude=1500.0),
    ]


# ============================================================================
# Фикстуры для API
# ============================================================================

@pytest.fixture
def mock_nominatim_response():
    """
    Моковый ответ от Nominatim API.

    Returns:
        Словарь с координатами страны.
    """
    return [{
        "boundingbox": ["35.0", "70.0", "27.0", "180.0"]
    }]


@pytest.fixture
def mock_opensky_response():
    """
    Моковый ответ от OpenSky API.

    Returns:
        Словарь с данными о самолётах.
    """
    return {
        "states": [
            ["4b1812", "SWR438A", "Switzerland", 1766166618, 1766166618,
             -0.0168, 51.0888, 4267.2, False, 189.7, 129.39, 14.63,
             None, 4282.44, "2061", False, 0],
            ["4b1813", "TEST", "Test", 0, 0, 0.0, 0.0, 1000.0, False, 100.0, 0.0, 0.0,
             None, 1000.0, "0000", False, 0]
        ]
    }


# ============================================================================
# Фикстуры для фильтрации
# ============================================================================

@pytest.fixture
def planes_for_filtering():
    """
    Самолёты для тестов фильтрации.

    Возвращает 4 самолёта:
    - FLIGHT1: USA, 1000м
    - FLIGHT2: Spain, 2000м
    - FLIGHT3: Spain, 3000м
    - FLIGHT4: France, 8000м

    Returns:
        Список объектов Aeroplane.
    """
    from src.application.aeroplane import Aeroplane
    return [
        Aeroplane(callsign="FLIGHT1", country="USA", velocity=100.0, altitude=1000.0),
        Aeroplane(callsign="FLIGHT2", country="Spain", velocity=200.0, altitude=2000.0),
        Aeroplane(callsign="FLIGHT3", country="Spain", velocity=150.0, altitude=3000.0),
        Aeroplane(callsign="FLIGHT4", country="France", velocity=180.0, altitude=8000.0),
    ]


@pytest.fixture
def planes_for_sorting():
    """
    Самолёты для тестов сортировки.

    Возвращает 3 самолёта с разными высотами:
    - SLOW: 1000м
    - MEDIUM: 3000м
    - FAST: 5000м

    Returns:
        Список объектов Aeroplane.
    """
    from src.application.aeroplane import Aeroplane
    return [
        Aeroplane(callsign="SLOW", country="USA", velocity=100.0, altitude=1000.0),
        Aeroplane(callsign="MEDIUM", country="USA", velocity=200.0, altitude=3000.0),
        Aeroplane(callsign="FAST", country="USA", velocity=300.0, altitude=5000.0),
    ]
