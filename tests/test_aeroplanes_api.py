# -*- coding: utf-8 -*-
"""Тесты для модуля src.aeroplanes_api."""

import pytest
from unittest.mock import patch, MagicMock
import requests


# ============================================================================
# 0. Проверка класса: AeroplanesAPI из модуля src.aeroplanes_api.
# ============================================================================

# Тест 001: Проверка что AeroplanesAPI наследуется от APIConnector.
def test_aeroplanes_api_inherits_from_api_connector():
    from src.infrastructure.aeroplanes_api import AeroplanesAPI
    from src.infrastructure.api_base import APIConnector
    assert issubclass(AeroplanesAPI, APIConnector)


# Тест 002: Проверка что можно создать экземпляр AeroplanesAPI.
def test_can_instantiate_aeroplanes_api():
    from src.infrastructure.aeroplanes_api import AeroplanesAPI
    api = AeroplanesAPI()
    assert api is not None
    assert isinstance(api, AeroplanesAPI)


# Тест 003: Проверка что get_country_coordinates возвращает boundingbox.
def test_get_country_coordinates_returns_bbox():
    from src.infrastructure.aeroplanes_api import AeroplanesAPI

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{
        "place_id": 346277167,
        "name": "Canada",
        "boundingbox": ["41.6765597", "83.3362128", "-141.0027500", "-52.3237664"]
    }]

    with patch("src.infrastructure.aeroplanes_api.requests.get", return_value=mock_response):
        api = AeroplanesAPI()
        result = api.get_country_coordinates("Canada")

    assert isinstance(result, list)
    assert len(result) == 4
    assert result[0] == 41.6765597
    assert result[1] == 83.3362128
    assert result[2] == -141.0027500
    assert result[3] == -52.3237664


# Тест 004: Проверка что get_country_coordinates обрабатывает ошибку сети.
def test_get_country_coordinates_handles_request_error():
    from src.infrastructure.aeroplanes_api import AeroplanesAPI

    with patch("src.infrastructure.aeroplanes_api.requests.get", side_effect=requests.exceptions.RequestException("Network error")):
        api = AeroplanesAPI()
        with pytest.raises(requests.exceptions.RequestException):
            api.get_country_coordinates("UnknownCountry")


# Тест 005: Проверка что get_country_coordinates обрабатывает отсутствие данных.
def test_get_country_coordinates_no_data():
    from src.infrastructure.aeroplanes_api import AeroplanesAPI

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = []

    with patch("src.infrastructure.aeroplanes_api.requests.get", return_value=mock_response):
        api = AeroplanesAPI()
        with pytest.raises(ValueError):
            api.get_country_coordinates("EmptyCountry")


# Тест 006: Проверка что get_aeroplanes возвращает список самолётов.
def test_get_aeroplanes_returns_list():
    from src.infrastructure.aeroplanes_api import AeroplanesAPI

    mock_nominatim = MagicMock()
    mock_nominatim.status_code = 200
    mock_nominatim.json.return_value = [{
        "name": "Spain",
        "boundingbox": ["27.6", "43.8", "-18.4", "4.4"]
    }]

    mock_opensky = MagicMock()
    mock_opensky.status_code = 200
    mock_opensky.json.return_value = {
        "time": 1766142246,
        "states": [
            [
                "4b1812", "SWR438A ", "Spain", 1766166618, 1766166618,
                1.0, 40.0, 4267.2, False, 189.7, 129.39, 14.63,
                None, 4282.44, "2061", False, 0
            ]
        ]
    }

    with patch("src.infrastructure.aeroplanes_api.requests.get", side_effect=[mock_nominatim, mock_opensky]):
        api = AeroplanesAPI()
        result = api.get_aeroplanes("Spain")

    assert isinstance(result, list)
    assert len(result) == 1


# Тест 007: Проверка что get_aeroplanes фильтрует по boundingbox.
def test_get_aeroplanes_filters_by_bbox():
    from src.infrastructure.aeroplanes_api import AeroplanesAPI

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
                1.0, 39.0, 1000.0, False, 100.0, 0.0, 0.0,
                None, 1000.0, "0000", False, 0
            ],
            [
                "plane2", "FLT2", "Spain", 0, 0,
                2.0, 41.0, 2000.0, False, 200.0, 0.0, 0.0,
                None, 2000.0, "0001", False, 0
            ],
            [
                "plane3", "FLT3", "France", 0, 0,
                3.0, 45.0, 3000.0, False, 300.0, 0.0, 0.0,
                None, 3000.0, "0002", False, 0
            ]
        ]
    }

    with patch("src.infrastructure.aeroplanes_api.requests.get", side_effect=[mock_nominatim, mock_opensky]):
        api = AeroplanesAPI()
        result = api.get_aeroplanes("Spain")

    assert len(result) == 1
    assert result[0][0] == "plane2"


# Тест 008: Проверка что make_request обрабатывает неверный JSON.
def test_make_request_handles_invalid_json():
    from src.infrastructure.aeroplanes_api import AeroplanesAPI

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.side_effect = ValueError("Invalid JSON")

    with patch("src.infrastructure.aeroplanes_api.requests.get", return_value=mock_response):
        api = AeroplanesAPI()
        with pytest.raises(ValueError):
            api.make_request("https://example.com/api")


# Тест 009: Проверка что make_request возвращает данные при успешном запросе.
def test_make_request_success():
    from src.infrastructure.aeroplanes_api import AeroplanesAPI

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"key": "value", "count": 42}

    with patch("src.infrastructure.aeroplanes_api.requests.get", return_value=mock_response):
        api = AeroplanesAPI()
        result = api.make_request("https://example.com/api", {"param": "test"})

    assert result["key"] == "value"
    assert result["count"] == 42


# Тест 010: Проверка что CircuitBreaker открывается после ошибок.
def test_circuit_breaker_opens_after_failures():
    from src.infrastructure.aeroplanes_api import AeroplanesAPI

    api = AeroplanesAPI()

    with patch("src.infrastructure.aeroplanes_api.requests.get", side_effect=requests.exceptions.RequestException("Error")):
        for _ in range(5):
            try:
                api.make_request("https://example.com/api")
            except requests.exceptions.RequestException:
                pass

    assert api._circuit_breaker.state == "OPEN"

    with pytest.raises(requests.exceptions.RequestException) as exc_info:
        api.make_request("https://example.com/api")
    assert "Circuit Breaker открыт" in str(exc_info.value)


# Тест 011: Проверка что CircuitBreaker сбрасывается после успеха.
def test_circuit_breaker_resets_on_success():
    from src.infrastructure.aeroplanes_api import AeroplanesAPI

    api = AeroplanesAPI()

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"key": "value"}

    with patch("src.infrastructure.aeroplanes_api.requests.get", side_effect=[
        requests.exceptions.RequestException("Error"),
        mock_response
    ]):
        try:
            api.make_request("https://example.com/api")
        except requests.exceptions.RequestException:
            pass

        result = api.make_request("https://example.com/api")
        assert result["key"] == "value"
        assert api._circuit_breaker.state == "CLOSED"
