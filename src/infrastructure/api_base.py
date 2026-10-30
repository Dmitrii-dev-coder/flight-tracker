"""
Модуль содержит абстрактный класс для работы с API сервисов.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class APIConnector(ABC):
    """
    Абстрактный базовый класс для коннекторов к внешним API.

    Определяет общий интерфейс для подключения к API сервисам,
    получения географических координат стран и информации о самолётах.
    Реализует принцип единственной ответственности (SRP) — один класс,
    один тип взаимодействия с API.
    """

    @abstractmethod
    def get_country_coordinates(self, country: str) -> list:
        """
        Получить географические координаты страны.

        Возвращает boundingbox — список координат [min_lat, max_lat, min_lon, max_lon],
        определяющих прямоугольную область страны.

        Args:
            country: Название страны на английском языке.

        Returns:
            Список из 4 чисел с координатами границы страны.

        Raises:
            requests.exceptions.RequestException: При ошибке сетевого запроса.
            ValueError: При отсутствии данных о стране.
        """
        pass

    @abstractmethod
    def get_aeroplanes(self, country: str) -> list:
        """
        Получить информацию о самолётах в воздушном пространстве страны.

        Использует географические координаты страны для фильтрации
        самолётов из API opensky-network.org.

        Args:
            country: Название страны на английском языке.

        Returns:
            Список словарей с данными о самолётах.

        Raises:
            requests.exceptions.RequestException: При ошибке сетевого запроса.
            ValueError: При отсутствии данных о стране или самолётах.
        """
        pass

    @abstractmethod
    def make_request(self, url: str, params: Optional[Dict[str, Any]] = None) -> dict:
        """
        Выполнить HTTP-запрос к API.

        Общий метод для отправки GET-запросов с обработкой ошибок
        и парсингом JSON-ответа.

        Args:
            url: URL адрес для запроса.
            params: Словарь с параметрами запроса.

        Returns:
            Словарь с распарсенным JSON-ответом.

        Raises:
            requests.exceptions.RequestException: При ошибке сетевого запроса.
            ValueError: При некорректном формате ответа.
        """
        pass
