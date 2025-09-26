from abc import ABC, abstractmethod


class BaseVacancyFile(ABC):
    """Абстрактный класс для манипуояций с вакансиями"""

    @abstractmethod
    def add_vacancy_tofile(self, data_to_add: list) -> None:
        """Метод записи вакансий в файл"""
        pass

    @abstractmethod
    def get_vacacny_fromfile(self, salary: int, area_name_mask: str) -> None:
        """Метод чтения вакансий из файла"""
        pass

    @abstractmethod
    def del_vacancy_fromfile(self) -> None:
        """Метод удаления вакансий из файла"""
        pass
