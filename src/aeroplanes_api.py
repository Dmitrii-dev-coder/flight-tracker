# -*- coding: utf-8 -*-
"""
Модуль содержит класс для работы с API opensky-network.org.
"""

import requests
from src.api_base import APIConnector


class AeroplanesAPI(APIConnector):
    """
    Класс для работы с API nominatim.openstreetmap.org и opensky-network.org.

    Наследуется от APIConnector и реализует методы для получения
    географических координат стран и информации о самолётах.
    Реализует принципы SRP и OCP.
    """

    def __init__(self):
        """
        Инициализация коннектора к API.

        Устанавливает базовые URL для nominatim и opensky API.
        """
        self.nominatim_url = "https://nominatim.openstreetmap.org/search"
        self.opensky_url = "https://opensky-network.org/api/states/all"

    def make_request(self, url: str, params: dict = None) -> dict:
        """
        Выполнить HTTP-запрос к API.

        Args:
            url: URL адрес для запроса.
            params: Словарь с параметрами запроса.

        Returns:
            Словарь с распарсенным JSON-ответом.

        Raises:
            requests.exceptions.RequestException: При ошибке сетевого запроса.
            ValueError: При некорректном формате ответа.
        """
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException:
            raise
        except ValueError:
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

        params = {}
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

            if (min_lon <= longitude <= max_lon and
                    min_lat <= latitude <= max_lat):
                filtered.append(state)

        return filtered
