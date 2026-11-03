# -*- coding: utf-8 -*-
"""Тесты для модуля src.json_saver."""

import json
import os
import shutil

import pytest

from src.infrastructure.json_saver import JSONSaver
from src.application.aeroplane import Aeroplane


# ============================================================================
# 0. Проверка класса: JSONSaver из модуля src.json_saver.
# ============================================================================

# Тест 001: Проверка, что можно создать экземпляр JSONSaver.
def test_can_create_json_saver():
    """Проверяет что можно создать экземпляр JSONSaver по умолчанию.

    Создаёт JSONSaver без параметров и проверяет что объект успешно создан.
    """
    saver = JSONSaver()
    assert saver is not None


# Тест 002: Проверка, что add_aeroplane сохраняет данные в JSON.
def test_add_aeroplane_saves_to_json(json_saver, test_plane):
    """Проверяет что add_aeroplane корректно сохраняет самолёт в JSON-файл.

    Добавляет test_plane через json_saver, проверяет что файл создан,
    содержит один элемент и его callsign равен "TEST", country равен "Russia".
    """
    json_saver.add_aeroplane(test_plane)
    filepath = json_saver.filepath

    assert os.path.exists(filepath)

    with open(filepath, encoding="utf-8") as f:
        data = json.load(f)

    assert len(data) == 1
    assert data[0]["callsign"] == "TEST"
    assert data[0]["country"] == "Russia"


# Тест 003: Проверка, что add_aeroplane добавляет к существующим данным.
def test_add_aeroplane_appends_to_existing(json_saver, test_planes):
    """Проверяет что add_aeroplane добавляет данные к существующим.

    Добавляет два самолёта последовательно и проверяет что в файле
    оба элемента с правильными callsign "FLIGHT1" и "FLIGHT2".
    """
    json_saver.add_aeroplane(test_planes[0])
    json_saver.add_aeroplane(test_planes[1])

    filepath = json_saver.filepath
    with open(filepath, encoding="utf-8") as f:
        data = json.load(f)

    assert len(data) == 2
    assert data[0]["callsign"] == "FLIGHT1"
    assert data[1]["callsign"] == "FLIGHT2"


# Тест 004: Проверка, что delete_aeroplane удаляет данные из JSON.
def test_delete_aeroplane_removes_from_json(json_saver, test_planes):
    """Проверяет что delete_aeroplane корректно удаляет самолёт из файла.

    Добавляет два самолёта, удаляет первый и проверяет что в файле
    остался только второй самолёт с callsign "FLIGHT2".
    """
    json_saver.add_aeroplane(test_planes[0])
    json_saver.add_aeroplane(test_planes[1])
    json_saver.delete_aeroplane(test_planes[0])

    filepath = json_saver.filepath
    with open(filepath, encoding="utf-8") as f:
        data = json.load(f)

    assert len(data) == 1
    assert data[0]["callsign"] == "FLIGHT2"


# Тест 005: Проверка, что удаление несуществующего самолёта не вызывает ошибок.
def test_delete_aeroplane_handles_missing(json_saver, test_plane):
    """Проверяет что удаление несуществующего самолёта не вызывает ошибок.

    Пытается удалить test_plane который не был добавлен и проверяет,
    что файл не создан или пуст.
    """
    json_saver.delete_aeroplane(test_plane)

    filepath = json_saver.filepath
    with open(filepath, encoding="utf-8") as f:
        data = json.load(f)

    assert len(data) == 0


# Тест 006: Проверка, что get_aeroplanes возвращает все данные.
def test_get_aeroplanes_returns_all(json_saver, test_planes):
    """Проверяет что get_aeroplanes возвращает все добавленные самолёты.

    Добавляет два самолёта и проверяет что get_aeroplanes возвращает
    список длиной 2.
    """
    json_saver.add_aeroplane(test_planes[0])
    json_saver.add_aeroplane(test_planes[1])

    result = json_saver.get_aeroplanes()
    assert len(result) == 2


# Тест 007: Проверка, что get_aeroplanes фильтрует по стране.
def test_get_aeroplanes_filters_by_country(json_saver, three_test_planes):
    """Проверяет что get_aeroplanes может фильтровать по стране.

    Добавляет три самолёта (USA, Spain, Spain) и проверяет что
    фильтрация по country="Spain" возвращает ровно 2 самолёта.
    """
    for plane in three_test_planes:
        json_saver.add_aeroplane(plane)

    result = json_saver.get_aeroplanes(country="Spain")
    assert len(result) == 2
    for plane in result:
        assert plane.country == "Spain"


# Тест 008: Проверка, что get_aeroplanes возвращает пустой список при отсутствии данных.
def test_get_aeroplanes_empty_file(json_saver):
    """Проверяет что get_aeroplanes возвращает пустой список для пустого файла.

    Вызывает get_aeroplanes без добавления каких-либо самолётов
    и проверяет что возвращается пустой список.
    """
    result = json_saver.get_aeroplanes()
    assert isinstance(result, list)
    assert len(result) == 0


# Тест 009: Проверка, что get_aeroplanes фильтрует по скорости.
def test_get_aeroplanes_filters_by_velocity(json_saver, planes_for_filtering):
    """Проверяет что get_aeroplanes может фильтровать по скорости.

    Добавляет 4 самолёта с разными скоростями и проверяет что
    фильтрация по velocity=200.0 возвращает ровно 1 самолёт.
    """
    for plane in planes_for_filtering:
        json_saver.add_aeroplane(plane)

    result = json_saver.get_aeroplanes(velocity=200.0)
    assert len(result) == 1
    assert result[0].velocity == 200.0


# Тест 010: Проверка, что get_aeroplanes фильтрует по высоте.
def test_get_aeroplanes_filters_by_altitude(json_saver):
    """Проверяет что get_aeroplanes может фильтровать по высоте.

    Создаёт два самолёта с разными высотами (1000м и 5000м), добавляет их
    и проверяет что фильтрация по altitude=5000.0 возвращает 1 самолёт.
    """
    plane1 = Aeroplane(callsign="FLIGHT1", country="USA", velocity=100.0, altitude=1000.0)
    plane2 = Aeroplane(callsign="FLIGHT2", country="Spain", velocity=200.0, altitude=5000.0)

    json_saver.add_aeroplane(plane1)
    json_saver.add_aeroplane(plane2)

    result = json_saver.get_aeroplanes(altitude=5000.0)
    assert len(result) == 1
    assert result[0].altitude == 5000.0


# Тест 011: Проверка, что get_aeroplanes обрабатывает отсутствие файла.
def test_get_aeroplanes_handles_missing_file(json_saver):
    """Проверяет что get_aeroplanes корректно обрабатывает отсутствие файла.

    Вызывает get_aeroplanes без создания файла и проверяет что
    возвращается пустой список без ошибок.
    """
    result = json_saver.get_aeroplanes()
    assert isinstance(result, list)
    assert len(result) == 0


# Тест 012: Проверка, что добавление не-объекта Aeroplane вызывает AttributeError.
def test_add_aeroplane_handles_invalid_object(json_saver):
    """Проверяет что добавление не-объекта Aeroplane вызывает AttributeError.

    Пытается добавить обычный object через add_aeroplane и ожидает
    AttributeError так как у объекта нет необходимых атрибутов Aeroplane.
    """
    invalid_object = object()
    with pytest.raises(AttributeError):
        json_saver.add_aeroplane(invalid_object)


# Тест 013: Проверка, что удаление не-объекта Aeroplane вызывает AttributeError.
def test_delete_aeroplane_handles_invalid_object(json_saver, test_plane):
    """Проверяет что удаление не-объекта Aeroplane вызывает AttributeError.

    Добавляет тестовый самолёт, затем пытается удалить обычный object
    и ожидает AttributeError так как у объекта нет необходимых атрибутов.
    """
    json_saver.add_aeroplane(test_plane)

    invalid_object = object()
    with pytest.raises(AttributeError):
        json_saver.delete_aeroplane(invalid_object)


# Тест 014: Проверка, что save_data обрабатывает ошибку записи.
def test_save_data_handles_io_error(test_plane, tmp_path):
    """Проверяет что save_data корректно обрабатывает ошибки записи в файл.

    Создаёт JSONSaver с путём в несуществующую директорию, удаляет директорию
    и проверяет что add_aeroplane вызывает IOError при невозможности записи.
    """
    filepath = str(tmp_path / "readonly" / "test.json")
    saver = JSONSaver(filepath=filepath)

    # Удалить папку, чтобы вызвать ошибку записи
    shutil.rmtree(os.path.dirname(filepath))

    with pytest.raises(IOError):
        saver.add_aeroplane(test_plane)


# Тест 015: Проверка, что _load_data обрабатывает некорректный JSON.
def test_load_data_handles_invalid_json(tmp_path):
    """Проверяет что _load_data обрабатывает некорректный JSON.

    Создает JSONSaver с файлом содержащим некорректный JSON,
    и проверяет что _load_data вызывает json.JSONDecodeError.
    """
    filepath = str(tmp_path / "invalid.json")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("некорректный json {")

    saver = JSONSaver(filepath=filepath)

    with pytest.raises(json.JSONDecodeError):
        saver._load_data()


# Тест 016: Проверка, что get_aeroplanes обрабатывает некорректный JSON.
def test_get_aeroplanes_handles_invalid_json(tmp_path):
    """Проверяет что get_aeroplanes обрабатывает некорректный JSON.

    Создает JSONSaver с файлом содержащим некорректный JSON,
    и проверяет что get_aeroplanes возвращает пустой список.
    """
    filepath = str(tmp_path / "invalid.json")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("некорректный json {")

    saver = JSONSaver(filepath=filepath)
    result = saver.get_aeroplanes()

    assert isinstance(result, list)
    assert len(result) == 0


# Тест 017: Проверка, что get_aeroplanes обрабатывает некорректные данные самолета.
def test_get_aeroplanes_handles_invalid_plane_data(json_saver):
    """Проверяет что get_aeroplanes обрабатывает некорректные данные самолета.

    Добавляет некорректные данные (отсутствует callsign) и проверяет,
    что get_aeroplanes возвращает пустой список.
    """
    filepath = json_saver.filepath
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump([{"invalid_key": "invalid_value"}], f)

    result = json_saver.get_aeroplanes()
    assert isinstance(result, list)
    assert len(result) == 0
