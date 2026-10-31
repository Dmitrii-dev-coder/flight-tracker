# -*- coding: utf-8 -*-
"""
Модуль содержит функцию для взаимодействия с пользователем через консоль.
"""

from src.application.filters import (
    filter_by_country,
    filter_by_altitude_range,
    sort_by_altitude_desc,
    get_top_n
)
from src.application.country_normalizer import normalize_countries, normalize_country


def print_aeroplanes(aeroplanes: list):
    """
    Вывести информацию о самолётах в человекочитаемом формате.

    Args:
        aeroplanes: Список объектов Aeroplane.
    """
    if not aeroplanes:
        print("Самолёты не найдены")
        return

    print(f"{'№':<5} {'Позывной':<15} {'Страна':<20} {'Скорость (м/с)':<15} {'Высота (м)':<12}")
    print("-" * 67)

    for i, plane in enumerate(aeroplanes, 1):
        print(f"{i:<5} {plane.callsign:<15} {plane.country:<20} {plane.velocity:<15.1f} {plane.altitude:<12.1f}")


def user_interaction(aeroplanes: list):
    """
    Взаимодействие с пользователем через консоль.

    Предоставляет пользователю возможности:
    1. Получить топ N самолётов по высоте полёта.
    2. Получить самолёты по стране их регистрации.
    3. Отфильтровать по диапазону высот полёта.

    Args:
        aeroplanes: Список объектов Aeroplane для обработки.
    """
    print("\n=== Трекер самолётов ===")
    print(f"Всего самолётов: {len(aeroplanes)}\n")

    # Топ N самолётов по высоте
    try:
        top_n = int(input("Введите количество самолётов для вывода в топ N: "))
        sorted_planes = sort_by_altitude_desc(aeroplanes)
        top_planes = get_top_n(sorted_planes, top_n)
        print(f"\n--- Топ {top_n} самолётов по высоте ---")
        print_aeroplanes(top_planes)
    except ValueError:
        print("Ошибка: введите корректное число для топ N")

    # Вывод списка самолётов
    print_aeroplanes(aeroplanes)

    # Фильтрация по стране
    filter_words = input("\nВведите названия стран для фильтрации (через пробел): ").split()
    if filter_words:
        normalized, unknown = normalize_countries(filter_words)
        if unknown:
            print(f"\nВнимание: страны не распознаны: {', '.join(unknown)}")
        if normalized:
            # Показываем, как были распознаны названия стран
            for original, english in zip(filter_words, normalized):
                if original != english:
                    print(f"Распознано: {original} → {english}")
            filtered = filter_by_country(aeroplanes, normalized)
            print(f"\n--- Самолёты в стране: {', '.join(normalized)} ---")
            print_aeroplanes(filtered)
        else:
            print("Страны не найдены")

    # Фильтрация по диапазону высот
    altitude_input = input("\nВведите диапазон высот полёта (например: 1000 - 5000): ")
    try:
        parts = altitude_input.split("-")
        if len(parts) == 2:
            min_alt = float(parts[0].strip())
            max_alt = float(parts[1].strip())
            ranged = filter_by_altitude_range(aeroplanes, min_alt, max_alt)
            print(f"\n--- Самолёты в диапазоне высот {min_alt} - {max_alt} м ---")
            print_aeroplanes(ranged)
    except ValueError:
        print("Ошибка: введите корректный диапазон (например: 1000 - 5000)")
