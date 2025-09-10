import json
from unittest.mock import mock_open, patch

import pandas as pd
import pytest

from src.reports import report_decorator, report_decorator_wo_filename, spending_by_category


@pytest.fixture
def transactions_data():
    """Фикстура, возвращающая данные о транзакциях."""
    data = {
        "Категория": ["Продукты", "Продукты", "Развлечения", "Продукты", "Продукты"],
        "Статус": ["OK", "OK", "OK", "OK", "Проблема"],
        "Сумма операции": [-100, -200, -50, -150, -300],
        "Дата операции": [
            "01.12.2021 12:00:00",
            "15.11.2021 12:00:00",
            "01.12.2021 12:00:00",
            "10.10.2021 12:00:00",
            "05.12.2021 12:00:00",
        ],
    }
    return pd.DataFrame(data)


@pytest.mark.parametrize(
    "category, last_date, expected_result",
    [
        (
            "Продукты",
            "31.12.2021",
            [
                {"День недели": "Monday", "Средние траты": 200.0},
                {"День недели": "Sunday", "Средние траты": 150.0},
                {"День недели": "Wednesday", "Средние траты": 100.0},
            ],
        )
    ],
)
def test_spending_by_category(transactions_data, category, last_date, expected_result):
    json_result = spending_by_category(transactions_data, category, last_date)
    result = json.loads(json_result)
    assert result == expected_result


@patch("builtins.open", new_callable=mock_open)
def test_report_decorator(mock_open):
    @report_decorator("test_report.txt")
    def sample_report():
        return "Sample Report Content"

    result = sample_report()
    mock_open().write.assert_called_with("Sample Report Content\n")
    assert result == "Sample Report Content"


@patch("builtins.open", new_callable=mock_open)
@patch("os.path.abspath")
def test_report_decorator_wo_filename(mock_abspath, mock_open):
    mock_abspath.return_value = "/mock/path/to/file"

    @report_decorator_wo_filename()
    def sample_report():
        return "Report Without Filename"

    result = sample_report()

    mock_open().write.assert_called_with("Report Without Filename\n")
    assert result == "Report Without Filename"
