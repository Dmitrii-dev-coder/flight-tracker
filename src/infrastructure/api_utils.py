# -*- coding: utf-8 -*-
"""
Модуль содержит паттерны устойчивого подключения к внешним API.

Реализует:
- Retry с Jitter — повтор запросов с увеличивающейся задержкой и случайным разбросом
- Circuit Breaker — временное отключение API при частых ошибках
"""

import time
import random
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import requests


class CircuitBreaker:
    """
    Паттерн Circuit Breaker — предотвращает повторные запросы к недоступному API.

    Работает в трёх состояниях:
    - CLOSED — запросы проходят нормально
    - OPEN — API недоступен, запросы отклоняются
    - HALF_OPEN — тестовый запрос после таймаута
    """

    def __init__(self, failure_threshold: int = 5, recovery_timeout: float = 30.0):
        """
        Инициализация Circuit Breaker.

        Args:
            failure_threshold: Количество ошибок для перехода в OPEN
            recovery_timeout: Время ожидания перед HALF_OPEN (секунды)
        """
        self._failure_threshold = failure_threshold
        self._recovery_timeout = recovery_timeout
        self._failure_count = 0
        self._last_failure_time = None
        self._state = "CLOSED"

    def _check_state(self):
        """Проверка и обновление состояния Circuit Breaker."""
        if self._state == "OPEN" and self._last_failure_time:
            elapsed = time.time() - self._last_failure_time
            if elapsed > self._recovery_timeout:
                self._state = "HALF_OPEN"

    def record_success(self):
        """Зафиксировать успешный запрос."""
        self._failure_count = 0
        self._state = "CLOSED"

    def record_failure(self):
        """Зафиксировать ошибку запроса."""
        self._failure_count += 1
        self._last_failure_time = time.time()

        if self._failure_count >= self._failure_threshold:
            self._state = "OPEN"

    def allow_request(self) -> bool:
        """
        Проверить, можно ли выполнить запрос.

        Returns:
            True если запрос разрешён, False если Circuit Breaker открыт.
        """
        self._check_state()
        return self._state != "OPEN"

    @property
    def state(self) -> str:
        """Текущее состояние Circuit Breaker."""
        return self._state


def make_request_with_retry(url: str, params: dict = None, timeout: float = 10.0) -> dict:
    """
    Выполнить HTTP-запрос с паттернами Retry и Jitter.

    Retry: до 3 попыток с увеличивающейся задержкой
    Jitter: случайная задержка 0-2 секунды после базовой паузы

    Args:
        url: URL для запроса
        params: Словарь с параметрами запроса
        timeout: Таймаут запроса в секундах

    Returns:
        Словарь с распарсенным JSON-ответом

    Raises:
        requests.exceptions.RequestException: При повторяющихся ошибках
        ValueError: При некорректном JSON-ответе
    """
    try:
        response = requests.get(url, params=params, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        # Retry с Jitter
        time.sleep(1 + random.uniform(0, 2))
        response = requests.get(url, params=params, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        raise
    except ValueError:
        raise ValueError(f"Некорректный JSON-ответ от {url}")
