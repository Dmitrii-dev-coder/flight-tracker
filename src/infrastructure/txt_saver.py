# -*- coding: utf-8 -*-
"""
Модуль содержит заглушку для сохранения информации о самолётах в TXT-файл.
"""

from src.infrastructure.file_connector import FileConnector


class TXTSaver(FileConnector):
    """
    Заглушка для сохранения информации о самолётах в TXT-файл.

    Может быть реализована в будущем для поддержки TXT-формата.
    """

    def add_aeroplane(self, aeroplane):
        """Добавить самолёт в TXT-файл (заглушка)."""
        raise NotImplementedError("TXT-сохранение ещё не реализовано")

    def delete_aeroplane(self, aeroplane):
        """Удалить самолёт из TXT-файла (заглушка)."""
        raise NotImplementedError("TXT-удаление ещё не реализовано")

    def get_aeroplanes(self, **filters):
        """Получить самолёты из TXT-файла (заглушка)."""
        raise NotImplementedError("TXT-чтение ещё не реализовано")
