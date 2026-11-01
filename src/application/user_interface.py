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
from src.application.country_normalizer import normalize_countries, normalize_country, save_translation


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

    # Фильтрация по стране
    filter_words = input("\nВведите названия стран для фильтрации (через пробел): ").split()
    if filter_words:
        normalized, unknown = normalize_countries(filter_words)
        if unknown:
            print(f"\nВнимание: страны не распознаны: {', '.join(unknown)}")
            print("\nРекомендуемые ресурсы для проверки названий:")
            print("- Wikipedia: Список стран по алфавиту (на русском и английском)")
            print("- GeoNames: geonames.org (официальные названия на всех языках)")
            print("- ISO 3166: iso.org (официальный стандарт кодов стран)")
            print("\nВведите 'y' для добавления в словарь, 'n' для пропуска:")
            answer = input("> ").strip().lower()
            if answer == "y":
                for ru_name in unknown:
                    en_name = input(f"Введите английское название для '{ru_name}': ").strip()
                    if en_name:
                        if save_translation(ru_name, en_name):
                            print(f"Добавлено: {ru_name} → {en_name}")
                            # Повторная нормализация для добавленной страны
                            normalized_en = normalize_country(ru_name)
                            normalized.append(normalized_en)
                        else:
                            print("Ошибка: не удалось сохранить перевод")
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
