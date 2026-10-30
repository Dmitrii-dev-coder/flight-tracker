# -*- coding: utf-8 -*-
"""Тесты для модуля src.api_base."""

import pytest
from abc import ABC, abstractmethod
import inspect


# ============================================================================
# 0. Проверка класса: APIConnector из модуля src.api_base.
# ============================================================================

# Тест 001: Проверка что APIConnector наследуется от ABC.
def test_api_connector_is_abstract():
    from src.api_base import APIConnector
    assert issubclass(APIConnector, ABC), "APIConnector должен наследоваться от ABC"


# Тест 002: Проверка что get_country_coordinates — абстрактный метод.
def test_get_country_coordinates_is_abstract():
    from src.api_base import APIConnector
    assert hasattr(APIConnector.get_country_coordinates, "__isabstractmethod__")
    assert APIConnector.get_country_coordinates.__isabstractmethod__ is True


# Тест 003: Проверка что get_aeroplanes — абстрактный метод.
def test_get_aeroplanes_is_abstract():
    from src.api_base import APIConnector
    assert hasattr(APIConnector.get_aeroplanes, "__isabstractmethod__")
    assert APIConnector.get_aeroplanes.__isabstractmethod__ is True


# Тест 004: Проверка что make_request — абстрактный метод.
def test_make_request_is_abstract():
    from src.api_base import APIConnector
    assert hasattr(APIConnector.make_request, "__isabstractmethod__")
    assert APIConnector.make_request.__isabstractmethod__ is True


# Тест 005: Проверка что нельзя создать экземпляр напрямую.
def test_cannot_instantiate_abstract():
    from src.api_base import APIConnector
    with pytest.raises(TypeError):
        APIConnector()


# Тест 006: Проверка сигнатур методов.
def test_method_signatures():
    from src.api_base import APIConnector

    sig = inspect.signature(APIConnector.get_country_coordinates)
    params = list(sig.parameters.keys())
    assert "self" in params
    assert "country" in params

    sig = inspect.signature(APIConnector.get_aeroplanes)
    params = list(sig.parameters.keys())
    assert "self" in params
    assert "country" in params
