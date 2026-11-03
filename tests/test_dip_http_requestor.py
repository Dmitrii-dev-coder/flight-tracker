# -*- coding: utf-8 -*-
"""Тесты для проверки принципа DIP: HTTPRequestor абстракция."""

from unittest.mock import MagicMock, patch

from src.infrastructure.aeroplanes_api import AeroplanesAPI
from src.infrastructure.http_requestor import HTTPRequestor
from src.infrastructure.requests_http_client import RequestsHTTPClient


# ============================================================================
# 1. Проверка HTTPRequestor абстракции.
# ============================================================================

# Тест 001: HTTPRequestor — абстрактный класс.
def test_http_requestor_is_abstract():
    """Проверяет что HTTPRequestor является абстрактным классом.

    Проверяет наличие атрибута __abstractmethods__ у класса HTTPRequestor,
    что указывает на его абстрактность.
    """
    assert hasattr(HTTPRequestor, '__abstractmethods__')


# Тест 002: Нельзя инстанцировать HTTPRequestor напрямую.
def test_cannot_instantiate_http_requestor():
    """Проверяет что создание экземпляра HTTPRequestor напрямую вызывает TypeError.

    Пытается создать объект HTTPRequestor и ожидает TypeError,
    так как это абстрактный класс.
    """
    import pytest
    with pytest.raises(TypeError):
        HTTPRequestor()


# Тест 003: RequestsHTTPClient наследуется от HTTPRequestor.
def test_requests_http_client_inherits_from_http_requestor():
    """Проверяет что RequestsHTTPClient наследуется от HTTPRequestor.

    Проверяет иерархию наследования: RequestsHTTPClient должен быть
    подклассом HTTPRequestor.
    """
    assert issubclass(RequestsHTTPClient, HTTPRequestor)


# Тест 004: RequestsHTTPClient имеет метод get.
def test_requests_http_client_has_get_method():
    """Проверяет что RequestsHTTPClient содержит метод get.

    Проверяет наличие метода get у класса RequestsHTTPClient,
    который используется для выполнения HTTP-запросов.
    """
    assert hasattr(RequestsHTTPClient, 'get')


# ============================================================================
# 2. Проверка DIP: AeroplanesAPI зависит от абстракции.
# ============================================================================

# Тест 005: AeroplanesAPI принимает HTTPRequestor в конструкторе.
def test_aeroplanes_api_accepts_http_requestor():
    """Проверяет что AeroplanesAPI принимает HTTPRequestor в конструкторе.

    Создаёт AeroplanesAPI с моковым HTTPRequestor и проверяет что
    он корректно сохраняется в атрибуте _http_requestor.
    """
    mock_requestor = MagicMock(spec=HTTPRequestor)
    api = AeroplanesAPI(http_requestor=mock_requestor)
    assert api._http_requestor is mock_requestor


# Тест 006: AeroplanesAPI создаёт RequestsHTTPClient по умолчанию.
def test_aeroplanes_api_creates_default_client():
    """Проверяет что AeroplanesAPI создаёт RequestsHTTPClient по умолчанию.

    Создаёт AeroplanesAPI без параметров и проверяет что _http_requestor
    является экземпляром RequestsHTTPClient.
    """
    api = AeroplanesAPI()
    assert isinstance(api._http_requestor, RequestsHTTPClient)


# Тест 007: DIP: можно подменить HTTP-клиент на мок.
def test_dip_can_mock_http_client():
    """Проверяет что HTTP-клиент можно подменить на моковый для тестирования.

    Создаёт AeroplanesAPI с моковым HTTPRequestor и проверяет что
    можно тестировать API без реальных сетевых вызовов.
    """
    mock_requestor = MagicMock(spec=HTTPRequestor)
    mock_requestor.get.return_value = {
        "time": 1234567890,
        "states": [
            ["plane1", "FLT1", "Spain", 0, 0, 1.0, 41.0, 5000.0,
             False, 200.0, 0.0, 0.0, None, 5000.0, "0000", False, 0]
        ]
    }

    api = AeroplanesAPI(http_requestor=mock_requestor)

    # Подменяем get_country_coordinates чтобы не делать реальный запрос
    with patch.object(api, 'get_country_coordinates', return_value=[40.0, 43.0, -5.0, 3.0]):
        result = api.get_aeroplanes("Spain")

    # Проверяем что используется mock
    assert len(result) == 1
    assert result[0][1] == "FLT1"


# Тест 008: DIP: AeroplanesAPI не импортирует requests напрямую в make_request.
def test_dip_no_direct_requests_in_make_request():
    """Проверяет что AeroplanesAPI.make_request использует абстракцию HTTPRequestor.

    Анализирует исходный код метода make_request и проверяет что он
    использует self._http_requestor.get(), а не requests.get() напрямую.
    """
    import inspect

    source = inspect.getsource(AeroplanesAPI.make_request)

    # make_request должен использовать self._http_requestor.get(), а не requests.get()
    assert "self._http_requestor.get" in source
    # Не должно быть прямого вызова requests.get() в make_request
    assert "requests.get" not in source


# Тест 009: DIP: тестирование с моком без сетевых вызовов.
def test_dip_integration_with_mock():
    """Проверяет что AeroplanesAPI работает с моковым HTTPRequestor без сетевых вызовов.

    Создаёт AeroplanesAPI с моковым HTTPRequestor который имитирует
    ответы Nominatim и OpenSky API, проверяя корректность обработки данных.
    """
    mock_requestor = MagicMock(spec=HTTPRequestor)

    # Настраиваем мок для nominatim (возвращает список)
    mock_requestor.get.side_effect = [
        [{"name": "France", "boundingbox": ["42.0", "51.0", "-5.0", "8.0"]}],
        {"time": 1234567890, "states": [
            ["p1", "AFR1", "France", 0, 0, 2.0, 48.0, 8000.0,
             False, 250.0, 90.0, 0.0, None, 8000.0, "0000", False, 0],
            ["p2", "DAH2", "France", 0, 0, 3.0, 49.0, 10000.0,
             False, 300.0, 180.0, 10.0, None, 10000.0, "0000", False, 0]
        ]}
    ]

    api = AeroplanesAPI(http_requestor=mock_requestor)
    result = api.get_aeroplanes("France")

    assert len(result) == 2
    assert mock_requestor.get.call_count == 2
