# -*- coding: utf-8 -*-
"""
Модуль для нормализации названий стран.

Позволяет пользователю вводить названия стран на русском или английском языке,
и преобразует их в официальные английские названия, которые понимает API.

Использует pycountry для поиска стран по английским названиям и ISO кодам.
Для русского ввода используется встроенный словарь.
"""

import json
from pathlib import Path
from typing import List, Tuple

import pycountry


# Путь к файлу пользовательского словаря
_USER_DICT_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "country_translations.json"


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
    "аргентина": "Argentina",
    "мексика": "Mexico",
    "южная корея": "South Korea",
    "северная корея": "North Korea",
    "турция": "Turkey",
    "саудовская аравия": "Saudi Arabia",
    "египет": "Egypt",
    "южная африка": "South Africa",
    "юар": "South Africa",
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
    "азербайджан": "Azerbaijan",
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
    "куба": "Cuba",
}


def _load_user_dict() -> dict:
    """
    Загрузить пользовательский словарь из JSON-файла.

    Если файл не существует или невалиден — возвращает пустой словарь.

    Returns:
        Словарь {русское название: английское название}.
    """
    if not _USER_DICT_PATH.exists():
        return {}
    try:
        with open(_USER_DICT_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}


def save_translation(ru_name: str, en_name: str) -> bool:
    """
    Сохранить новый перевод страны в пользовательский словарь.

    Args:
        ru_name: Название страны на русском.
        en_name: Название страны на английском.

    Returns:
        True если сохранение успешно, False при ошибке.
    """
    user_dict = _load_user_dict()
    user_dict[ru_name.strip().lower()] = en_name.strip()
    try:
        with open(_USER_DICT_PATH, "w", encoding="utf-8") as f:
            json.dump(user_dict, f, ensure_ascii=False, indent=2)
        return True
    except IOError:
        return False


def normalize_country(name: str) -> str:
    """
    Нормализовать название страны.

    Пытается найти страну по русскому или английскому названию,
    а также по ISO коду (например, 'RU', 'US', 'DE').
    Если страна не найдена — возвращает оригинальное название.

    Args:
        name: Название страны на русском или английском языке.

    Returns:
        Официальное английское название страны или оригинальное название.
    """
    if not name or not name.strip():
        return name.strip()

    normalized = name.strip().lower()

    # Сначала ищем в пользовательском словаре
    user_dict = _load_user_dict()
    if normalized in user_dict:
        return user_dict[normalized]

    # Затем ищем во встроенном словаре рус->англ
    if normalized in RU_TO_EN:
        return RU_TO_EN[normalized]

    # Затем ищем через pycountry (английский, ISO коды)
    try:
        result = pycountry.countries.search_fuzzy(normalized)
        if result:
            return result[0].name  # type: ignore
    except (AttributeError, LookupError):
        pass

    return name.strip()


def normalize_countries(names: List[str]) -> Tuple[List[str], List[str]]:
    """
    Нормализовать список названий стран.

    Если название на русском языке не распознано и вернулось без изменений,
    оно считается нераспознанным и попадает в список unknown.

    Args:
        names: Список названий стран для нормализации.

    Returns:
        Кортеж из двух списков: (нормализованные, нераспознанные).
    """
    normalized = []
    unknown = []

    for name in names:
        result = normalize_country(name)
        original_stripped = name.strip()

        # Если результат совпадает с оригиналом и это кириллица — страна не распознана
        if result == original_stripped and any('\u0400' <= c <= '\u04FF' for c in original_stripped):
            unknown.append(original_stripped)
        elif result:
            normalized.append(result)
        else:
            unknown.append(original_stripped)

    return normalized, unknown
