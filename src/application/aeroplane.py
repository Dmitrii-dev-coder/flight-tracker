# -*- coding: utf-8 -*-
"""
Модуль содержит класс для работы с информацией о самолётах.
"""

from src.application.aeroplane_base import AeroplaneBase


class Aeroplane(AeroplaneBase):
    """
    Класс для хранения и обработки информации о самолёте.

    Наследуется от AeroplaneBase, который в свою очередь
    наследуется от AeroplaneData (данные) и AeroplaneComparable (сравнение).

    Инкапсулирует данные о самолёте: позывной, страну регистрации,
    скорость, высоту и другие параметры. Поддерживает сравнение
    по скорости и высоте, валидацию входных данных.
    """

    def __init__(
        self,
        callsign: str,
        country: str,
        velocity: float,
        altitude: float,
        latitude: float = 0.0,
        longitude: float = 0.0,
        on_ground: bool = False,
        geo_altitude: float = 0.0,
        vertical_rate: float = 0.0,
        true_track: float = 0.0
    ):
        """
        Инициализация объекта самолёта.

        Args:
            callsign: Позывной рейса.
            country: Страна регистрации.
            velocity: Горизонтальная скорость (м/с).
            altitude: Барометрическая высота (м).
            latitude: Широта.
            longitude: Долгота.
            on_ground: Находится ли на земле.
            geo_altitude: Геометрическая высота (м).
            vertical_rate: Вертикальная скорость (м/с).
            true_track: Курс (градусы).

        Raises:
            ValueError: Если callsign пустой или скорость/высота отрицательные.
        """
        self._callsign = callsign
        self._country = country
        self._velocity = velocity
        self._altitude = altitude
        self._latitude = latitude
        self._longitude = longitude
        self._on_ground = on_ground
        self._geo_altitude = geo_altitude
        self._vertical_rate = vertical_rate
        self._true_track = true_track

        self._validate()

    def _validate(self):
        """
        Валидация входных данных.

        Raises:
            ValueError: Если данные некорректны.
        """
        if not self._callsign or not self._callsign.strip():
            raise ValueError("Позывной не может быть пустым")

        if self._velocity < 0:
            raise ValueError(f"Скорость не может быть отрицательной: {self._velocity}")

        if self._altitude < 0:
            raise ValueError(f"Высота не может быть отрицательной: {self._altitude}")

        if self._geo_altitude < 0:
            raise ValueError(f"Геометрическая высота не может быть отрицательной: {self._geo_altitude}")

    # --- Реализация абстрактных свойств AeroplaneData ---

    @property
    def callsign(self) -> str:
        """Получить позывной рейса."""
        return self._callsign

    @property
    def country(self) -> str:
        """Получить страну регистрации."""
        return self._country

    @property
    def velocity(self) -> float:
        """Получить горизонтальную скорость (м/с)."""
        return self._velocity

    @property
    def altitude(self) -> float:
        """Получить барометрическую высоту (м)."""
        return self._altitude

    @property
    def latitude(self) -> float:
        """Получить широту."""
        return self._latitude

    @property
    def longitude(self) -> float:
        """Получить долготу."""
        return self._longitude

    @property
    def on_ground(self) -> bool:
        """Получить статус (на земле или в воздухе)."""
        return self._on_ground

    @property
    def geo_altitude(self) -> float:
        """Получить геометрическую высоту (м)."""
        return self._geo_altitude

    @property
    def vertical_rate(self) -> float:
        """Получить вертикальную скорость (м/с)."""
        return self._vertical_rate

    @property
    def true_track(self) -> float:
        """Получить курс (градусы)."""
        return self._true_track

    # --- Реализация абстрактных методов AeroplaneComparable ---

    def __lt__(self, other):
        """
        Сравнить по скорости (возрастание).

        Args:
            other: Другой объект Aeroplane.

        Returns:
            True если скорость текущего меньше скорости другого.
        """
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return self._velocity < other._velocity

    def __gt__(self, other):
        """
        Сравнить по скорости (убывание).

        Args:
            other: Другой объект Aeroplane.

        Returns:
            True если скорость текущего больше скорости другого.
        """
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return self._velocity > other._velocity

    def __le__(self, other):
        """
        Сравнить по скорости (<=).

        Args:
            other: Другой объект Aeroplane.

        Returns:
            True если скорость текущего меньше или равна.
        """
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return self._velocity <= other._velocity

    def __ge__(self, other):
        """
        Сравнить по скорости (>=).

        Args:
            other: Другой объект Aeroplane.

        Returns:
            True если скорость текущего больше или равна.
        """
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return self._velocity >= other._velocity

    def __eq__(self, other):
        """
        Сравнить два самолёта по позывному.

        Args:
            other: Другой объект Aeroplane.

        Returns:
            True если позывные совпадают.
        """
        if not isinstance(other, Aeroplane):
            return False
        return self._callsign == other._callsign

    # --- Магические методы представления ---

    def __str__(self):
        """
        Получить человекочитаемое представление самолёта.

        Returns:
            Строка с основными данными о самолёте.
        """
        return (f"Aeroplane(callsign={self._callsign}, country={self._country}, "
                f"velocity={self._velocity}, altitude={self._altitude})")

    def __repr__(self):
        """
        Получить детальное представление самолёта.

        Returns:
            Строка с полным описанием объекта.
        """
        return (f"Aeroplane(callsign='{self._callsign}', country='{self._country}', "
                f"velocity={self._velocity}, altitude={self._altitude}, "
                f"latitude={self._latitude}, longitude={self._longitude}, "
                f"on_ground={self._on_ground}, geo_altitude={self._geo_altitude}, "
                f"vertical_rate={self._vertical_rate}, true_track={self._true_track})")

    # --- Сериализация ---

    @staticmethod
    def cast_to_object_list(json_data: list) -> list:
        """
        Преобразовать список JSON-данных в список объектов Aeroplane.

        Структура JSON-массива соответствует ответу opensky-network.org:
        [icao24, callsign, country, time_position, last_contact,
         longitude, latitude, baro_altitude, on_ground, velocity,
         true_track, vertical_rate, sensors, geo_altitude, squawk,
         spi, position_source]

        Args:
            json_data: Список списков с данными о самолётах.

        Returns:
            Список объектов Aeroplane.
        """
        aeroplanes = []
        for state in json_data:
            if state is None:
                continue

            callsign = state[1].strip() if state[1] else ""
            if not callsign:
                continue

            # Отрицательное значение altitude означает "недоступно" (специальное значение opensky)
            altitude = state[7] if state[7] is not None else 0.0
            if altitude < 0:
                altitude = 0.0

            aeroplanes.append(Aeroplane(
                callsign=callsign,
                country=state[2],
                velocity=state[9] if state[9] is not None else 0.0,
                altitude=altitude,
                latitude=state[6] if state[6] is not None else 0.0,
                longitude=state[5] if state[5] is not None else 0.0,
                on_ground=state[8] if state[8] is not None else False,
                geo_altitude=state[13] if state[13] is not None else 0.0,
                vertical_rate=state[11] if state[11] is not None else 0.0,
                true_track=state[10] if state[10] is not None else 0.0
            ))

        return aeroplanes
