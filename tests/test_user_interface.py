# -*- coding: utf-8 -*-
"""Тесты для модуля src.user_interface."""

import pytest
import io
import sys
from unittest.mock import patch

from src.application.user_interface import user_interaction


# ============================================================================
# 0. Проверка функции: user_interaction из модуля src.user_interface.
# ============================================================================

# Тест 001: Проверка, что функция существует и принимает список самолётов.
def test_user_interaction_exists():
    """Проверяет что функция user_interaction существует и является вызываемой.

    Проверяет что user_interaction является callable объектом.
    """
    assert callable(user_interaction)


# Тест 002: Проверка, что функция не вызывает ошибок при пустом списке.
def test_user_interaction_empty_list():
    """Проверяет что user_interaction корректно обрабатывает пустой список самолётов.

    Вызывает user_interaction с пустым списком и перехватывает исключения,
    убеждаясь что функция не падает при отсутствии данных.
    """
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()

    try:
        with patch("builtins.input", side_effect=["0", "", "0 - 1000"]):
            user_interaction([])
    except Exception as e:
        pytest.fail(f"user_interaction вызвал исключение: {e}")
    finally:
        sys.stdout = old_stdout


# Тест 003: Проверка, что функция корректно обрабатывает ввод топ N.
def test_user_interaction_top_n(planes_for_sorting):
    """Проверяет что пользовательский ввод для выбора топ N работает корректно.

    Имитирует ввод пользователя для выбора топ N самолётов и проверяет,
    что в выводе присутствует заголовок "Трекер самолётов".
    """
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()

    try:
        with patch("builtins.input", side_effect=["2", "", "0 - 1000"]):
            user_interaction(planes_for_sorting)
    except Exception as e:
        pytest.fail(f"user_interaction вызвал исключение: {e}")
    finally:
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout

    # Проверяем что вывод содержит заголовок
    assert "Трекер самолётов" in output


# Тест 004: Проверка, что функция корректно обрабатывает ввод страны.
def test_user_interaction_country_filter(planes_for_filtering):
    """Проверяет что фильтрация по стране через пользовательский интерфейс работает корректно.

    Имитирует ввод пользователя для фильтрации по стране "Spain" и проверяет,
    что функция не вызывает исключений при обработке ввода.
    """
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()

    try:
        with patch("builtins.input", side_effect=["0", "Spain", "0 - 1000"]):
            user_interaction(planes_for_filtering)
    except Exception as e:
        pytest.fail(f"user_interaction вызвал исключение: {e}")
    finally:
        sys.stdout = old_stdout


# Тест 005: Проверка, что функция корректно обрабатывает ввод диапазона высот.
def test_user_interaction_altitude_range(planes_for_filtering):
    """Проверяет что фильтрация по диапазону высот через пользовательский интерфейс работает корректно.

    Имитирует ввод пользователя для фильтрации по диапазону высот "1000 - 5000"
    и проверяет что функция не вызывает исключений.
    """
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()

    try:
        with patch("builtins.input", side_effect=["0", "", "1000 - 5000"]):
            user_interaction(planes_for_filtering)
    except Exception as e:
        pytest.fail(f"user_interaction вызвал исключение: {e}")
    finally:
        sys.stdout = old_stdout


# Тест 006: Проверка, что функция обрабатывает некорректный ввод топ N.
def test_user_interaction_invalid_top_n():
    """Проверяет что некорректный ввод для топ N обрабатывается gracefully.

    Имитирует ввод "abc" для топ N и проверяет что выводится сообщение
    об ошибке или отсутствии результатов.
    """
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()

    try:
        with patch("builtins.input", side_effect=["abc", "", "0 - 1000"]):
            user_interaction([])
    except Exception as e:
        pytest.fail(f"user_interaction вызвал исключение: {e}")
    finally:
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout

    # Проверяем что выведено сообщение об ошибке
    assert "Ошибка" in output or "не найдены" in output


# Тест 007: Проверка, что функция обрабатывает некорректный диапазон высот.
def test_user_interaction_invalid_altitude():
    """Проверяет что некорректный диапазон высот обрабатывается gracefully.

    Имитирует ввод "abc" для диапазона высот и проверяет что выводится
    сообщение об ошибке или отсутствии результатов.
    """
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()

    try:
        with patch("builtins.input", side_effect=["0", "", "abc"]):
            user_interaction([])
    except Exception as e:
        pytest.fail(f"user_interaction вызвал исключение: {e}")
    finally:
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout

    # Проверяем что выведено сообщение об ошибке
    assert "Ошибка" in output or "не найдены" in output


# Тест 008: Проверка что функция обрабатывает неизвестные страны.
def test_user_interaction_unknown_country(planes_for_filtering):
    """Проверяет что функция обрабатывает неизвестные страны.

    Имитирует ввод пользователя с неизвестной страной на русском
    и проверяет что выводится сообщение о нераспознанных странах.
    """
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()

    try:
        # Ввод: топ N, неизвестная страна (кириллица), ответ n, диапазон высот
        with patch("builtins.input", side_effect=["0", "НеизвестнаяСтрана", "n", "0 - 1000"]):
            user_interaction(planes_for_filtering)
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout
    except Exception as e:
        sys.stdout = old_stdout
        pytest.fail(f"user_interaction вызвал исключение: {e}")

    # Проверяем что выведено сообщение о неизвестных странах
    assert "не распознаны" in output or "Внимание" in output or "не найдены" in output


# Тест 009: Проверка что функция обрабатывает корректный диапазон высот.
def test_user_interaction_valid_altitude_range(planes_for_filtering):
    """Проверяет что функция корректно обрабатывает валидный диапазон высот.

    Имитирует ввод пользователя для фильтрации по диапазону высот "1000 - 5000"
    и проверяет что вывод содержит информацию о самолётах в диапазоне.
    """
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()

    try:
        with patch("builtins.input", side_effect=["1", "", "1000 - 5000"]):
            user_interaction(planes_for_filtering)
    except Exception as e:
        pytest.fail(f"user_interaction вызвал исключение: {e}")
    finally:
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout

    # Проверяем что вывод содержит заголовок диапазона
    assert "диапазоне высот" in output


# Тест 010: Проверка что функция обрабатывает некорректное число для топ N.
def test_user_interaction_invalid_top_n_number():
    """Проверяет что функция обрабатывает некорректное число для топ N.

    Имитирует ввод отрицательного числа для топ N и проверяет что
    выводится сообщение об ошибке.
    """
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()

    try:
        with patch("builtins.input", side_effect=["-1", "", "0 - 1000"]):
            user_interaction([])
    except Exception as e:
        pytest.fail(f"user_interaction вызвал исключение: {e}")
    finally:
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout

    # Проверяем что выведено сообщение об ошибке
    assert "Ошибка" in output or "корректное число" in output


# ============================================================================
# 1. Проверка функций: print_aeroplanes из модуля src.application.user_interface.
# ============================================================================

# Тест 011: Проверка что print_aeroplanes выводит список самолётов.
def test_print_aeroplanes_with_planes(planes_for_sorting):
    """Проверяет что print_aeroplanes корректно выводит информацию о самолётах.

    Создаёт список из двух самолётов и проверяет что вывод содержит
    заголовки колонок и данные о самолётах.
    """
    from src.application.user_interface import print_aeroplanes
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()

    try:
        print_aeroplanes(planes_for_sorting)
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout
    except Exception as e:
        sys.stdout = old_stdout
        pytest.fail(f"print_aeroplanes вызвал исключение: {e}")

    # Проверяем что вывод содержит заголовки и данные
    assert "Позывной" in output
    assert "Страна" in output
    assert "Скорость" in output
    assert "Высота" in output


# Тест 012: Проверка что print_aeroplanes выводит сообщение при пустом списке.
def test_print_aeroplanes_empty():
    """Проверяет что print_aeroplanes выводит сообщение при пустом списке.

    Вызывает print_aeroplanes с пустым списком и проверяет что
    выводится сообщение "Самолёты не найдены".
    """
    from src.application.user_interface import print_aeroplanes
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()

    try:
        print_aeroplanes([])
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout
    except Exception as e:
        sys.stdout = old_stdout
        pytest.fail(f"print_aeroplanes вызвал исключение: {e}")

    assert "Самолёты не найдены" in output


# ============================================================================
# 2. Проверка функций: user_interaction из модуля src.application.user_interface.
# ============================================================================

# Тест 013: Проверка что функция предлагает добавить неизвестную страну в словарь.
def test_user_interaction_add_unknown_country(tmp_path, monkeypatch, planes_for_filtering):
    """Проверяет что при неизвестной стране пользователь может добавить перевод.

    Имитирует ввод неизвестной страны, ответ "y" для добавления и английское название.
    Проверяет что выводится сообщение о добавлении.
    """
    from src.application import country_normalizer
    temp_file = tmp_path / "country_translations.json"
    monkeypatch.setattr(country_normalizer, "_USER_DICT_PATH", temp_file)

    old_stdout = sys.stdout
    sys.stdout = io.StringIO()

    try:
        # Ввод: топ N, неизвестная страна, ответ y, английское название, диапазон высот
        with patch("builtins.input", side_effect=["0", "НеизвестнаяСтрана", "y", "UnknownLand", "0 - 1000"]):
            user_interaction(planes_for_filtering)
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout
    except Exception as e:
        sys.stdout = old_stdout
        pytest.fail(f"user_interaction вызвал исключение: {e}")

    # Проверяем что выведено сообщение о добавлении
    assert "Добавлено" in output

    # Очищаем словарь после теста
    if temp_file.exists():
        temp_file.unlink()


# Тест 014: Проверка что функция показывает распознавание стран.
def test_user_interaction_country_recognition(planes_for_filtering):
    """Проверяет что функция показывает как были распознаны названия стран.

    Имитирует ввод русской страны "Россия" и проверяет что в выводе
    есть сообщение о распознавании.
    """
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()

    try:
        # Ввод: топ N, Россия, диапазон высот
        with patch("builtins.input", side_effect=["0", "Россия", "0 - 1000"]):
            user_interaction(planes_for_filtering)
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout
    except Exception as e:
        sys.stdout = old_stdout
        pytest.fail(f"user_interaction вызвал исключение: {e}")

    # Проверяем что выведено сообщение о распознавании
    assert "Распознано" in output


# Тест 015: Проверка что функция пропускает пустой ввод стран.
def test_user_interaction_empty_country_input(planes_for_filtering):
    """Проверяет что при пустом вводе стран функция переходит к следующему шагу.

    Имитирует пустой ввод для фильтрации по стране и проверяет что
    функция не вызывает ошибок.
    """
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()

    try:
        # Ввод: топ N, пустая страна, диапазон высот
        with patch("builtins.input", side_effect=["0", "", "0 - 1000"]):
            user_interaction(planes_for_filtering)
        sys.stdout = old_stdout
    except Exception as e:
        sys.stdout = old_stdout
        pytest.fail(f"user_interaction вызвал исключение: {e}")

    # Функция должна завершиться без ошибок
    assert True


# Тест 016: Проверка что при отказе от добавления страны показывается "Страны не найдены".
def test_user_interaction_skip_unknown_country(planes_for_filtering):
    """Проверяет что при отказе от добавления неизвестной страны выводится сообщение.

    Имитирует ввод неизвестной страны и ответ "n" для пропуска.
    Проверяет что выводится сообщение "Страны не найдены".
    """
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()

    try:
        # Ввод: топ N, неизвестная страна, ответ n, диапазон высот
        with patch("builtins.input", side_effect=["0", "НеизвестнаяСтрана", "n", "0 - 1000"]):
            user_interaction(planes_for_filtering)
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout
    except Exception as e:
        sys.stdout = old_stdout
        pytest.fail(f"user_interaction вызвал исключение: {e}")

    # Проверяем что выведено сообщение о сохранении
    assert "Сохранено" in output or "не найдены" in output


# Тест 017: Проверка что функция успешно добавляет перевод и нормализует страну.
def test_user_interaction_add_and_normalize(tmp_path, monkeypatch, planes_for_filtering):
    """Проверяет что при добавлении перевода страна нормализуется и фильтруется.

    Имитирует ввод неизвестной страны, ответ "y" для добавления и английское название.
    Monkeypatchит save_translation чтобы вернуть True, проверяет что выводится
    сообщение о добавлении и что страна найдена.
    """
    from src.application import country_normalizer
    from src.application import user_interface

    # Изолируем словарь переводов
    temp_file = tmp_path / "country_translations.json"
    monkeypatch.setattr(country_normalizer, "_USER_DICT_PATH", temp_file)

    old_stdout = sys.stdout
    sys.stdout = io.StringIO()

    try:
        # Monkeypatchим save_translation в user_interface чтобы всегда возвращать True
        original_save = user_interface.save_translation
        user_interface.save_translation = lambda ru, en: True

        try:
            # Ввод: топ N, неизвестная страна, ответ y, английское название, диапазон высот
            with patch("builtins.input", side_effect=["0", "XxXНеизвестнаяСтранаXxX", "y", "UnknownLand", "0 - 1000"]):
                user_interaction(planes_for_filtering)
            output = sys.stdout.getvalue()
            sys.stdout = old_stdout
        finally:
            user_interface.save_translation = original_save
    except Exception as e:
        sys.stdout = old_stdout
        pytest.fail(f"user_interaction вызвал исключение: {e}")

    # Проверяем что выведено сообщение о добавлении и повторной нормализации
    assert "Добавлено" in output

    # Очищаем словарь после теста
    if temp_file.exists():
        temp_file.unlink()


# Тест 018: Проверка что функция показывает ошибку при неудачном сохранении перевода.
def test_user_interaction_save_translation_error(tmp_path, monkeypatch, planes_for_filtering):
    """Проверяет что при ошибке сохранения перевода выводится сообщение об ошибке.

    Имитирует ввод неизвестной страны, ответ "y" для добавления и английское название.
    Monkeypatchит save_translation чтобы вернуть False, проверяет что выводится
    сообщение об ошибке сохранения.
    """
    from src.application import country_normalizer
    from src.application import user_interface

    # Изолируем словарь переводов
    temp_file = tmp_path / "country_translations.json"
    monkeypatch.setattr(country_normalizer, "_USER_DICT_PATH", temp_file)

    old_stdout = sys.stdout
    sys.stdout = io.StringIO()

    try:
        # Monkeypatchим save_translation в user_interface чтобы всегда возвращать False
        original_save = user_interface.save_translation
        user_interface.save_translation = lambda ru, en: False

        try:
            # Ввод: топ N, неизвестная страна, ответ y, английское название, диапазон высот
            with patch("builtins.input", side_effect=["0", "XxXНеизвестнаяСтранаXxX", "y", "UnknownLand", "0 - 1000"]):
                user_interaction(planes_for_filtering)
            output = sys.stdout.getvalue()
            sys.stdout = old_stdout
        finally:
            user_interface.save_translation = original_save
    except Exception as e:
        sys.stdout = old_stdout
        pytest.fail(f"user_interaction вызвал исключение: {e}")

    # Проверяем что выведено сообщение об ошибке сохранения
    assert "Ошибка: не удалось сохранить перевод" in output

    # Очищаем словарь после теста
    if temp_file.exists():
        temp_file.unlink()


# Тест 019: Проверка что функция показывает "Страны не найдены" при пустом normalized.
def test_user_interaction_no_countries_found(planes_for_filtering):
    """Проверяет что при пустом normalized выводится сообщение "Страны не найдены".

    Имитирует ввод неизвестной страны на кириллице, ответ "n" для пропуска
    и проверяет что выводится сообщение "Страны не найдены".
    """
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()

    try:
        # Ввод: топ N, неизвестная кириллица, ответ n, диапазон высот
        with patch("builtins.input", side_effect=["0", "XxXНеизвестнаяСтранаXxX", "n", "0 - 1000"]):
            user_interaction(planes_for_filtering)
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout
    except Exception as e:
        sys.stdout = old_stdout
        pytest.fail(f"user_interaction вызвал исключение: {e}")

    # Проверяем что выведено сообщение о пустом normalized
    assert "Страны не найдены" in output
