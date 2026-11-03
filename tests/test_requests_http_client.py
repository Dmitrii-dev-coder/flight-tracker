# -*- coding: utf-8 -*-
"""Тесты для модуля src.infrastructure.requests_http_client."""

from unittest.mock import MagicMock, patch

import pytest
import requests

from src.infrastructure.requests_http_client import RequestsHTTPClient
from src.infrastructure.http_requestor import HTTPRequestor


# ============================================================================
# 0. Проверка класса: RequestsHTTPClient из модуля src.requests_http_client.
# ============================================================================

# Тест 001: Проверка, что можно создать экземпляр RequestsHTTPClient.
def test_can_create_requests_http_client():
    """Проверяет что можно создать экземпляр RequestsHTTPClient.

    Создает RequestsHTTPClient и проверяет что объект успешно создан.
    """
    client = RequestsHTTPClient()
    assert client is not None


# Тест 002: Проверка, что RequestsHTTPClient наследуется от HTTPRequestor.
def test_requests_http_client_inherits_from_http_requestor():
    """Проверяет что RequestsHTTPClient наследуется от HTTPRequestor.

    Проверяет иерархию наследования: RequestsHTTPClient должен быть подклассом
    HTTPRequestor из модуля src.infrastructure.http_requestor.
    """
    assert issubclass(RequestsHTTPClient, HTTPRequestor)


# Тест 003: Проверка, что __init__ устанавливает заголовки по умолчанию.
def test_init_sets_default_headers():
    """Проверяет что __init__ устанавливает заголовок User-Agent.

    Создает RequestsHTTPClient и проверяет что _headers содержит
    корректный User-Agent.
    """
    client = RequestsHTTPClient()
    assert hasattr(client, '_headers')
    assert 'User-Agent' in client._headers
    assert client._headers['User-Agent'] == 'FlightTracker/1.0 (coursework)'


# Тест 004: Проверка, что get вызывает requests.get с правильными параметрами.
@patch('src.infrastructure.requests_http_client.requests.get')
def test_get_calls_requests_get(mock_get):
    """Проверяет что метод get вызывает requests.get с правильными параметрами.

    Создает RequestsHTTPClient, вызывает get и проверяет что requests.get
    вызван с правильным URL, params, headers и timeout.
    """
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"key": "value"}
    mock_get.return_value = mock_response

    client = RequestsHTTPClient()
    result = client.get("https://example.com/api", params={"q": "test"}, timeout=5.0)

    mock_get.assert_called_once()
    call_args = mock_get.call_args
    assert call_args[0][0] == "https://example.com/api"
    assert call_args[1]["params"] == {"q": "test"}
    assert call_args[1]["timeout"] == 5.0
    assert "headers" in call_args[1]
    assert result == {"key": "value"}


# Тест 005: Проверка что get использует заголовки по умолчанию.
@patch('src.infrastructure.requests_http_client.requests.get')
def test_get_uses_default_headers(mock_get):
    """Проверяет что метод get использует заголовки по умолчанию.

    Создает RequestsHTTPClient, вызывает get и проверяет что
    передаются заголовки User-Agent.
    """
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": "test"}
    mock_get.return_value = mock_response

    client = RequestsHTTPClient()
    client.get("https://example.com/api")

    call_args = mock_get.call_args
    assert call_args[1]["headers"] == {"User-Agent": "FlightTracker/1.0 (coursework)"}


# Тест 006: Проверка что get вызывает raise_for_status.
@patch('src.infrastructure.requests_http_client.requests.get')
def test_get_raises_for_error_status(mock_get):
    """Проверяет что get вызывает исключение при ошибке HTTP.

    Создает RequestsHTTPClient и мокает response с ошибкой 404,
    проверяет что вызывается исключение от requests.
    """
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")
    mock_get.return_value = mock_response

    client = RequestsHTTPClient()
    with pytest.raises(requests.exceptions.HTTPError):
        client.get("https://example.com/api")


# Тест 007: Проверка, что get возвращает JSON данные.
@patch('src.infrastructure.requests_http_client.requests.get')
def test_get_returns_json_data(mock_get):
    """Проверяет что get возвращает распарсенные JSON данные.

    Создает RequestsHTTPClient, вызывает get и проверяет что
    возвращается словарь из response.json().
    """
    expected_data = {
        "time": 1234567890,
        "states": [
            ["plane1", "FLT1", "Spain", 0, 0, 1.0, 41.0, 5000.0,
             False, 200.0, 0.0, 0.0, None, 5000.0, "0000", False, 0]
        ]
    }
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = expected_data
    mock_get.return_value = mock_response

    client = RequestsHTTPClient()
    result = client.get("https://opensky.network/api/flights")

    assert result == expected_data
    assert result["time"] == 1234567890
    assert len(result["states"]) == 1


# Тест 008: Проверка что get использует timeout по умолчанию.
@patch('src.infrastructure.requests_http_client.requests.get')
def test_get_uses_default_timeout(mock_get):
    """Проверяет что get использует timeout по умолчанию 10 секунд.

    Вызывает get без явного указания timeout и проверяет что
    передается timeout=10.0.
    """
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {}
    mock_get.return_value = mock_response

    client = RequestsHTTPClient()
    client.get("https://example.com/api")

    call_args = mock_get.call_args
    assert call_args[1]["timeout"] == 10.0
