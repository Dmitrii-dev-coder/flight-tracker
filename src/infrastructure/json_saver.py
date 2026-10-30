# -*- coding: utf-8 -*-
"""
Модуль содержит класс для сохранения информации о самолётах в JSON-файл.
"""

import json
import os
from src.infrastructure.file_connector import FileConnector


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

        Raises:
            FileNotFoundError: Если файл не существует.
            json.JSONDecodeError: Если файл содержит некорректный JSON.
        """
        try:
            with open(self._filepath, encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Файл не найден: {self._filepath}")
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(
                f"Некорректный JSON в файле {self._filepath}: {e.msg}",
                e.doc,
                e.pos
            )

    def _save_data(self, data: list):
        """
        Сохранить данные в JSON-файл.

        Args:
            data: Список словарей с данными о самолётах.

        Raises:
            IOError: При ошибке записи в файл.
        """
        try:
            with open(self._filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except IOError as e:
            raise IOError(f"Ошибка записи в файл {self._filepath}: {e}")

    def add_aeroplane(self, aeroplane):
        """
        Добавить информацию о самолёте в JSON-файл.

        Args:
            aeroplane: Объект Aeroplane для сохранения.

        Raises:
            IOError: При ошибке записи в файл.
            AttributeError: Если объект не имеет необходимых атрибутов.
        """
        try:
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
        except AttributeError as e:
            raise AttributeError(f"Объект не имеет необходимых атрибутов: {e}")

    def delete_aeroplane(self, aeroplane):
        """
        Удалить информацию о самолёте из JSON-файла.

        Args:
            aeroplane: Объект Aeroplane для удаления.

        Raises:
            IOError: При ошибке записи в файл.
            AttributeError: Если объект не имеет необходимых атрибутов.
        """
        try:
            data = self._load_data()
            data = [item for item in data if item.get("callsign") != aeroplane.callsign]
            self._save_data(data)
        except AttributeError as e:
            raise AttributeError(f"Объект не имеет необходимых атрибутов: {e}")

    def get_aeroplanes(self, **filters):
        """
        Получить список самолётов из файла по критериям.

        Args:
            **filters: Критерии фильтрации (country, velocity, altitude).

        Returns:
            Список объектов Aeroplane, соответствующих критериям.

        Raises:
            IOError: При ошибке чтения файла.
            ValueError: Если фильтр содержит неизвестный ключ.
        """
        from src.application.aeroplane import Aeroplane

        try:
            data = self._load_data()
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Ошибка чтения файла: {e}")
            return []

        aeroplanes = []

        for item in data:
            try:
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
            except ValueError as e:
                print(f"Ошибка создания объекта самолёта: {e}")
                continue

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
