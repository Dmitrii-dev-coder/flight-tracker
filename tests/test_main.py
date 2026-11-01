# -*- coding: utf-8 -*-
"""Тесты для модуля main (точка входа программы)."""

import json
import pytest


# ============================================================================
# 0. Проверка функции: _handle_unknown_country из модуля main.
# ============================================================================

# Тест 001: Проверка что модуль main импортируется.
def test_main_module_importable():
    """Проверка что модуль main существует и импортируется."""
    import main
    assert hasattr(main, 'main')
    assert hasattr(main, '_handle_unknown_country')


# Тест 002: Проверка что _handle_unknown_country предлагает добавить страну.
def test_handle_unknown_country_adds_translation(tmp_path, monkeypatch):
    """Проверка что при ответе 'y' страна добавляется в словарь."""
    from main import _handle_unknown_country
    
    # Подменяем путь к JSON-файлу
    temp_file = tmp_path / "country_translations.json"
    from src.application import country_normalizer
    monkeypatch.setattr(country_normalizer, "_USER_DICT_PATH", temp_file)
    
    # Имитируем ввод: 'y' затем 'TestCountry'
    inputs = iter(['y', 'TestCountry'])
    monkeypatch.setattr('builtins.input', lambda msg: next(inputs))
    
    result = _handle_unknown_country("ТестоваяСтрана")
    
    assert result is True
    assert temp_file.exists()
    data = json.load(open(temp_file, "r", encoding="utf-8"))
    assert "тестоваястрана" in data
    assert data["тестоваястрана"] == "TestCountry"


# Тест 003: Проверка что при ответе 'n' функция возвращает False.
def test_handle_unknown_country_skips(tmp_path, monkeypatch):
    """Проверка что при ответе 'n' функция возвращает False и не создаёт файл."""
    from main import _handle_unknown_country
    
    temp_file = tmp_path / "country_translations.json"
    from src.application import country_normalizer
    monkeypatch.setattr(country_normalizer, "_USER_DICT_PATH", temp_file)
    
    # Имитируем ввод: 'n'
    monkeypatch.setattr('builtins.input', lambda msg: 'n')
    
    result = _handle_unknown_country("ПропускаемаяСтрана")
    
    assert result is False
    assert not temp_file.exists()


# Тест 004: Проверка что пустой английский ввод приводит к пропуску.
def test_handle_unknown_country_empty_english(tmp_path, monkeypatch):
    """Проверка что пустой английский название приводит к пропуску."""
    from main import _handle_unknown_country
    
    temp_file = tmp_path / "country_translations.json"
    from src.application import country_normalizer
    monkeypatch.setattr(country_normalizer, "_USER_DICT_PATH", temp_file)
    
    # Имитируем ввод: 'y' затем пустая строка
    inputs = iter(['y', ''])
    monkeypatch.setattr('builtins.input', lambda msg: next(inputs))
    
    result = _handle_unknown_country("ПустаяСтрана")
    
    assert result is False
    assert not temp_file.exists()
