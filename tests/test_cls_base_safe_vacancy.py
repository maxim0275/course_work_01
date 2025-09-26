import unittest
import json
import os
from abc import abstractmethod, ABC


# Предположим, что базовый абстрактный класс уже определен, как указано:
class BaseSafeVacancy(ABC):
    """ Абстрактный класс для сохранения данных о вакансиях в файл """

    @abstractmethod
    def safe_vacancy(self, data: list, filename: str) -> None:
        """ Метод для сохранения данных о вакансиях в файл """
        pass


# Реализация конкретного класса для тестирования
class SafeVacancy(BaseSafeVacancy):
    def safe_vacancy(self, data: list, filename: str) -> None:
        with open(filename, 'w') as file:
            json.dump(data, file)


class TestSafeVacancy(unittest.TestCase):
    def setUp(self):
        self.test_filename = 'test_vacancies.json'
        self.vacancy_data = [
            {"title": "Developer", "company": "TechCorp"},
            {"title": "Designer", "company": "DesignStudio"},
        ]
        self.vacancy_saver = SafeVacancy()

    def test_safe_vacancy(self):
        """ Проверка корректности сохранения вакансий в файл """
        self.vacancy_saver.safe_vacancy(self.vacancy_data, self.test_filename)

        # Проверим, что файл создан и содержит корректные данные
        self.assertTrue(os.path.exists(self.test_filename))

        with open(self.test_filename, 'r') as file:
            loaded_data = json.load(file)

        self.assertEqual(loaded_data, self.vacancy_data)

    def tearDown(self):
        """ Удаляем тестовый файл после теста """
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)


if __name__ == '__main__':
    unittest.main()
