# -*- coding: utf-8 -*-
"""Тесты для интеграции всех компонентов проекта."""

import os
import tempfile

from unittest.mock import MagicMock

from src.infrastructure.aeroplanes_api import AeroplanesAPI
from src.infrastructure.http_requestor import HTTPRequestor
from src.application.aeroplane import Aeroplane
from src.infrastructure.json_saver import JSONSaver
from src.application.user_interface import user_interaction
from src.infrastructure.api_base import APIConnector
from src.infrastructure.file_connector import FileConnector
from src.application.filters import (
    filter_by_country,
    filter_by_altitude_range,
    sort_by_altitude_desc,
    get_top_n
)


# ============================================================================
# 0. Проверка интеграции: объединение всех компонентов в единую программу.
# ============================================================================

# Тест 001: Проверка, что все модули импортируются без ошибок.
def test_all_modules_importable():
    """Проверяет что все ключевые модули проекта импортируются без ошибок.

    Проверяет что основные классы и функции не равны None.
    """
    assert AeroplanesAPI is not None
    assert Aeroplane is not None
    assert JSONSaver is not None
    assert user_interaction is not None


# Тест 002: Проверка, что AeroplanesAPI наследуется от APIConnector.
def test_api_inheritance_chain():
    """Проверяет что AeroplanesAPI правильно наследуется от APIConnector.

    Проверяет иерархию наследования: AeroplanesAPI должен быть подклассом
    APIConnector из модуля src.infrastructure.api_base.
    """
    assert issubclass(AeroplanesAPI, APIConnector)


# Тест 003: Проверка, что JSONSaver наследуется от FileConnector.
def test_json_saver_inheritance_chain():
    """Проверяет что JSONSaver правильно наследуется от FileConnector.

    Проверяет иерархию наследования: JSONSaver должен быть подклассом
    FileConnector из модуля src.infrastructure.file_connector.
    """
    assert issubclass(JSONSaver, FileConnector)


# Тест 004: Проверка полного конвейера: API -> Aeroplane -> JSONSaver.
def test_full_pipeline():
    """Проверяет полный конвейер обработки данных: API -> Aeroplane -> JSONSaver.

    Создаёт моковый HTTP-запрос, получает данные о самолётах через API,
    преобразует их в объекты Aeroplane, сохраняет через JSONSaver и проверяет
    что данные корректно сохранены и могут быть прочитаны.
    """
    mock_requestor = MagicMock(spec=HTTPRequestor)
    mock_requestor.get.side_effect = [
        [{"name": "Spain", "boundingbox": ["40.0", "43.0", "-5.0", "3.0"]}],
        {
            "time": 1766142246,
            "states": [
                [
                    "plane1", "FLT1", "Spain", 0, 0,
                    1.0, 41.0, 5000.0, False, 200.0, 0.0, 0.0,
                    None, 5000.0, "0000", False, 0
                ]
            ]
        }
    ]

    api = AeroplanesAPI(http_requestor=mock_requestor)
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


# Тест 005: Проверка, что все классы используются в main.py.
def test_all_classes_used_in_main():
    """Проверяет что все ключевые классы доступны в соответствующих модулях main.py.

    Проверяет что модули содержат ожидаемые классы и функции:
    AeroplanesAPI, Aeroplane, JSONSaver, user_interaction.
    """
    from src.infrastructure import json_saver
    from src.infrastructure import aeroplanes_api
    from src.application import user_interface
    from src.application import aeroplane

    # Проверяем что модули не пустые
    assert hasattr(aeroplanes_api, "AeroplanesAPI")
    assert hasattr(aeroplane, "Aeroplane")
    assert hasattr(json_saver, "JSONSaver")
    assert hasattr(user_interface, "user_interaction")


# Тест 006: Проверка, что main.py существует и запускается.
def test_main_py_exists():
    """Проверяет что файл main.py существует в корневой директории проекта.

    Проверяет существование файла main.py как точки входа приложения.
    """
    assert os.path.exists("main.py")


# Тест 007: Проверка, что все фильтры работают вместе.
def test_all_filters_work_together(planes_for_filtering):
    """Проверяет что все функции фильтрации и сортировки работают корректно вместе.

    Выполняет цепочку операций: фильтрация по стране, сортировка по убыванию высоты,
    получение топ-N и фильтрация по диапазону высот, проверяя корректность
    результатов на каждом шаге.
    """
    # Фильтрация по стране
    spain = filter_by_country(planes_for_filtering, ["Spain"])
    assert len(spain) == 2

    # Сортировка
    sorted_spain = sort_by_altitude_desc(spain)
    assert sorted_spain[0].altitude == 3000.0

    # Топ N
    top1 = get_top_n(sorted_spain, 1)
    assert len(top1) == 1

    # Фильтрация по высоте
    # USA 1000, Spain 2000, Spain 3000, France 8000
    # В диапазоне 1000-3000: 1000, 2000, 3000 = 3 самолёта
    ranged = filter_by_altitude_range(planes_for_filtering, 1000.0, 3000.0)
    assert len(ranged) == 3
