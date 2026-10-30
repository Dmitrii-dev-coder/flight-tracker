# -*- coding: utf-8 -*-
"""
Модуль содержит абстрактный класс для HTTP-запросов.

Реализует принцип инверсии зависимостей (DIP):
вместо прямой зависимости от requests — зависимость от абстракции.
Это упрощает тестирование и замену HTTP-клиента.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class HTTPRequestor(ABC):
    """
    Абстрактный базовый класс для выполнения HTTP-запросов.

    Определяет общий интерфейс для отправки GET-запросов.
    Позволяет подменять реальный HTTP-клиент на мок при тестировании.

    Реализует принцип инверсии зависимостей (DIP):
    модули высокого уровня (AeroplanesAPI) зависят от абстракции,
    а не от конкретной библиотеки requests.
    """

    @abstractmethod
    def get(self, url: str, params: Optional[Dict[str, Any]] = None, timeout: float = 10.0) -> dict:
        """
        Выполнить GET-запрос.

        Args:
            url: URL адрес для запроса.
            params: Словарь с параметрами запроса.
            timeout: Таймаут запроса в секундах.

        Returns:
            Словарь с распарсенным JSON-ответом.

        Raises:
            requests.exceptions.RequestException: При ошибке сетевого запроса.
            ValueError: При некорректном формате ответа.
        """
        pass
