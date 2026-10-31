# -*- coding: utf-8 -*-
"""
Модуль содержит фабрику для создания объектов Aeroplane из JSON-данных.

Реализует принцип единственной ответственности (SRP):
выносит логику преобразования JSON в объекты из класса Aeroplane.
"""

from typing import Any, Dict, List

from src.application.aeroplane import Aeroplane


class AeroplaneFactory:
    """
    Фабрика для создания объектов Aeroplane из JSON-данных.

    Отвечает только за преобразование данных из внешнего формата
    (список списков opensky-network.org) в объекты Aeroplane.

    Не содержит бизнес-логики, валидации или сравнения —
    это чистая фабрика данных.
    """

    @staticmethod
    def create_from_json(json_data: List[List[Any]]) -> List[Aeroplane]:
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
