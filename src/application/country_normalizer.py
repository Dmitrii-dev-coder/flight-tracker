# -*- coding: utf-8 -*-
"""
Модуль для нормализации названий стран.

Позволяет пользователю вводить названия стран на русском или английском языке,
и преобразует их в официальные английские названия, которые понимает API.

Использует pycountry для поиска стран по английским названиям и ISO кодам.
Для русского ввода используется встроенный словарь.
"""

from typing import List, Tuple

import pycountry


# Словарь: русское название -> английское название
# Покрывает основные страны, используемые в проекте
RU_TO_EN = {
    "россия": "Russia",
    "сша": "United States",
    "германия": "Germany",
    "франция": "France",
    "великобритания": "United Kingdom",
    "италия": "Italy",
    "испания": "Spain",
    "канада": "Canada",
    "китай": "China",
    "япония": "Japan",
    "индия": "India",
    "бразилия": "Brazil",
    "австралия": "Australia",
    " argentina": "Argentina",
    "мексика": "Mexico",
    "южная корея": "South Korea",
    "северная корея": "North Korea",
    "турция": "Turkey",
    "саудовская аравия": "Saudi Arabia",
    "египет": "Egypt",
    "южная африка": "South Africa",
    "швеция": "Sweden",
    "норвегия": "Norway",
    "финляндия": "Finland",
    "нидерланды": "Netherlands",
    "беларусь": "Belarus",
    "казахстан": "Kazakhstan",
    "украина": "Ukraine",
    "узбекистан": "Uzbekistan",
    "грузия": "Georgia",
    "армения": "Armenia",
    "azerbaijan": "Azerbaijan",
    "поля": "Poland",
    "чехия": "Czech Republic",
    "австрия": "Austria",
    "швейцария": "Switzerland",
    "португалия": "Portugal",
    "greece": "Greece",
    "болгария": "Bulgaria",
    "румыния": "Romania",
    "венгрия": "Hungary",
    "таиланд": "Thailand",
    "вьетнам": "Vietnam",
    "индонезия": "Indonesia",
    "пакистан": "Pakistan",
    "бангладеш": "Bangladesh",
}


def normalize_country(name: str) -> str:
    """
    Нормализовать название страны.

    Пытается найти страну по русскому или английскому названию,
    а также по ISO коду (например, 'RU', 'US', 'DE').

    Args:
        name: Название страны на русском или английском языке.

    Returns:
        Официальное английское название страны или None.
    """
    if not name or not name.strip():
        return None

    normalized = name.strip().lower()

    # Сначала ищем в словаре рус->англ
    if normalized in RU_TO_EN:
        return RU_TO_EN[normalized]

    # Затем ищем через pycountry (английский, ISO коды)
    try:
        result = pycountry.countries.search_fuzzy(normalized)
        if result:
            return result[0].name
    except (AttributeError, LookupError):
        pass

    return None


def normalize_countries(names: List[str]) -> Tuple[List[str], List[str]]:
    """
    Нормализовать список названий стран.

    Args:
        names: Список названий стран для нормализации.

    Returns:
        Кортеж из двух списков: (нормализованные, нераспознанные).
    """
    normalized = []
    unknown = []

    for name in names:
        result = normalize_country(name)
        if result:
            normalized.append(result)
        else:
            unknown.append(name.strip())

    return normalized, unknown
