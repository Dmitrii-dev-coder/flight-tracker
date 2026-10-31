# -*- coding: utf-8 -*-
"""
Модуль содержит реализацию HTTP-запросов через библиотеку requests.

Является конкретной реализацией абстракции HTTPRequestor.
"""

from typing import Any, Dict, Optional
import requests
from src.infrastructure.http_requestor import HTTPRequestor


class RequestsHTTPClient(HTTPRequestor):
    """
    Реализация HTTPRequestor через библиотеку requests.

    Конкретный класс для выполнения HTTP-запросов.
    Может быть подменён на мок при тестировании.
    """

    def __init__(self):
        """
        Инициализация HTTP-клиента с заголовками по умолчанию.

        Nominatim API требует заголовок User-Agent.
        """
        self._headers = {"User-Agent": "FlightTracker/1.0 (coursework)"}

    def get(self, url: str, params: Optional[Dict[str, Any]] = None, timeout: float = 10.0) -> dict:
        """
        Выполнить GET-запрос через requests.

        Args:
            url: URL адрес для запроса.
            params: Словарь с параметрами запроса.
            timeout: Таймаут запроса в секундах.

        Returns:
            Словарь с распарсенным JSON-ответом.

        Raises:
            requests.exceptions.RequestException: При ошибке сетевого запроса.
            ValueError: При некорректном формате ответа.
        """
        response = requests.get(url, params=params, headers=self._headers, timeout=timeout)
        response.raise_for_status()
        return response.json()
