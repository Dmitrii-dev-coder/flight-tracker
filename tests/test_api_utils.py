# -*- coding: utf-8 -*-
"""Тесты для модуля src.infrastructure.api_utils."""

import time

import pytest
import requests
from unittest.mock import MagicMock

from src.infrastructure.api_utils import CircuitBreaker, make_request_with_retry
from src.infrastructure.http_requestor import HTTPRequestor


# ============================================================================
# 0. Проверка класса: CircuitBreaker из модуля src.infrastructure.api_utils.
# ============================================================================

# Тест 001: Проверка, что CircuitBreaker инициализируется в состоянии CLOSED.
def test_circuit_breaker_initial_state():
    """Проверяет что CircuitBreaker инициализируется в состоянии CLOSED.

    Создаёт CircuitBreaker по умолчанию и проверяет что его начальное
    состояние state равно "CLOSED".
    """
    cb = CircuitBreaker()
    assert cb.state == "CLOSED"


# Тест 002: Проверка, что allow_request возвращает True в состоянии CLOSED.
def test_circuit_breaker_allow_request_closed():
    """Проверяет что allow_request возвращает True в состоянии CLOSED.

    Создаёт CircuitBreaker и вызывает allow_request(), проверяя что
    в состоянии CLOSED запросы разрешены.
    """
    cb = CircuitBreaker()
    assert cb.allow_request() is True


# Тест 003: Проверка, что record_success сбрасывает счётчик ошибок.
def test_circuit_breaker_record_success():
    """Проверяет что record_success сбрасывает счётчик ошибок и закрывает circuit breaker.

    Создаёт 5 ошибок чтобы открыть CircuitBreaker, затем вызывает record_success
    и проверяет что состояние возвращается в CLOSED и запросы снова разрешены.
    """
    cb = CircuitBreaker()

    for _ in range(5):
        cb.record_failure()

    assert cb.state == "OPEN"

    cb.record_success()
    assert cb.state == "CLOSED"
    assert cb.allow_request() is True


# Тест 004: Проверка, что после threshold ошибок Circuit Breaker открывается.
def test_circuit_breaker_opens_after_threshold():
    """Проверяет что CircuitBreaker открывается после превышения threshold ошибок.

    Создаёт CircuitBreaker с threshold=3 и вызывает record_failure три раза,
    проверяя что состояние остаётся CLOSED после 2 ошибок и открывается
    после третьей.
    """
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
    """Проверяет что CircuitBreaker переходит в HALF_OPEN после recovery_timeout.

    Создаёт CircuitBreaker с recovery_timeout=0.1, открывает его ошибками,
    затем ожидает таймаут и проверяет что состояние переходит в HALF_OPEN
    и запросы снова разрешены.
    """
    cb = CircuitBreaker(failure_threshold=2, recovery_timeout=0.1)

    cb.record_failure()
    cb.record_failure()
    assert cb.state == "OPEN"

    time.sleep(0.15)
    cb._check_state()
    assert cb.state == "HALF_OPEN"
    assert cb.allow_request() is True


# Тест 006: Проверка, что Circuit Breaker закрывается после HALF_OPEN успеха.
def test_circuit_breaker_closes_after_half_open_success():
    """Проверяет что CircuitBreaker закрывается после успеха в состоянии HALF_OPEN.

    Создаёт CircuitBreaker, открывает его ошибками, ожидает таймаут для
    перехода в HALF_OPEN, вызывает record_success и проверяет что
    состояние возвращается в CLOSED.
    """
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
    """Проверяет что make_request_with_retry успешно выполняет запрос.

    Создаёт моковый HTTPRequestor и вызывает make_request_with_retry,
    проверяя что результат возвращается корректно.
    """
    mock_requestor = MagicMock(spec=HTTPRequestor)
    mock_requestor.get.return_value = {"key": "value"}

    result = make_request_with_retry(mock_requestor, "https://example.com/api")
    assert result["key"] == "value"


# Тест 008: Проверка что make_request_with_retry обрабатывает Timeout.
def test_make_request_with_retry_timeout():
    """Проверяет что make_request_with_retry повторяет запрос при Timeout.

    Создаёт моковый HTTPRequestor который первый раз бросает Timeout,
    а второй раз возвращает успешный результат, проверяя что функция
    успешно выполняет повторный запрос.
    """
    mock_requestor = MagicMock(spec=HTTPRequestor)
    call_count = 0

    def mock_get(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            raise requests.exceptions.Timeout("Timeout")
        return {"key": "value"}

    mock_requestor.get.side_effect = mock_get
    result = make_request_with_retry(mock_requestor, "https://example.com/api")
    assert result["key"] == "value"
    assert call_count == 2  # Первый вызов упал, второй успешный


# Тест 009: Проверка что make_request_with_retry передаёт timeout.
def test_make_request_with_retry_timeout_param():
    """Проверяет что make_request_with_retry корректно передаёт параметр timeout.

    Создаёт моковый HTTPRequestor и вызывает make_request_with_retry
    с timeout=15.0, проверяя что параметр timeout передаётся в метод get.
    """
    mock_requestor = MagicMock(spec=HTTPRequestor)
    mock_requestor.get.return_value = {"key": "value"}

    make_request_with_retry(mock_requestor, "https://example.com/api", timeout=15.0)
    mock_requestor.get.assert_called_once()
    assert mock_requestor.get.call_args[1]["timeout"] == 15.0


# Тест 010: Проверка что make_request_with_retry пробрасывает RequestException.
def test_make_request_with_retry_request_exception():
    """Проверяет что make_request_with_retry пробрасывает RequestException.

    Создаёт моковый HTTPRequestor который бросает ConnectionError,
    и проверяет что функция пробрасывает это исключение.
    """
    mock_requestor = MagicMock(spec=HTTPRequestor)
    mock_requestor.get.side_effect = requests.exceptions.ConnectionError("Connection refused")

    with pytest.raises(requests.exceptions.ConnectionError):
        make_request_with_retry(mock_requestor, "https://example.com/api")


# Тест 011: Проверка что make_request_with_retry пробрасывает ValueError.
def test_make_request_with_retry_value_error():
    """Проверяет что make_request_with_retry пробрасывает ValueError.

    Создаёт моковый HTTPRequestor который бросает ValueError,
    и проверяет что функция пробрасывает это исключение.
    """
    mock_requestor = MagicMock(spec=HTTPRequestor)
    mock_requestor.get.side_effect = ValueError("Invalid JSON")

    with pytest.raises(ValueError) as exc_info:
        make_request_with_retry(mock_requestor, "https://example.com/api")

    assert "Некорректный JSON-ответ" in str(exc_info.value)
