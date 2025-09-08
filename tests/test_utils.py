import unittest
from unittest.mock import patch, mock_open
import json
import pandas as pd

from src.utils import get_user_info, reading_operations_from_excel, get_stock, get_currency_rate, date_add_month


class TestUtils(unittest.TestCase):

    def setUp(self):
        """Этот метод запускается перед выполнением каждого теста."""
        # Подготовка общих данных для тестов
        self.mock_file_data = json.dumps({
            "filename_opers_data": "operations.xlsx",
            "user_stocks": ["AAPL", "GOOGL"],
            "user_currencies": ["USD", "EUR"]
        })

        self.excel_data = pd.DataFrame({'Column1': [1, 2], 'Column2': [3, 4]})

        self.mock_stock_response = {'symbol': 'AAPL', 'close': 150}
        self.mock_currency_response = {'success': True, 'result': 75.0}

        self.date_src = pd.to_datetime("2023-01-15")
        self.expected_date_add_month = pd.to_datetime("2023-02-14")

    @patch('builtins.open', new_callable=mock_open, read_data=None)
    def test_get_user_info(self, mock_file):
        mock_file.return_value.read.return_value = self.mock_file_data
        # Тестируем получение имени файла
        self.assertEqual(get_user_info(1), "operations.xlsx")
        self.assertEqual(get_user_info(2), ["AAPL", "GOOGL"])
        self.assertEqual(get_user_info(3), ["USD", "EUR"])

    @patch('os.path.isfile')
    @patch('pandas.read_excel')
    def test_reading_operations_from_excel(self, mock_read_excel, mock_isfile):
        # Тестируем успешное чтение файла
        mock_isfile.return_value = True
        mock_read_excel.return_value = self.excel_data

        df = reading_operations_from_excel("dummy_path.xlsx")
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(df.shape, (2, 2))

    @patch('src.utils.request')
    def test_get_stock(self, mock_request):
        # Тестируем получение цены акции
        mock_request.return_value.status_code = 200
        mock_request.return_value.json.return_value = self.mock_stock_response

        result = get_stock("AAPL")
        self.assertEqual(result['symbol'], 'AAPL')
        self.assertEqual(result['close'], 150)

    @patch('src.utils.request')
    def test_get_currency_rate(self, mock_request):
        # Настраиваем мокаемый ответ API
        mock_request.return_value.status_code = 200
        mock_request.return_value.json.return_value = self.mock_currency_response

        # Вызываем тестируемую функцию
        result = get_currency_rate("USD")

        # Проверяем, что функция возвращает моканные данные
        self.assertTrue(result['success'])
        self.assertEqual(result['result'], 75.0)

    def test_date_add_month(self):
        # Тестируем добавление месяца к дате
        result = date_add_month(self.date_src)
        self.assertEqual(result, self.expected_date_add_month)


if __name__ == "__main__":
    unittest.main()