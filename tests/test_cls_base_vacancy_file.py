import json
import os
import unittest

from src.cls_safe_vacancy_json import SafeVacancyJson


class TestSafeVacancyJson(unittest.TestCase):

    def setUp(self):
        """Метод, который выполняется перед каждым тестом"""
        self.vacancy_data = [
            {"title": "Разработчик Python", "salary": 100000, "area": "Москва"},
            {"title": "Frontend Developer", "salary": 80000, "area": "Санкт-Петербург"},
        ]
        self.filename = "test_vacancies.json"
        self.safe_vacancy = SafeVacancyJson()

    def tearDown(self):
        """Метод, который выполняется после каждого теста"""
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_safe_vacancy(self):
        """Тестирование метода safe_vacancy"""
        self.safe_vacancy.safe_vacancy(self.vacancy_data, self.filename)

        # Проверяем, что файл  создан
        self.assertTrue(os.path.exists(self.filename))

        # Проверяем содержимое  файла
        with open(self.filename, "r", encoding="utf-8") as file:
            data = json.load(file)
            self.assertEqual(data, self.vacancy_data)


if __name__ == "__main__":
    unittest.main()
