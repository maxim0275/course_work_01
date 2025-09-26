import json

from src.cls_base_vacancy_file import BaseVacancyFile


class VacancyFile(BaseVacancyFile):
    """ Класс для работы с файлом.
    """
    vacancy_data = None

    def __init__(self, filename: str) -> None:
        self._filename = filename if filename else "data/vac_default.json"

    def get_vacacny_fromfile(self, salary_mask: int = None, area_name_mask: str = None) -> list:
        """ Загрузить вакансии из файла, если указаны параметры, то применить фильтр """

        # открыть файл и считать данные в список
        with open(self._filename) as file:
            loaded_data = json.load(file)

        # возвратить отфильтрованные вакансии
        if salary_mask and area_name_mask:
            return list(
                filter(lambda x: area_name_mask.lower() in x['area_name'].lower() and x['salr_from'] > salary_mask,
                       loaded_data))
        elif salary_mask and area_name_mask is None:
            return list(
                filter(lambda x: x['salr_from'] > salary_mask, loaded_data))
        elif salary_mask is None and area_name_mask:
            return list(
                filter(lambda x: area_name_mask.lower() in x['area_name'].lower(), loaded_data))

        else:
            return list(
                filter(lambda x: x, loaded_data))

    def add_vacancy_tofile(self, data_to_add: list) -> None:
        """ добавить вакансии в файл"""

        with open(self._filename) as file:
            loaded_data = json.load(file)

        loaded_data.extend(data_to_add)

        # Файл не сохраняет дубли вакансий
        loaded_data = [dict(t) for t in {frozenset(d.items()) for d in loaded_data}]

        with open(self._filename, "w", encoding="utf-8") as file:
            json.dump(loaded_data, file)

    def del_vacancy_fromfile(self) -> None:
        """ Удалить вакансии из файла"""
        with open(self._filename, "w", encoding="utf-8") as file:
            json.dump(None, file)
