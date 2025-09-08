import pytest
from unittest.mock import patch
import pandas as pd
from datetime import datetime
from src.cat_web_page_main import greeting, get_card_out, get_top5_tran, get_currency_rates, get_stocks


@pytest.fixture
def sample_data():
    return pd.DataFrame({
        "Дата операции": ["01.10.2023 10:00:00", "15.10.2023 10:00:00"],
        "Сумма платежа": [-1000, -500],
        "Номер карты": ["xxxx-xxxx-xxxx-1234", "xxxx-xxxx-xxxx-5678"],
        "Кэшбэк": [10, 5],
        "Статус": ["OK", "OK"]
    })


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
@patch('src.cat_web_page_main.get_currency_rate')
@patch('src.cat_web_page_main.get_user_info')
def test_get_currency_rates(mock_get_user_info, mock_get_currency_rate, user_info, currency_data, expected):
    mock_get_user_info.return_value = user_info
    mock_get_currency_rate.side_effect = currency_data

    result = get_currency_rates()
    assert result == expected


@pytest.mark.parametrize("expected", [
    [{"stock": "AAPL", "price": 145.3}, {"stock": "GOOGL", "price": 2734.5}]
])
@patch('src.cat_web_page_main.get_stock')
@patch('src.cat_web_page_main.get_user_info')
def test_get_stocks(mock_get_user_info, mock_get_stock, user_info, stock_data, expected, user_info_stock):
    mock_get_user_info.return_value = user_info_stock
    mock_get_stock.side_effect = stock_data

    result = get_stocks()
    assert result == expected
