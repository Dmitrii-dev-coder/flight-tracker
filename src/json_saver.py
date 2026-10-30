# -*- coding: utf-8 -*-
"""
Модуль содержит класс для сохранения информации о самолётах в JSON-файл.
"""

import json
import os
from src.file_connector import FileConnector


class JSONSaver(FileConnector):
    """
    Класс для сохранения информации о самолётах в JSON-файл.

    Реализует методы добавления, удаления и получения данных о самолётах
    из JSON-файла. Выступает в роли коннектора, который можно заменить
    на БД-коннектор при необходимости.
    """

    def __init__(self, filepath: str = "data/aeroplanes.json"):
        """
        Инициализация JSONSaver.

        Args:
            filepath: Путь к JSON-файлу для хранения данных.
        """
        self._filepath = filepath
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """Создать файл, если он не существует."""
        directory = os.path.dirname(self._filepath)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

        if not os.path.exists(self._filepath):
            with open(self._filepath, "w", encoding="utf-8") as f:
                json.dump([], f)

    def _load_data(self) -> list:
        """
        Загрузить данные из JSON-файла.

        Returns:
            Список словарей с данными о самолётах.
        """
        with open(self._filepath, encoding="utf-8") as f:
            return json.load(f)

    def _save_data(self, data: list):
        """
        Сохранить данные в JSON-файл.

        Args:
            data: Список словарей с данными о самолётах.
        """
        with open(self._filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def add_aeroplane(self, aeroplane):
        """
        Добавить информацию о самолёте в JSON-файл.

        Args:
            aeroplane: Объект Aeroplane для сохранения.
        """
        data = self._load_data()

        aeroplane_dict = {
            "callsign": aeroplane.callsign,
            "country": aeroplane.country,
            "velocity": aeroplane.velocity,
            "altitude": aeroplane.altitude,
            "latitude": aeroplane.latitude,
            "longitude": aeroplane.longitude,
            "on_ground": aeroplane.on_ground,
            "geo_altitude": aeroplane.geo_altitude,
            "vertical_rate": aeroplane.vertical_rate,
            "true_track": aeroplane.true_track
        }

        data.append(aeroplane_dict)
        self._save_data(data)

    def delete_aeroplane(self, aeroplane):
        """
        Удалить информацию о самолёте из JSON-файла.

        Args:
            aeroplane: Объект Aeroplane для удаления.
        """
        data = self._load_data()
        data = [item for item in data if item.get("callsign") != aeroplane.callsign]
        self._save_data(data)

    def get_aeroplanes(self, **filters):
        """
        Получить список самолётов из файла по критериям.

        Args:
            **filters: Критерии фильтрации (country, velocity, altitude).

        Returns:
            Список объектов Aeroplane, соответствующих критериям.
        """
        from src.aeroplane import Aeroplane

        data = self._load_data()
        aeroplanes = []

        for item in data:
            plane = Aeroplane(
                callsign=item.get("callsign", ""),
                country=item.get("country", ""),
                velocity=item.get("velocity", 0.0),
                altitude=item.get("altitude", 0.0),
                latitude=item.get("latitude", 0.0),
                longitude=item.get("longitude", 0.0),
                on_ground=item.get("on_ground", False),
                geo_altitude=item.get("geo_altitude", 0.0),
                vertical_rate=item.get("vertical_rate", 0.0),
                true_track=item.get("true_track", 0.0)
            )

            match = True
            for key, value in filters.items():
                if hasattr(plane, key):
                    plane_value = getattr(plane, key)
                    if plane_value != value:
                        match = False
                        break

            if match:
                aeroplanes.append(plane)

        return aeroplanes
