import os
import unittest

from src.cls_safe_vacancy_excel import SafeVacancyExcel


class TestSafeVacancyExcel(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.filename = "../data/vacancy_xls.xlsx"
        cls.safe_vacancy_excel = SafeVacancyExcel()

    def setUp(self):
        # Создадим данные для  тестирования
        self.test_data = [
            {"title": "Vacancy 1", "company": "Company A", "salary": 100000},
            {"title": "Vacancy 2", "company": "Company B", "salary": 120000},
        ]

    def test_safe_vacancy_creates_file(self):
        # Запуск метода сохранения вакансий
        self.safe_vacancy_excel.safe_vacancy(self.test_data, self.filename)

        # Проверяем, что файл создан
        self.assertTrue(os.path.exists(self.filename), "Файл не был создан")

    def test_safe_vacancy_correct_data(self):
        # Запуск метода сохранения вакансий
        self.safe_vacancy_excel.safe_vacancy(self.test_data, self.filename)

        # Чтение содержимого файла для проверки
        import pandas as pd

        df = pd.read_excel(self.filename)
        # Проверяем количество строк и столбцов
        self.assertEqual(len(df), len(self.test_data), "Некорректное количество строк в файле")
        self.assertEqual(len(df.columns), len(self.test_data[0]), "Некорректное количество столбцов в файле")

        # Проверяем, что данные соответствуют исходным
        for index, entry in enumerate(self.test_data):
            for key, value in entry.items():
                self.assertEqual(df.at[index, key], value, f"Некорректные данные для строки {index}, столбца {key}")

    @classmethod
    def tearDownClass(cls):
        # Удаляем файл после тестов
        if os.path.exists(cls.filename):
            os.remove(cls.filename)


if __name__ == "__main__":
    unittest.main()
