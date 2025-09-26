import os

from src.cls_safe_vacancy_txt import SafeVacancyTxt


def test_safe_vacancy_txt_writes_lines(tmp_path):
    # Подготовка
    data = [
        {"id": 1, "title": "Python разработчик", "company": "ООО Ромашка"},
        {"id": 2, "title": "Инженер по тестированию", "company": "АО Альфа"},
        "Простая строка вакансии",
    ]

    # Преобразуем данные в строковое представление, чтобы проверить точный вывод
    expected_lines = [str(vac) for vac in data]

    # Путь к файлу во временной директории
    tmp_file = tmp_path / "vacancies.txt"

    # Вызов метода
    vac_txt = SafeVacancyTxt()
    vac_txt.safe_vacancy(data, str(tmp_file))

    # Проверка существования и содержания файла
    assert os.path.exists(tmp_file)

    with open(tmp_file, "r", encoding="utf-8") as f:
        lines = [line.rstrip("\n") for line in f]

    assert lines == expected_lines
