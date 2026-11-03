# -*- coding: utf-8 -*-
"""Тесты для модуля src.txt_saver."""

import pytest

from src.infrastructure.txt_saver import TXTSaver


# ============================================================================
# 0. Проверка класса: TXTSaver из модуля src.txt_saver.
# ============================================================================

# Тест 001: Проверка, что можно создать экземпляр TXTSaver.
def test_can_create_txt_saver():
    """Проверяет что можно создать экземпляр TXTSaver.

    Создает TXTSaver и проверяет что объект успешно создан.
    """
    saver = TXTSaver()
    assert saver is not None


# Тест 002: Проверка, что TXTSaver наследуется от FileConnector.
def test_txt_saver_inherits_from_file_connector():
    """Проверяет что TXTSaver наследуется от FileConnector.

    Проверяет иерархию наследования: TXTSaver должен быть подклассом
    FileConnector из модуля src.infrastructure.file_connector.
    """
    from src.infrastructure.file_connector import FileConnector
    assert issubclass(TXTSaver, FileConnector)


# Тест 003: Проверка, что add_aeroplane вызывает NotImplementedError.
def test_add_aeroplane_raises_not_implemented():
    """Проверяет что add_aeroplane вызывает NotImplementedError.

    Создает TXTSaver и вызывает add_aeroplane, ожидая NotImplementedError
    так как метод является заглушкой.
    """
    saver = TXTSaver()
    with pytest.raises(NotImplementedError) as exc_info:
        saver.add_aeroplane(None)
    assert "TXT-сохранение ещё не реализовано" in str(exc_info.value)


# Тест 004: Проверка, что delete_aeroplane вызывает NotImplementedError.
def test_delete_aeroplane_raises_not_implemented():
    """Проверяет что delete_aeroplane вызывает NotImplementedError.

    Создает TXTSaver и вызывает delete_aeroplane, ожидая NotImplementedError
    так как метод является заглушкой.
    """
    saver = TXTSaver()
    with pytest.raises(NotImplementedError) as exc_info:
        saver.delete_aeroplane(None)
    assert "TXT-удаление ещё не реализовано" in str(exc_info.value)


# Тест 005: Проверка, что get_aeroplanes вызывает NotImplementedError.
def test_get_aeroplanes_raises_not_implemented():
    """Проверяет что get_aeroplanes вызывает NotImplementedError.

    Создает TXTSaver и вызывает get_aeroplanes, ожидая NotImplementedError
    так как метод является заглушкой.
    """
    saver = TXTSaver()
    with pytest.raises(NotImplementedError) as exc_info:
        saver.get_aeroplanes()
    assert "TXT-чтение ещё не реализовано" in str(exc_info.value)
