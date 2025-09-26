import unittest

from src.cls_vacancy import HHVacancy


class TestHHVacancy(unittest.TestCase):

    def setUp(self):
        """Метод, который выполняется перед каждым тестом"""
        self.valid_vacancy = HHVacancy("1", "Разработчик Python", "Москва", 100000, 150000)
        self.valid_vacancy_min = HHVacancy("2", "Системный администратор", "СПБ", 80000, 0)
        self.invalid_vacancy_id = "abc"
        self.invalid_vacancy_name = "Код."

    def test_initialization_valid(self):
        """Тестирование корректной инициализации вакансии"""
        self.assertEqual(self.valid_vacancy.vacancy_id, "1")
        self.assertEqual(self.valid_vacancy.name, "Разработчик Python")
        self.assertEqual(self.valid_vacancy.area_name, "Москва")
        self.assertEqual(self.valid_vacancy.salary, 125000)

    def test_invalid_vacancy_id(self):
        """Тестирование некорректного идентификатора вакансии"""
        with self.assertRaises(ValueError):
            HHVacancy(self.invalid_vacancy_id, "Вакансия", "Москва", 100000, 150000)

    def test_invalid_vacancy_name(self):
        """Тестирование некорректного имени вакансии"""
        vacancy = HHVacancy("3", self.invalid_vacancy_name, "Москва", 100000, 150000)
        self.assertEqual(vacancy.name, "Не указано")

    def test_area_name_too_short(self):
        """Тестирование слишком короткого названия области"""
        vacancy = HHVacancy("4", "Вакансия", "М", 100000, 150000)
        self.assertEqual(vacancy.area_name, "Не указано")

    def test_salary_calculation(self):
        """Тестирование вычисления зарплаты"""
        vacancy = HHVacancy("5", "Тестировщик", "Москва", 60000, 90000)
        self.assertEqual(vacancy.salary, 75000)

        vacancy_min = HHVacancy("6", "UI/UX Дизайнер", "Москва", 0, 65000)
        self.assertEqual(vacancy_min.salary, 65000 / 2)

        vacancy_with_no_salary = HHVacancy("7", "Менеджер", "Москва", 0, 0)
        self.assertEqual(vacancy_with_no_salary.salary, 0)

    def test_comparison_methods(self):
        """Тестирование методов сравнения"""
        vacancy = HHVacancy("8", "Веб-разработчик", "Москва", 90000, 120000)
        self.assertTrue(vacancy < self.valid_vacancy)
        self.assertTrue(self.valid_vacancy > vacancy)
        self.assertTrue(self.valid_vacancy >= self.valid_vacancy)
        self.assertTrue(vacancy <= self.valid_vacancy)

    def test_repr(self):
        """Тестирование метода __repr__"""
        expected_repr = "Идентификатор=1, Вакансия=Разработчик Python, Место=Москва, Зарплата=125000.0"
        self.assertEqual(repr(self.valid_vacancy), expected_repr)


if __name__ == "__main__":
    unittest.main()
