# -*- coding: utf-8 -*-
"""
Точка входа в программу "Трекер самолётов".

Объединяет все компоненты: API-коннектор, классы самолётов,
файловое хранилище и пользовательский интерфейс.
"""

import requests

from src.infrastructure.aeroplanes_api import AeroplanesAPI
from src.application.aeroplane import Aeroplane
from src.infrastructure.json_saver import JSONSaver
from src.application.user_interface import user_interaction
from src.application.country_normalizer import normalize_country


def main():
    """
    Главная функция программы.

    Получает данные о самолётах, сохраняет в JSON и запускает
    пользовательский интерфейс.
    """
    print("=== Трекер самолётов ===\n")

    # Создание экземпляра API-коннектора
    api = AeroplanesAPI()

    # Ввод названия страны
    country = input("Введите название страны: ").strip()

    if not country:
        print("Ошибка: название страны не может быть пустым")
        return

    # Нормализация названия страны
    normalized = normalize_country(country)
    if not normalized:
        print(f"Страна '{country}' не распознана")
        return

    if country != normalized:
        print(f"Распознано: {country} → {normalized}\n")

    # Получение данных о самолётах
    print(f"Получение данных о самолётах в воздушном пространстве {normalized}...")
    try:
        aeroplanes_data = api.get_aeroplanes(country)
    except requests.exceptions.RequestException as e:
        print(f"Ошибка подключения к API: {e}")
        print("Проверьте подключение к интернету и попробуйте снова")
        return

    if not aeroplanes_data:
        print(f"Самолёты в воздушном пространстве {normalized} не найдены")
        return

    print(f"Найдено {len(aeroplanes_data)} самолётов")

    # Преобразование в объекты
    aeroplanes = Aeroplane.cast_to_object_list(aeroplanes_data)
    print(f"Преобразовано {len(aeroplanes)} объектов\n")

    # Сохранение в JSON
    json_saver = JSONSaver()
    for plane in aeroplanes:
        json_saver.add_aeroplane(plane)
    print(f"Данные сохранены в {json_saver._filepath}\n")

    # Запуск пользовательского интерфейса
    user_interaction(aeroplanes)


if __name__ == "__main__":
    main()
