# -*- coding: utf-8 -*-
"""
Модуль содержит абстрактный базовый класс для информации о самолётах.
"""

from abc import ABC, abstractmethod


class AeroplaneBase(ABC):
    """
    Абстрактный базовый класс для информации о самолётах.

    Определяет общий интерфейс для работы с данными о самолётах:
    - Геттеры для доступа к атрибутам
    - Методы сравнения
    - Магические методы
    - Метод преобразования из JSON

    Наследуется от ABC, все ключевые методы имеют декоратор @abstractmethod.
    """

    @property
    @abstractmethod
    def callsign(self) -> str:
        """Получить позывной рейса."""
        pass

    @property
    @abstractmethod
    def country(self) -> str:
        """Получить страну регистрации."""
        pass

    @property
    @abstractmethod
    def velocity(self) -> float:
        """Получить горизонтальную скорость (м/с)."""
        pass

    @property
    @abstractmethod
    def altitude(self) -> float:
        """Получить барометрическую высоту (м)."""
        pass

    @property
    @abstractmethod
    def latitude(self) -> float:
        """Получить широту."""
        pass

    @property
    @abstractmethod
    def longitude(self) -> float:
        """Получить долготу."""
        pass

    @property
    @abstractmethod
    def on_ground(self) -> bool:
        """Получить статус (на земле или в воздухе)."""
        pass

    @property
    @abstractmethod
    def geo_altitude(self) -> float:
        """Получить геометрическую высоту (м)."""
        pass

    @property
    @abstractmethod
    def vertical_rate(self) -> float:
        """Получить вертикальную скорость (м/с)."""
        pass

    @property
    @abstractmethod
    def true_track(self) -> float:
        """Получить курс (градусы)."""
        pass

    @abstractmethod
    def _validate(self):
        """
        Валидация входных данных.

        Должен быть реализован в подклассе.
        """
        pass

    @abstractmethod
    def __str__(self):
        """
        Получить человекочитаемое представление самолёта.
        """
        pass

    @abstractmethod
    def __repr__(self):
        """
        Получить детальное представление самолёта.
        """
        pass

    @abstractmethod
    def __eq__(self, other):
        """
        Сравнить два самолёта по позывному.
        """
        pass

    @abstractmethod
    def __lt__(self, other):
        """
        Сравнить по скорости (возрастание).
        """
        pass

    @abstractmethod
    def __gt__(self, other):
        """
        Сравнить по скорости (убывание).
        """
        pass

    @abstractmethod
    def __le__(self, other):
        """
        Сравнить по скорости (<=).
        """
        pass

    @abstractmethod
    def __ge__(self, other):
        """
        Сравнить по скорости (>=).
        """
        pass

    @staticmethod
    @abstractmethod
    def cast_to_object_list(json_data: list) -> list:
        """
        Преобразовать список JSON-данных в список объектов Aeroplane.
        """
        pass
