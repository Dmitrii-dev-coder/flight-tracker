# -*- coding: utf-8 -*-
"""
Модуль содержит заглушку для сохранения информации о самолётах в CSV-файл.
"""

from src.file_connector import FileConnector


class CSVSaver(FileConnector):
    """
    Заглушка для сохранения информации о самолётах в CSV-файл.

    Может быть реализована в будущем для поддержки CSV-формата.
    """

    def add_aeroplane(self, aeroplane):
        """Добавить самолёт в CSV-файл (заглушка)."""
        raise NotImplementedError("CSV-сохранение ещё не реализовано")

    def delete_aeroplane(self, aeroplane):
        """Удалить самолёт из CSV-файла (заглушка)."""
        raise NotImplementedError("CSV-удаление ещё не реализовано")

    def get_aeroplanes(self, **filters):
        """Получить самолёты из CSV-файла (заглушка)."""
        raise NotImplementedError("CSV-чтение ещё не реализовано")
