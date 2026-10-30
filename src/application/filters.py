# -*- coding: utf-8 -*-
"""
Модуль содержит функции для фильтрации и сортировки самолётов.
"""


def filter_by_country(aeroplanes: list, countries: list) -> list:
    """
    Отфильтровать самолёты по стране регистрации.

    Args:
        aeroplanes: Список объектов Aeroplane.
        countries: Список названий стран для фильтрации.

    Returns:
        Список самолётов, зарегистрированных в указанных странах.
    """
    return [plane for plane in aeroplanes if plane.country in countries]


def filter_by_altitude_range(aeroplanes: list, min_alt: float, max_alt: float) -> list:
    """
    Отфильтровать самолёты по диапазону высоты полёта.

    Args:
        aeroplanes: Список объектов Aeroplane.
        min_alt: Минимальная высота (м).
        max_alt: Максимальная высота (м).

    Returns:
        Список самолётов в указанном диапазоне высот.

    Raises:
        ValueError: Если min_alt > max_alt.
    """
    if min_alt > max_alt:
        raise ValueError(f"Минимальная высота ({min_alt}) больше максимальной ({max_alt})")

    return [plane for plane in aeroplanes if min_alt <= plane.altitude <= max_alt]


def sort_by_altitude_desc(aeroplanes: list) -> list:
    """
    Отсортировать самолёты по убыванию высоты полёта (DESC).

    Args:
        aeroplanes: Список объектов Aeroplane.

    Returns:
        Отсортированный список (от большей высоты к меньшей).
    """
    return sorted(aeroplanes, key=lambda x: x.altitude, reverse=True)


def get_top_n(aeroplanes: list, n: int) -> list:
    """
    Получить топ N самолётов.

    Args:
        aeroplanes: Список объектов Aeroplane (должен быть отсортирован).
        n: Количество самолётов для возврата.

    Returns:
        Список из N самолётов.

    Raises:
        ValueError: Если n < 0.
    """
    if n < 0:
        raise ValueError(f"Количество не может быть отрицательным: {n}")

    return aeroplanes[:n]


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
