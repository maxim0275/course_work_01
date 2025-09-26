from abc import ABC, abstractmethod


class BaseSafeVacancy(ABC):
    """Абстрактный класс для сохранения данных о вакансиях в файл"""

    @abstractmethod
    def safe_vacancy(self, data: list, filename: str) -> None:
        """Метод для сохранения данных о вакансиях в файл"""
        pass
