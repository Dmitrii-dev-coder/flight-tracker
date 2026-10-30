# -*- coding: utf-8 -*-
"""
Модуль содержит абстрактный класс для данных самолёта.

Реализует принцип разделения интерфейсов (ISP):
только данные, без методов сравнения и сериализации.
"""

from abc import ABC, abstractmethod


class AeroplaneData(ABC):
    """
    Абстрактный базовый класс для данных самолёта.

    Определяет только геттеры для доступа к атрибутам самолёта.
    Не включает методы сравнения или сериализации.

    Реализует принцип разделения интерфейсов (ISP):
    клиент, которому нужны только данные, не зависит от методов сравнения.
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
