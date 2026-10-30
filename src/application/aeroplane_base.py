# -*- coding: utf-8 -*-
"""
Модуль содержит абстрактный базовый класс для информации о самолётах.

Наследуется от разделённых интерфейсов ISP:
- AeroplaneData — только данные (10 свойств)
- AeroplaneComparable — только методы сравнения (6 магических методов)

Это устраняет нарушение ISP: клиент, которому нужны только данные,
не зависит от методов сравнения и сериализации.
"""

from abc import ABC, abstractmethod
from src.application.aeroplane_data import AeroplaneData
from src.application.aeroplane_comparable import AeroplaneComparable


class AeroplaneBase(AeroplaneData, AeroplaneComparable, ABC):
    """
    Абстрактный базовый класс для информации о самолётах.

    Наследуется от AeroplaneData (данные) и AeroplaneComparable (сравнение).
    Также определяет методы сериализации и магические методы представления.

    Реализует принцип разделения интерфейсов (ISP):
    данные и сравнение вынесены в отдельные интерфейсы.
    """

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

    @staticmethod
    @abstractmethod
    def cast_to_object_list(json_data: list) -> list:
        """
        Преобразовать список JSON-данных в список объектов Aeroplane.
        """
        pass
