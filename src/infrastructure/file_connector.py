# -*- coding: utf-8 -*-
"""
Модуль содержит абстрактный класс для работы с файлами.
"""

from abc import ABC, abstractmethod


class FileConnector(ABC):
    """
    Абстрактный базовый класс для коннекторов к файловым хранилищам.

    Определяет общий интерфейс для добавления, удаления и получения
    информации о самолётах из файлов. Может быть заменён на БД-коннектор.
    """

    @abstractmethod
    def add_aeroplane(self, aeroplane):
        """
        Добавить информацию о самолёте в файл.

        Args:
            aeroplane: Объект Aeroplane для сохранения.

        Raises:
            NotImplementedError: Должен быть переопределён в подклассе.
        """
        pass

    @abstractmethod
    def delete_aeroplane(self, aeroplane):
        """
        Удалить информацию о самолёте из файла.

        Args:
            aeroplane: Объект Aeroplane для удаления.

        Raises:
            NotImplementedError: Должен быть переопределён в подклассе.
        """
        pass

    @abstractmethod
    def get_aeroplanes(self, **filters):
        """
        Получить список самолётов из файла по критериям.

        Args:
            **filters: Критерии фильтрации (страна, скорость, высота и т.д.).

        Returns:
            Список объектов Aeroplane, соответствующих критериям.

        Raises:
            NotImplementedError: Должен быть переопределён в подклассе.
        """
        pass
