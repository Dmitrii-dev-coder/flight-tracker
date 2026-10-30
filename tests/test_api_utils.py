# -*- coding: utf-8 -*-
"""Тесты для модуля src.infrastructure.api_utils."""

from unittest.mock import patch, MagicMock
import requests


# ============================================================================
# 0. Проверка класса: CircuitBreaker из модуля src.infrastructure.api_utils.
# ============================================================================

# Тест 001: Проверка что CircuitBreaker инициализируется в состоянии CLOSED.
def test_circuit_breaker_initial_state():
    from src.infrastructure.api_utils import CircuitBreaker
    cb = CircuitBreaker()
    assert cb.state == "CLOSED"


# Тест 002: Проверка что allow_request возвращает True в состоянии CLOSED.
def test_circuit_breaker_allow_request_closed():
    from src.infrastructure.api_utils import CircuitBreaker
    cb = CircuitBreaker()
    assert cb.allow_request() is True


# Тест 003: Проверка что record_success сбрасывает счётчик ошибок.
def test_circuit_breaker_record_success():
    from src.infrastructure.api_utils import CircuitBreaker
    cb = CircuitBreaker()

    for _ in range(5):
        cb.record_failure()

    assert cb.state == "OPEN"

    cb.record_success()
    assert cb.state == "CLOSED"
    assert cb.allow_request() is True


# Тест 004: Проверка что после threshold ошибок Circuit Breaker открывается.
def test_circuit_breaker_opens_after_threshold():
    from src.infrastructure.api_utils import CircuitBreaker
    cb = CircuitBreaker(failure_threshold=3)

    cb.record_failure()
    assert cb.state == "CLOSED"

    cb.record_failure()
    assert cb.state == "CLOSED"

    cb.record_failure()
    assert cb.state == "OPEN"
    assert cb.allow_request() is False


# Тест 005: Проверка что Circuit Breaker переходит в HALF_OPEN после таймаута.
def test_circuit_breaker_half_open_after_timeout():
    from src.infrastructure.api_utils import CircuitBreaker
    import time

    cb = CircuitBreaker(failure_threshold=2, recovery_timeout=0.1)

    cb.record_failure()
    cb.record_failure()
    assert cb.state == "OPEN"

    time.sleep(0.15)
    cb._check_state()
    assert cb.state == "HALF_OPEN"
    assert cb.allow_request() is True


# Тест 006: Проверка что Circuit Breaker закрывается после HALF_OPEN успеха.
def test_circuit_breaker_closes_after_half_open_success():
    from src.infrastructure.api_utils import CircuitBreaker
    import time

    cb = CircuitBreaker(failure_threshold=2, recovery_timeout=0.1)

    cb.record_failure()
    cb.record_failure()
    assert cb.state == "OPEN"

    time.sleep(0.15)
    cb._check_state()
    cb.record_success()
    assert cb.state == "CLOSED"


# Тест 007: Проверка что make_request_with_retry выполняет запрос.
def test_make_request_with_retry_success():
    from src.infrastructure.api_utils import make_request_with_retry

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"key": "value"}

    with patch("requests.get", return_value=mock_response):
        result = make_request_with_retry("https://example.com/api")
        assert result["key"] == "value"


# Тест 008: Проверка что make_request_with_retry обрабатывает Timeout.
def test_make_request_with_retry_timeout():
    from src.infrastructure.api_utils import make_request_with_retry

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"key": "value"}

    call_count = 0

    def mock_get(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            raise requests.exceptions.Timeout("Timeout")
        return mock_response

    with patch("requests.get", side_effect=mock_get):
        result = make_request_with_retry("https://example.com/api")
        assert result["key"] == "value"
        assert call_count == 2  # Первый вызов упал, второй успешный


# Тест 009: Проверка что make_request_with_retry передаёт timeout.
def test_make_request_with_retry_timeout_param():
    from src.infrastructure.api_utils import make_request_with_retry

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"key": "value"}

    with patch("requests.get", return_value=mock_response) as mock_get:
        make_request_with_retry("https://example.com/api", timeout=15.0)
        mock_get.assert_called_once()
        assert mock_get.call_args[1]["timeout"] == 15.0
