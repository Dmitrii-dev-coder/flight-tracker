# -*- coding: utf-8 -*-
"""
Модуль содержит класс для работы с API opensky-network.org.
"""

from typing import Any, Dict, Optional
from src.infrastructure.api_base import APIConnector
from src.infrastructure.api_utils import CircuitBreaker
from src.infrastructure.http_requestor import HTTPRequestor


class AeroplanesAPI(APIConnector):
    """
    Класс для работы с API nominatim.openstreetmap.org и opensky-network.org.

    Наследуется от APIConnector и реализует методы для получения
    географических координат стран и информации о самолётах.
    Реализует принципы SRP, OCP и DIP.

    DIP: использует HTTPRequestor абстракцию вместо прямого импорта requests.
    """

    def __init__(self, http_requestor: Optional[HTTPRequestor] = None):
        """
        Инициализация коннектора к API.

        Args:
            http_requestor: HTTP-клиент для выполнения запросов.
                           Если None, создаётся RequestsHTTPClient.
        """
        if http_requestor is None:
            self._http_requestor: HTTPRequestor = self._create_default_requestor()
        else:
            self._http_requestor = http_requestor

        self.nominatim_url = "https://nominatim.openstreetmap.org/search"
        self.opensky_url = "https://opensky-network.org/api/states/all"
        self._circuit_breaker = CircuitBreaker(failure_threshold=5, recovery_timeout=30.0)

    def _create_default_requestor(self) -> HTTPRequestor:
        """
        Создать HTTP-клиент по умолчанию.

        Используется как фабрика для создания HTTPRequestor.
        Позволяет переопределить в подклассах для тестирования.

        Returns:
            Экземпляр HTTPRequestor.
        """
        from src.infrastructure.requests_http_client import RequestsHTTPClient
        return RequestsHTTPClient()

    def make_request(self, url: str, params: Optional[Dict[str, Any]] = None) -> dict:
        """
        Выполнить HTTP-запрос к API с Circuit Breaker.

        Проверяет состояние Circuit Breaker перед выполнением запроса.
        При успешном запросе сбрасывает счётчик ошибок,
        при ошибке — увеличивает счётчик.

        Args:
            url: URL адрес для запроса.
            params: Словарь с параметрами запроса.

        Returns:
            Словарь с распарсенным JSON-ответом.

        Raises:
            requests.exceptions.RequestException: При ошибке сетевого запроса.
            ValueError: При некорректном формате ответа.
        """
        if not self._circuit_breaker.allow_request():
            raise RuntimeError(
                f"Circuit Breaker открыт (состояние: {self._circuit_breaker.state}). "
                f"Попробуйте позже"
            )

        try:
            result = self._http_requestor.get(url, params=params, timeout=10.0)
            self._circuit_breaker.record_success()
            return result
        except RuntimeError:
            self._circuit_breaker.record_failure()
            raise
        except ValueError:
            self._circuit_breaker.record_failure()
            raise ValueError(f"Некорректный JSON-ответ от {url}")

    def get_country_coordinates(self, country: str) -> list:
        """
        Получить географические координаты страны.

        Выполняет запрос к nominatim.openstreetmap.org и возвращает
        boundingbox — список координат [min_lat, max_lat, min_lon, max_lon].

        Args:
            country: Название страны на английском языке.

        Returns:
            Список из 4 чисел с координатами границы страны.

        Raises:
            requests.exceptions.RequestException: При ошибке сетевого запроса.
            ValueError: При отсутствии данных о стране.
        """
        params = {
            "format": "json",
            "q": country,
            "limit": 1
        }

        result = self.make_request(self.nominatim_url, params)

        if not result:
            raise ValueError(f"Страна не найдена: {country}")

        boundingbox = result[0].get("boundingbox")
        if not boundingbox:
            raise ValueError(f"Нет координат для страны: {country}")

        return [float(coord) for coord in boundingbox]

    def get_aeroplanes(self, country: str) -> list:
        """
        Получить информацию о самолётах в воздушном пространстве страны.

        Получает boundingbox страны, затем запрашивает все самолёты
        из opensky-network.org и фильтрует по координатам.

        Args:
            country: Название страны на английском языке.

        Returns:
            Список словарей с данными о самолётах в пределах страны.

        Raises:
            requests.exceptions.RequestException: При ошибке сетевого запроса.
            ValueError: При отсутствии данных о стране или самолётах.
        """
        try:
            bbox = self.get_country_coordinates(country)
        except ValueError:
            raise

        params: Dict[str, Any] = {}
        result = self.make_request(self.opensky_url, params)

        if not result or "states" not in result:
            return []

        states = result["states"]
        min_lat, max_lat, min_lon, max_lon = bbox

        filtered = []
        for state in states:
            if state is None:
                continue

            longitude = state[5]
            latitude = state[6]

            if longitude is None or latitude is None:
                continue

            if (min_lon <= longitude <= max_lon
                    and min_lat <= latitude <= max_lat):
                filtered.append(state)

        return filtered
