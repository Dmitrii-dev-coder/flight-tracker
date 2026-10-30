# -*- coding: utf-8 -*-
"""Тесты для модуля src.json_saver."""

import json
import os
import tempfile
import pytest


# ============================================================================
# 0. Проверка класса: JSONSaver из модуля src.json_saver.
# ============================================================================

# Тест 001: Проверка что можно создать экземпляр JSONSaver.
def test_can_create_json_saver():
    from src.infrastructure.json_saver import JSONSaver
    saver = JSONSaver()
    assert saver is not None


# Тест 002: Проверка что add_aeroplane сохраняет данные в JSON.
def test_add_aeroplane_saves_to_json():
    from src.infrastructure.json_saver import JSONSaver
    from src.application.aeroplane import Aeroplane

    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = os.path.join(tmpdir, "test_aeroplanes.json")
        saver = JSONSaver(filepath=filepath)

        plane = Aeroplane(
            callsign="TEST123",
            country="Spain",
            velocity=268.79,
            altitude=10203.18
        )
        saver.add_aeroplane(plane)

        assert os.path.exists(filepath)

        with open(filepath, encoding="utf-8") as f:
            data = json.load(f)

        assert len(data) == 1
        assert data[0]["callsign"] == "TEST123"
        assert data[0]["country"] == "Spain"


# Тест 003: Проверка что add_aeroplane добавляет к существующим данным.
def test_add_aeroplane_appends_to_existing():
    from src.infrastructure.json_saver import JSONSaver
    from src.application.aeroplane import Aeroplane

    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = os.path.join(tmpdir, "test_aeroplanes.json")
        saver = JSONSaver(filepath=filepath)

        plane1 = Aeroplane(callsign="FLIGHT1", country="USA", velocity=100.0, altitude=1000.0)
        plane2 = Aeroplane(callsign="FLIGHT2", country="Spain", velocity=200.0, altitude=2000.0)

        saver.add_aeroplane(plane1)
        saver.add_aeroplane(plane2)

        with open(filepath, encoding="utf-8") as f:
            data = json.load(f)

        assert len(data) == 2
        assert data[0]["callsign"] == "FLIGHT1"
        assert data[1]["callsign"] == "FLIGHT2"


# Тест 004: Проверка что delete_aeroplane удаляет данные из JSON.
def test_delete_aeroplane_removes_from_json():
    from src.infrastructure.json_saver import JSONSaver
    from src.application.aeroplane import Aeroplane

    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = os.path.join(tmpdir, "test_aeroplanes.json")
        saver = JSONSaver(filepath=filepath)

        plane1 = Aeroplane(callsign="DELETE_ME", country="USA", velocity=100.0, altitude=1000.0)
        plane2 = Aeroplane(callsign="KEEP_ME", country="Spain", velocity=200.0, altitude=2000.0)

        saver.add_aeroplane(plane1)
        saver.add_aeroplane(plane2)
        saver.delete_aeroplane(plane1)

        with open(filepath, encoding="utf-8") as f:
            data = json.load(f)

        assert len(data) == 1
        assert data[0]["callsign"] == "KEEP_ME"


# Тест 005: Проверка что delete_aeroplane обрабатывает отсутствие самолёта.
def test_delete_aeroplane_handles_missing():
    from src.infrastructure.json_saver import JSONSaver
    from src.application.aeroplane import Aeroplane

    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = os.path.join(tmpdir, "test_aeroplanes.json")
        saver = JSONSaver(filepath=filepath)

        plane = Aeroplane(callsign="TEST", country="USA", velocity=100.0, altitude=1000.0)
        saver.delete_aeroplane(plane)

        with open(filepath, encoding="utf-8") as f:
            data = json.load(f)

        assert len(data) == 0


# Тест 006: Проверка что get_aeroplanes возвращает все данные.
def test_get_aeroplanes_returns_all():
    from src.infrastructure.json_saver import JSONSaver
    from src.application.aeroplane import Aeroplane

    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = os.path.join(tmpdir, "test_aeroplanes.json")
        saver = JSONSaver(filepath=filepath)

        plane1 = Aeroplane(callsign="FLIGHT1", country="USA", velocity=100.0, altitude=1000.0)
        plane2 = Aeroplane(callsign="FLIGHT2", country="Spain", velocity=200.0, altitude=2000.0)

        saver.add_aeroplane(plane1)
        saver.add_aeroplane(plane2)

        result = saver.get_aeroplanes()
        assert len(result) == 2


# Тест 007: Проверка что get_aeroplanes фильтрует по стране.
def test_get_aeroplanes_filters_by_country():
    from src.infrastructure.json_saver import JSONSaver
    from src.application.aeroplane import Aeroplane

    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = os.path.join(tmpdir, "test_aeroplanes.json")
        saver = JSONSaver(filepath=filepath)

        plane1 = Aeroplane(callsign="FLIGHT1", country="USA", velocity=100.0, altitude=1000.0)
        plane2 = Aeroplane(callsign="FLIGHT2", country="Spain", velocity=200.0, altitude=2000.0)
        plane3 = Aeroplane(callsign="FLIGHT3", country="Spain", velocity=150.0, altitude=1500.0)

        saver.add_aeroplane(plane1)
        saver.add_aeroplane(plane2)
        saver.add_aeroplane(plane3)

        result = saver.get_aeroplanes(country="Spain")
        assert len(result) == 2
        for plane in result:
            assert plane.country == "Spain"


# Тест 008: Проверка что get_aeroplanes возвращает пустой список при отсутствии данных.
def test_get_aeroplanes_empty_file():
    from src.infrastructure.json_saver import JSONSaver

    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = os.path.join(tmpdir, "test_aeroplanes.json")
        saver = JSONSaver(filepath=filepath)

        result = saver.get_aeroplanes()
        assert isinstance(result, list)
        assert len(result) == 0


# Тест 009: Проверка что get_aeroplanes фильтрует по скорости.
def test_get_aeroplanes_filters_by_velocity():
    from src.infrastructure.json_saver import JSONSaver
    from src.application.aeroplane import Aeroplane

    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = os.path.join(tmpdir, "test_aeroplanes.json")
        saver = JSONSaver(filepath=filepath)

        plane1 = Aeroplane(callsign="FLIGHT1", country="USA", velocity=100.0, altitude=1000.0)
        plane2 = Aeroplane(callsign="FLIGHT2", country="Spain", velocity=200.0, altitude=2000.0)
        plane3 = Aeroplane(callsign="FLIGHT3", country="France", velocity=300.0, altitude=3000.0)

        saver.add_aeroplane(plane1)
        saver.add_aeroplane(plane2)
        saver.add_aeroplane(plane3)

        result = saver.get_aeroplanes(velocity=200.0)
        assert len(result) == 1
        assert result[0].velocity == 200.0


# Тест 010: Проверка что get_aeroplanes фильтрует по высоте.
def test_get_aeroplanes_filters_by_altitude():
    from src.infrastructure.json_saver import JSONSaver
    from src.application.aeroplane import Aeroplane

    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = os.path.join(tmpdir, "test_aeroplanes.json")
        saver = JSONSaver(filepath=filepath)

        plane1 = Aeroplane(callsign="FLIGHT1", country="USA", velocity=100.0, altitude=1000.0)
        plane2 = Aeroplane(callsign="FLIGHT2", country="Spain", velocity=200.0, altitude=5000.0)

        saver.add_aeroplane(plane1)
        saver.add_aeroplane(plane2)

        result = saver.get_aeroplanes(altitude=5000.0)
        assert len(result) == 1
        assert result[0].altitude == 5000.0


# Тест 011: Проверка что get_aeroplanes обрабатывает отсутствие файла.
def test_get_aeroplanes_handles_missing_file():
    from src.infrastructure.json_saver import JSONSaver

    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = os.path.join(tmpdir, "nonexistent.json")
        saver = JSONSaver(filepath=filepath)

        result = saver.get_aeroplanes()
        assert isinstance(result, list)
        assert len(result) == 0


# Тест 012: Проверка что add_aeroplane обрабатывает некорректный объект.
def test_add_aeroplane_handles_invalid_object():
    from src.infrastructure.json_saver import JSONSaver

    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = os.path.join(tmpdir, "test_aeroplanes.json")
        saver = JSONSaver(filepath=filepath)

        invalid_object = object()
        with pytest.raises(AttributeError):
            saver.add_aeroplane(invalid_object)


# Тест 013: Проверка что delete_aeroplane обрабатывает некорректный объект.
def test_delete_aeroplane_handles_invalid_object():
    from src.infrastructure.json_saver import JSONSaver
    from src.application.aeroplane import Aeroplane

    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = os.path.join(tmpdir, "test_aeroplanes.json")
        saver = JSONSaver(filepath=filepath)

        # Добавим корректный самолёт
        plane = Aeroplane(callsign="TEST", country="USA", velocity=100.0, altitude=1000.0)
        saver.add_aeroplane(plane)

        # Удаление некорректного объекта вызывает AttributeError
        invalid_object = object()
        with pytest.raises(AttributeError):
            saver.delete_aeroplane(invalid_object)


# Тест 014: Проверка что save_data обрабатывает ошибку записи.
def test_save_data_handles_io_error():
    from src.infrastructure.json_saver import JSONSaver
    from src.application.aeroplane import Aeroplane
    import shutil

    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = os.path.join(tmpdir, "readonly", "test.json")
        saver = JSONSaver(filepath=filepath)

        # Удалить папку чтобы вызвать ошибку записи
        shutil.rmtree(os.path.dirname(filepath))

        plane = Aeroplane(callsign="TEST", country="USA", velocity=100.0, altitude=1000.0)
        with pytest.raises(IOError):
            saver.add_aeroplane(plane)
