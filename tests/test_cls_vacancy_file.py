import unittest
import json
import os

from src.cls_vacancy_file import VacancyFile


class TestVacancyFile(unittest.TestCase):

    def setUp(self):
        """ Метод, который выполняется перед каждым тестом """
        self.filename = 'test_vacancies.json'
        self.vacancy_file = VacancyFile(self.filename)

        # Начальные данные для заполнения файла
        self.sample_data = [
            {"title": "Разработчик Python", "salr_from": 100000, "area_name": "Москва"},
            {"title": "Frontend Developer", "salr_from": 80000, "area_name": "Санкт-Петербург"}
        ]

        # Создаем файл с начальными данными
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(self.sample_data, file)

    def tearDown(self):
        """ Метод, который выполняется после каждого теста """
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_add_vacancy_tofile(self):
        """ Тестирование метода добавления вакансий в файл """
        new_data = [
            {"title": "Системный администратор", "salr_from": 90000, "area_name": "Москва"},
            {"title": "Разработчик Python", "salr_from": 100000, "area_name": "Москва"}  # Дубликат
        ]

        self.vacancy_file.add_vacancy_tofile(new_data)

        with open(self.filename, "r", encoding="utf-8") as file:
            result_data = json.load(file)

            # Проверяем, что файл содержит ожидаемые данные без дубликатов
            self.assertEqual(len(result_data), 3)
            self.assertIn(new_data[0], result_data)

    def test_get_vacacny_fromfile(self):
        """ Тестирование метода получения вакансий """
        # Получение вакансий с параметрами фильтрации
        filtered_data = self.vacancy_file.get_vacacny_fromfile(salary_mask=90000, area_name_mask="Москва")
        self.assertEqual(len(filtered_data), 1)  # Должен вернуться только один элемент
        self.assertEqual(filtered_data[0]["title"], "Разработчик Python")

        # Получение вакансий без фильтров
        all_data = self.vacancy_file.get_vacacny_fromfile()
        self.assertEqual(len(all_data), len(self.sample_data))

    def test_del_vacancy_fromfile(self):
        """ Тестирование метода удаления вакансий из файла """
        self.vacancy_file.del_vacancy_fromfile()

        with open(self.filename, "r", encoding="utf-8") as file:
            result_data = json.load(file)

            # Проверяем, что файл стал пустым (или равен None)
            self.assertIsNone(result_data)

if __name__ == '__main__':
    unittest.main()