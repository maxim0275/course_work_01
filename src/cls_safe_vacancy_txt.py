from src.cls_base_safe_vacancy import BaseSafeVacancy


class SafeVacancyTxt(BaseSafeVacancy):
    """Класс для сохранения данных о вакансиях в файл TXT"""

    def safe_vacancy(self, data: list, filename: str) -> None:
        """Метод для сохранения данных о вакансиях в файл TXT"""
        """ В текстовый файл построчно сохраняютмя текстовые представления вакансий"""
        with open(filename, "w", encoding="utf-8") as file:
            for vac in data:
                file.write(str(vac) + "\n")
