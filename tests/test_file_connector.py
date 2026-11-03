# -*- coding: utf-8 -*-
"""Тесты для модуля src.file_connector."""

import inspect

import pytest
from abc import ABC

from src.infrastructure.file_connector import FileConnector


# ============================================================================
# 0. Проверка класса: FileConnector из модуля src.file_connector.
# ============================================================================

# Тест 001: Проверка, что FileConnector является абстрактным классом.
def test_file_connector_is_abstract():
    """Проверяет что FileConnector является абстрактным классом.

    Проверяет что FileConnector наследуется от ABC (Abstract Base Class).
    """
    assert issubclass(FileConnector, ABC)


# Тест 002: Проверка, что add_aeroplane — абстрактный метод.
def test_add_aeroplane_is_abstract():
    """Проверяет что метод add_aeroplane является абстрактным.

    Проверяет наличие атрибута __isabstractmethod__ и что он равен True
    для метода add_aeroplane класса FileConnector.
    """
    assert hasattr(FileConnector.add_aeroplane, "__isabstractmethod__")
    assert FileConnector.add_aeroplane.__isabstractmethod__ is True


# Тест 003: Проверка, что delete_aeroplane — абстрактный метод.
def test_delete_aeroplane_is_abstract():
    """Проверяет что метод delete_aeroplane является абстрактным.

    Проверяет наличие атрибута __isabstractmethod__ и что он равен True
    для метода delete_aeroplane класса FileConnector.
    """
    assert hasattr(FileConnector.delete_aeroplane, "__isabstractmethod__")
    assert FileConnector.delete_aeroplane.__isabstractmethod__ is True


# Тест 004: Проверка, что get_aeroplanes — абстрактный метод.
def test_get_aeroplanes_is_abstract():
    """Проверяет что метод get_aeroplanes является абстрактным.

    Проверяет наличие атрибута __isabstractmethod__ и что он равен True
    для метода get_aeroplanes класса FileConnector.
    """
    assert hasattr(FileConnector.get_aeroplanes, "__isabstractmethod__")
    assert FileConnector.get_aeroplanes.__isabstractmethod__ is True


# Тест 005: Проверка, что нельзя создать экземпляр напрямую.
def test_cannot_instantiate_file_connector():
    """Проверяет что создание экземпляра FileConnector напрямую вызывает TypeError.

    Пытается создать объект FileConnector и ожидает TypeError,
    так как это абстрактный класс с абстрактными методами.
    """
    with pytest.raises(TypeError):
        FileConnector()


# Тест 006: Проверка сигнатур методов.
def test_method_signatures():
    """Проверяет что абстрактные методы имеют правильные сигнатуры.

    Проверяет что add_aeroplane, delete_aeroplane и get_aeroplanes имеют
    ожидаемые параметры в своих сигнатурах.
    """
    sig = inspect.signature(FileConnector.add_aeroplane)
    params = list(sig.parameters.keys())
    assert "self" in params
    assert "aeroplane" in params

    sig = inspect.signature(FileConnector.delete_aeroplane)
    params = list(sig.parameters.keys())
    assert "self" in params
    assert "aeroplane" in params

    sig = inspect.signature(FileConnector.get_aeroplanes)
    params = list(sig.parameters.keys())
    assert "self" in params
