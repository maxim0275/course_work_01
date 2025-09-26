from abc import ABC, abstractmethod

import requests


class GetVacAPI(ABC):
    """Абстрактный класс для получения вакансий с сайта с помощью API"""

    @abstractmethod
    def _connect_to_api(self, params=None) -> requests.models.Response:
        pass

    @abstractmethod
    def get_vacancies(self, key_word: str = None) -> None:
        """Метод для получения вакансий с сайта с помощью API"""
        pass

    @abstractmethod
    def answer(self):
        pass
