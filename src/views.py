from src.cat_web_page_main import (greeting, get_card_out, get_currency_rates,
                                   get_stocks, get_top5_tran)
from src.reports import spending_by_category, report_decorator, report_decorator_wo_filename
from src.services import get_profitable_cashback
from src.utils import reading_operations_from_excel


def get_cat_web_page_main():
    data = {"greeting": "", "cards": "", "top_transactions": "", "currency_rates": "", "stock_prices": ""}

    # Записать приветствие
    greeting_text = greeting()

    # Прочитать данные операций
    operations_data = reading_operations_from_excel()
    # print(operations_data)

    # Записать расходы по картам
    cards_out_data = get_card_out(operations_data, '2021-12-31')

    # Записать Топ-5 транзакций по сумме платежа
    top5_transactions = get_top5_tran(operations_data, '2021-12-31')

    # Записать Курс валют
    currency_rates = get_currency_rates()

    # Записать Стоимость акций из S&P500
    stocks_companys = get_stocks()

    data["greeting"] = greeting_text
    data["cards"] = cards_out_data
    data["stock_prices"] = stocks_companys
    data["currency_rates"] = currency_rates
    data["top_transactions"] = top5_transactions

    return data


# print(get_cat_web_page_main())

def get_cat_serivces_profitable_cashback():
    # Прочитать данные операций
    operations_data = reading_operations_from_excel()
    operations_data = get_profitable_cashback(operations_data, year_par="2021", month_par="11")
    return operations_data


# print(get_cat_serivces_profitable_cashback())

def get_cat_reoprt_spending_by_category():
    # Прочитать данные операций
    operations_data = reading_operations_from_excel()
    data = spending_by_category(operations_data, "Супермаркеты")

    return data


@report_decorator('../data/report.txt')
def generate_report():
    # Формируем отчет
    report = get_cat_reoprt_spending_by_category()
    return report


# Вызов функции-отчета
generate_report()


@report_decorator_wo_filename()
def generate_report_wo_filename():
    # Формируем отчет
    report = get_cat_reoprt_spending_by_category()
    return report


# Вызов функции-отчета
generate_report_wo_filename()
