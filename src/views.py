import json
from datetime import datetime

import numpy as np

from src.cat_web_page_main import get_card_out, get_currency_rates, get_stocks, get_top5_tran, greeting
from src.reports import report_decorator, report_decorator_wo_filename, spending_by_category
from src.services import get_profitable_cashback
from src.utils import reading_operations_from_excel

np.set_printoptions(legacy="1.25")


def get_cat_web_page_main(date_par):
    """
    возвращает JSON данные для главной страницы
    """

    date_par_str = datetime.strftime(date_par, format="%Y-%m-%d %H:%M:%S")
    data = {"greeting": "", "cards": "", "top_transactions": "", "currency_rates": "", "stock_prices": ""}

    # Записать приветствие
    # if not parser.parse(date_par):
    #     return "Некорректная дата"

    greeting_text = greeting(date_par)

    # Прочитать данные операций
    operations_data = reading_operations_from_excel()
    # print(operations_data)

    # Записать расходы по картам
    cards_out_data = get_card_out(operations_data, date_par_str)

    # Записать Топ-5 транзакций по сумме платежа
    top5_transactions = get_top5_tran(operations_data, date_par_str)

    # Записать Курс валют
    currency_rates = get_currency_rates()

    # Записать Стоимость акций из S&P500
    stocks_companys = get_stocks()

    data["greeting"] = greeting_text
    data["cards"] = cards_out_data
    data["stock_prices"] = stocks_companys
    data["currency_rates"] = currency_rates
    data["top_transactions"] = top5_transactions

    return json.dumps(data, ensure_ascii=False, indent=2)


# my_date = datetime.strptime("2021-12-31 23:00:00", "%Y-%m-%d %H:%M:%S")
# print(get_cat_web_page_main(my_date))


def get_cat_services_profitable_cashback():
    """
    читает данные транзакций и возвращает выгодные кешбэки
    """
    operations_data = reading_operations_from_excel()
    operations_data = get_profitable_cashback(operations_data, year_par="2021", month_par="11")
    return operations_data


# print(get_cat_services_profitable_cashback())


def get_cat_report_spending_by_category():
    """
    читает данные транзакций и покупки по категории
    """
    operations_data = reading_operations_from_excel()
    data = spending_by_category(operations_data, "Супермаркеты")
    return data


@report_decorator("../data/report.txt")
def generate_report():
    """
    возвращает данные для отчета
    """
    # Формируем отчет
    report = get_cat_report_spending_by_category()
    return report


# Вызов функции-отчета
# generate_report()


@report_decorator_wo_filename()
def generate_report_wo_filename():
    """
    возвращает данные для отчета
    """
    report = get_cat_report_spending_by_category()
    return report


# Вызов функции-отчета
# generate_report_wo_filename()
