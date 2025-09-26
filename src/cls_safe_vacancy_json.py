import json

from src.cls_base_safe_vacancy import BaseSafeVacancy


class SafeVacancyJson(BaseSafeVacancy):
    """Класс для сохранения данных о вакансиях в файл JSON"""

    def safe_vacancy(self, data: list, filename: str) -> None:
        """Метод для сохранения данных о вакансиях в файл JSON"""
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file)
