import json
import unittest

import pandas as pd

from src.services import get_profitable_cashback


class TestServices(unittest.TestCase):

    def setUp(self):
        """Этот метод будет запускаться перед каждым тестом."""
        # Создаем данные для тестирования
        self.data = pd.DataFrame({
            "Дата платежа": [
                "05.12.2021",
                "15.12.2021",
                "20.11.2021",
                "20.12.2021"
            ],
            "Категория": [
                "Food",
                "Electronics",
                "Food",
                "Transport"
            ],
            "Кэшбэк": [
                100.0,
                150.0,
                50.0,
                200.0
            ],
            "Статус": [
                "OK",
                "OK",
                "Canceled",
                "OK"
            ]
        })

        # Ожидаемый результат
        self.expected_result = {
            "Transport": 200.0,
            "Electronics": 150.0,
            "Food": 100.0
        }
        self.expected_result_json = json.dumps(self.expected_result, ensure_ascii=False, indent=2)

    def test_get_profitable_cashback(self):
        """Тестируем функцию get_profitable_cashback."""
        # Вызов тестируемой функции
        result = get_profitable_cashback(self.data, year_par="2021", month_par="12")

        # Проверка результата
        self.assertEqual(result, self.expected_result_json)


if __name__ == "__main__":
    unittest.main()
