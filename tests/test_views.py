import json
from unittest.mock import patch

import pytest

from src.views import get_cat_report_spending_by_category, get_cat_services_profitable_cashback, get_cat_web_page_main


# Фикстура для даты операции
@pytest.fixture
def transaction_date():
    return "2021-12-31 23:00:00"


@pytest.mark.parametrize(
    "mock_operations_data, mock_greeting_result, mock_card_out, "
    "mock_top_transactions, mock_currency_rates, mock_stock_prices",
    [
        (
            [{"operation": "transaction details"}],
            "Hello, User!",
            "Cards Out Data",
            "Top 5 Transactions",
            "Currency Rates",
            "Stock Prices",
        ),
    ],
)
@patch("src.views.reading_operations_from_excel")
@patch("src.views.greeting")
@patch("src.views.get_card_out")
@patch("src.views.get_top5_tran")
@patch("src.views.get_currency_rates")
@patch("src.views.get_stocks")
def test_get_cat_web_page_main(
    mock_get_stocks,
    mock_get_currency_rates,
    mock_get_top5_tran,
    mock_get_card_out,
    mock_greeting,
    mock_reading_operations,
    mock_operations_data,
    mock_greeting_result,
    mock_card_out,
    mock_top_transactions,
    mock_currency_rates,
    mock_stock_prices,
    transaction_date,
):
    mock_reading_operations.return_value = mock_operations_data
    mock_greeting.return_value = mock_greeting_result
    mock_get_card_out.return_value = mock_card_out
    mock_get_top5_tran.return_value = mock_top_transactions
    mock_get_currency_rates.return_value = mock_currency_rates
    mock_get_stocks.return_value = mock_stock_prices

    result = get_cat_web_page_main(transaction_date)
    result_data = json.loads(result)

    assert result_data["greeting"] == mock_greeting_result
    assert result_data["cards"] == mock_card_out
    assert result_data["top_transactions"] == mock_top_transactions
    assert result_data["currency_rates"] == mock_currency_rates
    assert result_data["stock_prices"] == mock_stock_prices


@pytest.mark.parametrize(
    "mock_operations_data, mock_profitable_cashback",
    [
        ([{"operation": "transaction details"}], [{"category": "Supermarkets", "cashback": 15}]),
    ],
)
@patch("src.views.reading_operations_from_excel")
@patch("src.views.get_profitable_cashback")
def test_get_cat_services_profitable_cashback(
    mock_get_profitable_cashback, mock_reading_operations, mock_operations_data, mock_profitable_cashback
):
    mock_reading_operations.return_value = mock_operations_data
    mock_get_profitable_cashback.return_value = mock_profitable_cashback

    result = get_cat_services_profitable_cashback()
    assert result == mock_profitable_cashback


@pytest.mark.parametrize(
    "mock_operations_data, spending_data",
    [
        ([{"operation": "transaction details"}], {"category": "Supermarkets", "amount_spent": 150}),
    ],
)
@patch("src.views.reading_operations_from_excel")
@patch("src.views.spending_by_category")
def test_get_cat_report_spending_by_category(
    mock_spending_by_category, mock_reading_operations, mock_operations_data, spending_data
):
    mock_reading_operations.return_value = mock_operations_data
    mock_spending_by_category.return_value = spending_data

    result = get_cat_report_spending_by_category()
    assert result == spending_data
