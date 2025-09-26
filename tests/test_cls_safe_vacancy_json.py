import json
import os

import pytest

from src.cls_safe_vacancy_json import SafeVacancyJson


def test_safe_vacancy_json_saves_data_to_file(tmp_path):
    # Подготовка
    filename = tmp_path / "vacancies.json"
    data = [
        {"id": 1, "title": "Разработчик", "company": "Компания А"},
        {"id": 2, "title": "Тестировщик", "company": "Компания Б"},
    ]

    vacancy_saver = SafeVacancyJson()

    # Вызов метода
    vacancy_saver.safe_vacancy(data, str(filename))

    # Проверка: файл создан и содержит корректный JSON
    assert os.path.exists(filename)
    with open(filename, "r", encoding="utf-8") as f:
        loaded = json.load(f)

    assert loaded == data


def test_safe_vacancy_json_saves_empty_list(tmp_path):
    filename = tmp_path / "vacancies_empty.json"
    data = []

    vacancy_saver = SafeVacancyJson()
    vacancy_saver.safe_vacancy(data, str(filename))

    assert os.path.exists(filename)
    with open(filename, "r", encoding="utf-8") as f:
        loaded = json.load(f)

    assert loaded == data


def test_safe_vacancy_json_overwrites_existing_file(tmp_path):
    filename = tmp_path / "vacancies_overwrite.json"
    initial_data = [{"id": 99, "title": "Старое", "company": "Стартап"}]
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(initial_data, f)

    new_data = [{"id": 1, "title": "Новая вакансия", "company": "Новая Компания"}]
    vacancy_saver = SafeVacancyJson()
    vacancy_saver.safe_vacancy(new_data, str(filename))

    with open(filename, "r", encoding="utf-8") as f:
        loaded = json.load(f)

    assert loaded == new_data


def test_safe_vacancy_json_invalid_path(tmp_path, monkeypatch):
    invalid_path = "/invalid_path/vacancies.json"

    vacancy_saver = SafeVacancyJson()

    with pytest.raises(Exception):
        vacancy_saver.safe_vacancy([{"id": 1}], invalid_path)
