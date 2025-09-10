import json
import unittest
from datetime import datetime
from unittest.mock import mock_open, patch

import pandas as pd
import pytest

from src.utils import (date_add_month, get_card_out, get_currency_rate, get_currency_rates, get_stock, get_stocks,
                       get_top5_tran, get_user_info, greeting, reading_operations_from_excel)


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


@pytest.fixture
def sample_data():
    return pd.DataFrame({
        "Дата операции": ["01.10.2023 10:00:00", "15.10.2023 10:00:00"],
        "Сумма платежа": [-1000, -500],
        "Номер карты": ["xxxx-xxxx-xxxx-1234", "xxxx-xxxx-xxxx-5678"],
        "Кэшбэк": [10, 5],
        "Статус": ["OK", "OK"]
    })


# =============================================================================================================

@pytest.fixture
def sample_oper_data():
    return pd.DataFrame({
        "Дата платежа": ["01.10.2023 10:00:00", "05.10.2023 15:30:00", "10.10.2023 12:00:00"],
        "Дата операции": ["01.10.2023 10:00:00", "05.10.2023 15:30:00", "10.10.2023 12:00:00"],
        "Сумма платежа": [-1000, -2000, -1500],
        "Категория": ["Food", "Electronics", "Transport"],
        "Описание": ["Groceries", "Laptop", "Taxi"]
    })


@pytest.fixture
def user_info():
    return ["USD", "EUR"]


@pytest.fixture
def user_info_stock():
    return ["AAPL", "GOOGL"]


@pytest.fixture
def currency_data():
    return [{"result": 74.0}, {"result": 85.5}]


@pytest.fixture
def stock_data():
    return [{"high": 145.3}, {"high": 2734.5}]


@pytest.mark.parametrize("test_input,expected", [
    (datetime.strptime("2023-10-30 06:30:00", "%Y-%m-%d %H:%M:%S"), "Доброе утро"),
    (datetime.strptime("2023-10-30 13:00:00", "%Y-%m-%d %H:%M:%S"), "Добрый день"),
    (datetime.strptime("2023-10-30 20:00:00", "%Y-%m-%d %H:%M:%S"), "Добрый вечер"),
    (datetime.strptime("2023-10-30 00:30:00", "%Y-%m-%d %H:%M:%S"), "Доброй ночи"),
])
def test_greeting(test_input, expected):
    assert greeting(test_input) == expected


@pytest.mark.parametrize("expected", [
    [{'cashback': '5.00', 'last_digits': 'xxx-xxxx-xxxx-5678', 'total_spent': '500.00'}]
])
def test_get_card_out(sample_data, expected):
    result = get_card_out(sample_data, "2023-10-31 23:59:59")
    assert result == expected


@pytest.mark.parametrize("expected", [
    [
        {'amount': 2000, 'category': 'Electronics', 'date': '05.10.2023 15:30:00', 'description': 'Laptop'},
        {'amount': 1500, 'category': 'Transport', 'date': '10.10.2023 12:00:00', 'description': 'Taxi'}
    ]
])
def test_get_top5_tran(sample_oper_data, expected):
    result = get_top5_tran(sample_oper_data, "2023-10-31 23:59:59")
    assert result == expected


@pytest.mark.parametrize("expected", [
    [{"currency": "USD", "rate": 74.0}, {"currency": "EUR", "rate": 85.5}]
])
@patch('src.utils.get_currency_rate')
@patch('src.utils.get_user_info')
def test_get_currency_rates(mock_get_user_info, mock_get_currency_rate, user_info, currency_data, expected):
    mock_get_user_info.return_value = user_info
    mock_get_currency_rate.side_effect = currency_data

    result = get_currency_rates()
    assert result == expected


@pytest.mark.parametrize("expected", [
    [{"stock": "AAPL", "price": 145.3}, {"stock": "GOOGL", "price": 2734.5}]
])
@patch('src.utils.get_stock')
@patch('src.utils.get_user_info')
def test_get_stocks(mock_get_user_info, mock_get_stock, user_info, stock_data, expected, user_info_stock):
    mock_get_user_info.return_value = user_info_stock
    mock_get_stock.side_effect = stock_data

    result = get_stocks()
    assert result == expected


if __name__ == "__main__":
    unittest.main()
