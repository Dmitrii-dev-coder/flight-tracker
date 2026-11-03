# -*- coding: utf-8 -*-
"""Тесты для модуля src.csv_saver."""

import pytest

from src.infrastructure.csv_saver import CSVSaver


# ============================================================================
# 0. Проверка класса: CSVSaver из модуля src.csv_saver.
# ============================================================================

# Тест 001: Проверка, что можно создать экземпляр CSVSaver.
def test_can_create_csv_saver():
    """Проверяет что можно создать экземпляр CSVSaver.

    Создает CSVSaver и проверяет что объект успешно создан.
    """
    saver = CSVSaver()
    assert saver is not None


# Тест 002: Проверка что CSVSaver наследуется от FileConnector.
def test_csv_saver_inherits_from_file_connector():
    """Проверяет что CSVSaver наследуется от FileConnector.

    Проверяет иерархию наследования: CSVSaver должен быть подклассом
    FileConnector из модуля src.infrastructure.file_connector.
    """
    from src.infrastructure.file_connector import FileConnector
    assert issubclass(CSVSaver, FileConnector)


# Тест 003: Проверка что add_aeroplane вызывает NotImplementedError.
def test_add_aeroplane_raises_not_implemented():
    """Проверяет что add_aeroplane вызывает NotImplementedError.

    Создает CSVSaver и вызывает add_aeroplane, ожидая NotImplementedError
    так как метод является заглушкой.
    """
    saver = CSVSaver()
    with pytest.raises(NotImplementedError) as exc_info:
        saver.add_aeroplane(None)
    assert "CSV-сохранение ещё не реализовано" in str(exc_info.value)


# Тест 004: Проверка что delete_aeroplane вызывает NotImplementedError.
def test_delete_aeroplane_raises_not_implemented():
    """Проверяет что delete_aeroplane вызывает NotImplementedError.

    Создает CSVSaver и вызывает delete_aeroplane, ожидая NotImplementedError
    так как метод является заглушкой.
    """
    saver = CSVSaver()
    with pytest.raises(NotImplementedError) as exc_info:
        saver.delete_aeroplane(None)
    assert "CSV-удаление ещё не реализовано" in str(exc_info.value)


# Тест 005: Проверка что get_aeroplanes вызывает NotImplementedError.
def test_get_aeroplanes_raises_not_implemented():
    """Проверяет что get_aeroplanes вызывает NotImplementedError.

    Создает CSVSaver и вызывает get_aeroplanes, ожидая NotImplementedError
    так как метод является заглушкой.
    """
    saver = CSVSaver()
    with pytest.raises(NotImplementedError) as exc_info:
        saver.get_aeroplanes()
    assert "CSV-чтение ещё не реализовано" in str(exc_info.value)
