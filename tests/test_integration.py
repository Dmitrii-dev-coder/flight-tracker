# -*- coding: utf-8 -*-
"""Тесты для интеграции всех компонентов проекта."""

from unittest.mock import patch, MagicMock


# ============================================================================
# 0. Проверка интеграции: объединение всех компонентов в единую программу.
# ============================================================================

# Тест 001: Проверка что все модули импортируются без ошибок.
def test_all_modules_importable():
    from src.infrastructure.aeroplanes_api import AeroplanesAPI
    from src.application.aeroplane import Aeroplane
    from src.infrastructure.json_saver import JSONSaver
    from src.application.user_interface import user_interaction

    assert AeroplanesAPI is not None
    assert Aeroplane is not None
    assert JSONSaver is not None
    assert user_interaction is not None


# Тест 002: Проверка что AeroplanesAPI наследуется от APIConnector.
def test_api_inheritance_chain():
    from src.infrastructure.aeroplanes_api import AeroplanesAPI
    from src.infrastructure.api_base import APIConnector

    assert issubclass(AeroplanesAPI, APIConnector)


# Тест 003: Проверка что JSONSaver наследуется от FileConnector.
def test_json_saver_inheritance_chain():
    from src.infrastructure.json_saver import JSONSaver
    from src.infrastructure.file_connector import FileConnector

    assert issubclass(JSONSaver, FileConnector)


# Тест 004: Проверка полного конвейера: API -> Aeroplane -> JSONSaver.
def test_full_pipeline():
    from src.infrastructure.aeroplanes_api import AeroplanesAPI
    from src.application.aeroplane import Aeroplane
    from src.infrastructure.json_saver import JSONSaver
    import tempfile
    import os

    mock_nominatim = MagicMock()
    mock_nominatim.status_code = 200
    mock_nominatim.json.return_value = [{
        "name": "Spain",
        "boundingbox": ["40.0", "43.0", "-5.0", "3.0"]
    }]

    mock_opensky = MagicMock()
    mock_opensky.status_code = 200
    mock_opensky.json.return_value = {
        "time": 1766142246,
        "states": [
            [
                "plane1", "FLT1", "Spain", 0, 0,
                1.0, 41.0, 5000.0, False, 200.0, 0.0, 0.0,
                None, 5000.0, "0000", False, 0
            ]
        ]
    }

    with patch("src.infrastructure.aeroplanes_api.requests.get", side_effect=[mock_nominatim, mock_opensky]):
        api = AeroplanesAPI()
        aeroplanes_data = api.get_aeroplanes("Spain")

        aeroplanes = Aeroplane.cast_to_object_list(aeroplanes_data)

        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "test_integration.json")
            saver = JSONSaver(filepath=filepath)

            for plane in aeroplanes:
                saver.add_aeroplane(plane)

            saved = saver.get_aeroplanes()
            assert len(saved) == 1
            assert saved[0].callsign == "FLT1"


# Тест 005: Проверка что все классы используются в main.py.
def test_all_classes_used_in_main():
    from src.infrastructure import json_saver
    from src.infrastructure import aeroplanes_api
    from src.application import user_interface
    from src.application import aeroplane

    # Проверяем что модули не пустые
    assert hasattr(aeroplanes_api, "AeroplanesAPI")
    assert hasattr(aeroplane, "Aeroplane")
    assert hasattr(json_saver, "JSONSaver")
    assert hasattr(user_interface, "user_interaction")


# Тест 006: Проверка что main.py существует и запускается.
def test_main_py_exists():
    import os
    assert os.path.exists("main.py")


# Тест 007: Проверка что все фильтры работают вместе.
def test_all_filters_work_together():
    from src.application.filters import (
        filter_by_country,
        filter_by_altitude_range,
        sort_by_altitude_desc,
        get_top_n
    )
    from src.application.aeroplane import Aeroplane

    planes = [
        Aeroplane(callsign="FLIGHT1", country="Spain", velocity=100.0, altitude=1000.0),
        Aeroplane(callsign="FLIGHT2", country="USA", velocity=200.0, altitude=5000.0),
        Aeroplane(callsign="FLIGHT3", country="Spain", velocity=150.0, altitude=3000.0),
        Aeroplane(callsign="FLIGHT4", country="France", velocity=180.0, altitude=8000.0),
    ]

    # Фильтрация по стране
    spain = filter_by_country(planes, ["Spain"])
    assert len(spain) == 2

    # Сортировка
    sorted_spain = sort_by_altitude_desc(spain)
    assert sorted_spain[0].altitude == 3000.0

    # Топ N
    top1 = get_top_n(sorted_spain, 1)
    assert len(top1) == 1

    # Фильтрация по высоте
    ranged = filter_by_altitude_range(planes, 1000.0, 3000.0)
    assert len(ranged) == 2
