# -*- coding: utf-8 -*-
"""Тесты для модуля aeroplanes_api."""

import pytest
from unittest.mock import MagicMock

from src.infrastructure.aeroplanes_api import AeroplanesAPI
from src.infrastructure.http_requestor import HTTPRequestor


# ============================================================================
# 0. Проверка класса: AeroplanesAPI из модуля src.aeroplanes_api.
# ============================================================================

# Тест 001: Проверка, что можно создать экземпляр AeroplanesAPI.
def test_can_create_api():
    """
    Проверяет, что объект AeroplanesAPI создаётся без параметров.

    При создании без параметров должен автоматически создаваться HTTP-клиент по умолчанию.
    """
    api = AeroplanesAPI()
    assert api is not None


# Тест 002: Проверка, что AeroplanesAPI наследуется от APIConnector.
def test_api_inheritance():
    """
    Проверяет, что AeroplanesAPI наследуется от абстрактного класса APIConnector.

    Это соответствует требованию курсовой о наследовании абстрактных классов.
    """
    from src.infrastructure.api_base import APIConnector
    assert issubclass(AeroplanesAPI, APIConnector)


# Тест 003: Проверка get_country_coordinates — успешный запрос.
def test_get_country_coordinates_success(mock_nominatim_response):
    """
    Проверяет, что get_country_coordinates возвращает boundingbox при успешном ответе Nominatim.

    Mock возвращает координаты границы страны, метод должен вернуть список из 4 чисел.
    """
    mock_requestor = MagicMock(spec=HTTPRequestor)
    mock_requestor.get.return_value = mock_nominatim_response

    api = AeroplanesAPI(http_requestor=mock_requestor)
    bbox = api.get_country_coordinates("Spain")

    assert len(bbox) == 4
    assert all(isinstance(coord, float) for coord in bbox)


# Тест 004: Проверка get_country_coordinates — страна не найдена.
def test_get_country_coordinates_not_found():
    """
    Проверяет, что get_country_coordinates вызывает ValueError при пустом ответе Nominatim.

    Пустой список означает, что страна не найдена.
    """
    mock_requestor = MagicMock(spec=HTTPRequestor)
    mock_requestor.get.return_value = []

    api = AeroplanesAPI(http_requestor=mock_requestor)
    with pytest.raises(ValueError):
        api.get_country_coordinates("Atlantis")


# Тест 005: Проверка get_country_coordinates — нет boundingbox.
def test_get_country_coordinates_no_bbox():
    """
    Проверяет, что get_country_coordinates вызывает ValueError при отсутствии boundingbox.

    Nominatim вернул ответ, но без координат границы.
    """
    mock_requestor = MagicMock(spec=HTTPRequestor)
    mock_requestor.get.return_value = [{"name": "Spain"}]

    api = AeroplanesAPI(http_requestor=mock_requestor)
    with pytest.raises(ValueError):
        api.get_country_coordinates("Spain")


# Тест 006: Проверка get_aeroplanes — успешный запрос.
def test_get_aeroplanes_success():
    """
    Проверяет, что get_aeroplanes возвращает список самолётов в пределах boundingbox.

    Mock возвращает координаты страны и список самолётов, метод должен отфильтровать по координатам.
    """
    mock_requestor = MagicMock(spec=HTTPRequestor)
    mock_requestor.get.side_effect = [
        [{"name": "Spain", "boundingbox": ["27.6", "43.8", "-18.4", "4.4"]}],
        {
            "time": 1766142246,
            "states": [
                [
                    "4b1812", "SWR438A ", "Spain", 1766166618, 1766166618,
                    1.0, 40.0, 4267.2, False, 189.7, 129.39, 14.63,
                    None, 4282.44, "2061", False, 0
                ]
            ]
        }
    ]

    api = AeroplanesAPI(http_requestor=mock_requestor)
    result = api.get_aeroplanes("Spain")

    assert isinstance(result, list)
    assert len(result) == 1


# Тест 007: Проверка get_aeroplanes — пустой ответ OpenSky.
def test_get_aeroplanes_empty_opensky(mock_nominatim_response):
    """
    Проверяет, что get_aeroplanes возвращает пустой список при пустом ответе OpenSky.

    OpenSky вернул пустой ответ — самолётов нет.
    """
    mock_requestor = MagicMock(spec=HTTPRequestor)
    mock_requestor.get.side_effect = [mock_nominatim_response, {"states": []}]

    api = AeroplanesAPI(http_requestor=mock_requestor)
    result = api.get_aeroplanes("Spain")

    assert result == []


# Тест 008: Проверка Circuit Breaker — не пропускает запрос после 5 ошибок.
def test_circuit_breaker_opens_after_failures():
    """
    Проверяет, что Circuit Breaker открывается после 5 ошибок.

    При открытии Circuit Breaker метод get_aeroplanes должен вызвать RuntimeError.
    """
    mock_requestor = MagicMock(spec=HTTPRequestor)
    mock_requestor.get.side_effect = RuntimeError("Error")

    api = AeroplanesAPI(http_requestor=mock_requestor)
    for _ in range(5):
        try:
            api.get_country_coordinates("Spain")
        except RuntimeError:
            pass

    assert api._circuit_breaker.state == "OPEN"

    with pytest.raises(RuntimeError) as exc_info:
        api.get_country_coordinates("Spain")
    assert "Circuit Breaker открыт" in str(exc_info.value)


# Тест 009: Проверка Circuit Breaker — пропускает запрос после восстановления.
def test_circuit_breaker_half_open():
    """
    Проверяет, что Circuit Breaker переходит в HALF_OPEN после таймаута.

    После recovery_timeout (30 секунд) Circuit Breaker должен позволить тестовый запрос.
    """
    import time

    mock_requestor = MagicMock(spec=HTTPRequestor)
    mock_requestor.get.side_effect = Exception("API error")

    api = AeroplanesAPI(http_requestor=mock_requestor)

    # 5 ошибок для срабатывания Circuit Breaker
    for _ in range(5):
        with pytest.raises(Exception):
            api.get_country_coordinates("Spain")

    # Ждём recovery_timeout (уменьшено до 0.5 сек для ускорения тестов)
    time.sleep(0.5)

    # Теперь должен быть HALF_OPEN и запрос должен пройти
    mock_requestor.get.side_effect = None
    mock_requestor.get.return_value = [{"name": "Spain", "boundingbox": ["40.0", "43.0", "-5.0", "3.0"]}]
    result = api.get_country_coordinates("Spain")
    assert result is not None


# Тест 010: Проверка Circuit Breaker — сообщение об ошибке.
def test_circuit_breaker_error_message():
    """
    Проверяет, что при открытии Circuit Breaker выводится понятное сообщение об ошибке.

    Сообщение должно содержать информацию о состоянии Circuit Breaker.
    """
    mock_requestor = MagicMock(spec=HTTPRequestor)
    mock_requestor.get.side_effect = RuntimeError("Error")

    api = AeroplanesAPI(http_requestor=mock_requestor)

    # 5 ошибок для срабатывания Circuit Breaker
    for _ in range(5):
        try:
            api.get_country_coordinates("Spain")
        except RuntimeError:
            pass

    # 6-й запрос должен вызвать RuntimeError с понятным сообщением
    with pytest.raises(RuntimeError) as exc_info:
        api.get_country_coordinates("Spain")

    assert "Circuit Breaker открыт" in str(exc_info.value)


# Тест 011: Проверка Circuit Breaker — сбрасывает счётчик при успехе.
def test_circuit_breaker_resets_on_success():
    """
    Проверяет, что успешный запрос сбрасывает счётчик ошибок Circuit Breaker.

    После успешного запроса Circuit Breaker должен вернуться в состояние CLOSED.
    """
    mock_requestor = MagicMock(spec=HTTPRequestor)
    call_count = 0

    def mock_get(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            raise RuntimeError("Error")
        return [{"name": "Spain", "boundingbox": ["40.0", "43.0", "-5.0", "3.0"]}]

    mock_requestor.get.side_effect = mock_get

    api = AeroplanesAPI(http_requestor=mock_requestor)
    try:
        api.get_country_coordinates("Spain")
    except RuntimeError:
        pass

    result = api.get_country_coordinates("Spain")
    assert result is not None
    assert api._circuit_breaker.state == "CLOSED"


# Тест 012: Проверка get_aeroplanes — фильтрация по координатам.
def test_get_aeroplanes_filters_by_coordinates():
    """
    Проверяет, что get_aeroplanes правильно фильтрует самолёты по координатам.

    Самолёты за пределами boundingbox должны быть исключены из результата.
    """
    mock_requestor = MagicMock(spec=HTTPRequestor)
    # boundingbox Spain: lat 40-43, lon -5 to 3
    mock_requestor.get.side_effect = [
        [{"name": "Spain", "boundingbox": ["40.0", "43.0", "-5.0", "3.0"]}],
        {
            "states": [
                # Самолёт внутри Spain (lat 41, lon -2)
                ["plane1", "FLY1", "Spain", 0, 0, -2.0, 41.0, 5000.0,
                 False, 200.0, 0.0, 0.0, None, 5000.0, "0000", False, 0],
                # Самолёт вне Spain (lat 50, lon 10)
                ["plane2", "FLY2", "France", 0, 0, 10.0, 50.0, 6000.0,
                 False, 250.0, 90.0, 0.0, None, 6000.0, "0001", False, 0]
            ]
        }
    ]

    api = AeroplanesAPI(http_requestor=mock_requestor)
    result = api.get_aeroplanes("Spain")

    assert len(result) == 1
    assert result[0][1] == "FLY1"


# Тест 013: Проверка что get_aeroplanes обрабатывает некорректный JSON.
def test_get_aeroplanes_handles_invalid_json():
    """
    Проверяет, что get_aeroplanes обрабатывает некорректный JSON.

    Возвращает некорректный JSON и проверяет что ValueError обрабатывается.
    """
    mock_requestor = MagicMock(spec=HTTPRequestor)
    mock_requestor.get.side_effect = ValueError("Invalid JSON")

    api = AeroplanesAPI(http_requestor=mock_requestor)

    with pytest.raises(ValueError):
        api.get_aeroplanes("Spain")


# Тест 014: Проверка что get_aeroplanes пропускает None элементы.
def test_get_aeroplanes_skips_none_states():
    """
    Проверяет, что get_aeroplanes пропускает None элементы в списке состояний.

    Возвращает список состояний с None элементами и проверяет что они пропускаются.
    """
    mock_requestor = MagicMock(spec=HTTPRequestor)
    mock_requestor.get.side_effect = [
        [{"name": "Spain", "boundingbox": ["40.0", "43.0", "-5.0", "3.0"]}],
        {
            "states": [
                None,
                ["plane1", "FLT1", "Spain", 0, 0, -2.0, 41.0, 5000.0,
                 False, 200.0, 0.0, 0.0, None, 5000.0, "0000", False, 0],
                None,
            ]
        }
    ]

    api = AeroplanesAPI(http_requestor=mock_requestor)
    result = api.get_aeroplanes("Spain")

    assert len(result) == 1
    assert result[0][1] == "FLT1"


# Тест 015: Проверка что get_aeroplanes пропускает самолёты с None координатами.
def test_get_aeroplanes_skips_none_coordinates():
    """
    Проверяет, что get_aeroplanes пропускает самолёты с None координатами.

    Возвращает список состояний с самолётами имеющими None latitude/longitude
    и проверяет что они пропускаются.
    """
    mock_requestor = MagicMock(spec=HTTPRequestor)
    mock_requestor.get.side_effect = [
        [{"name": "Spain", "boundingbox": ["40.0", "43.0", "-5.0", "3.0"]}],
        {
            "states": [
                # Самолёт с None координатами
                ["p1", "FLT1", "Spain", 0, 0, None, None, 5000.0,
                 False, 200.0, 0.0, 0.0, None, 5000.0, "0000", False, 0],
                # Самолёт с валидными координатами
                ["p2", "FLT2", "Spain", 0, 0, 1.0, 41.0, 8000.0,
                 False, 250.0, 90.0, 0.0, None, 8000.0, "0000", False, 0]
            ]
        }
    ]

    api = AeroplanesAPI(http_requestor=mock_requestor)
    result = api.get_aeroplanes("Spain")

    assert len(result) == 1
    assert result[0][1] == "FLT2"


# Тест 016: Проверка что get_aeroplanes возвращает пустой список при отсутствии states.
def test_get_aeroplanes_returns_empty_when_no_states():
    """
    Проверяет, что get_aeroplanes возвращает пустой список при отсутствии states.

    Возвращает ответ без ключа states и проверяет что возвращается пустой список.
    """
    mock_requestor = MagicMock(spec=HTTPRequestor)
    mock_requestor.get.side_effect = [
        [{"name": "Spain", "boundingbox": ["40.0", "43.0", "-5.0", "3.0"]}],
        {"time": 1234567890}  # Нет states
    ]

    api = AeroplanesAPI(http_requestor=mock_requestor)
    result = api.get_aeroplanes("Spain")

    assert result == []
