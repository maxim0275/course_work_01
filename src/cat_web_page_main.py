import logging
import os
from datetime import datetime

import pandas as pd

from src.utils import get_currency_rate, get_stock, get_user_info

cat_web_page_main_logger = logging.getLogger("cat_web_page_main")
cat_web_page_main_logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(filename)s - %(levelname)s - %(message)s")
path_to_file: str = os.path.join(os.path.dirname(__file__), "../logs/cat_web_page_main.log")
file_handler = logging.FileHandler(path_to_file, encoding="utf-8", mode="w")
file_handler.setFormatter(formatter)
cat_web_page_main_logger.addHandler(file_handler)


def greeting(date_par):
    """
    Возвращает нужно приветствие в зависимости от времени суток
    """
    cat_web_page_main_logger.debug("Формирование приветствия")
    hours = date_par.hour
    if 5 < hours < 12:
        return "Доброе утро"
    elif 12 < hours < 19:
        return "Добрый день"
    elif 19 < hours < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def get_card_out(data_cards, date_param):
    """
    на входе данные транзаций и дата
    на выходе траты по картам за месяц в переданной дате
    """
    result = []
    cat_web_page_main_logger.debug("Обработка данных для выборки трат по картам начата")
    # Границы диапазонов выборки
    date_end = datetime.strptime(date_param, "%Y-%m-%d %H:%M:%S")  # "2021-12-31"
    date_begin = date_end.replace(day=1)  # "2021-12-01"

    # Преобразовать столбец даты
    data_cards["Дата операции"] = pd.to_datetime(data_cards["Дата операции"], format="%d.%m.%Y %H:%M:%S")

    # Оставить из выборки только расходы
    cards_pays_only = data_cards.loc[
        (data_cards["Сумма платежа"] < 0)
        & (data_cards["Дата операции"] <= date_end)
        & (data_cards["Дата операции"] >= date_begin)
        & (data_cards["Номер карты"].notna())
        & (data_cards["Статус"] == "OK")
    ]

    # Сформировать Series для сумм и кешбэка
    card_series_pay = cards_pays_only.groupby("Номер карты", dropna=False)["Сумма платежа"].sum().round(2)
    card_series_cashback = cards_pays_only.groupby("Номер карты", dropna=False)["Кэшбэк"].sum().round(2)

    # Для каждой карты занести сумму расходов и сумму кешбэка
    dicts = {"last_digits": "", "total_spent": 0, "cashback": 0}
    for card in card_series_pay.keys():
        dicts["last_digits"] = card[1:]
        dicts["total_spent"] = f"{abs(card_series_pay.get(card)):.2f}"
        dicts["cashback"] = f"{abs(card_series_cashback.get(card)):.2f}"
        result.append(dicts.copy())

    cat_web_page_main_logger.debug("Обработка данных для выборки трат по картам закончена")
    return result


def get_top5_tran(data_oper, date_param):
    """
    возвращает 5 самых больших транзакций
    """
    result = []
    cat_web_page_main_logger.debug("Обработка данных для 5 транзакций начата")
    # Границы диапазонов выборки
    date_end = datetime.strptime(date_param, "%Y-%m-%d %H:%M:%S")  # "2021-12-31"
    date_begin = date_end.replace(day=1)  # "2021-12-01"

    # Преобразовать столбец даты
    data_oper["Дата операции"] = pd.to_datetime(data_oper["Дата операции"], format="%d.%m.%Y %H:%M:%S")

    # Занести значения по модулю
    data_oper["Сумма платежа"] = data_oper["Сумма платежа"].apply(lambda x: abs(x))

    data_for_period = data_oper.loc[
        (data_oper["Дата операции"] <= date_end) & (data_oper["Дата операции"] >= date_begin)
    ]

    data_sorted = data_for_period.sort_values(by="Сумма платежа", ascending=False).head()

    pay_string = {"date": "", "amount": 0, "category": "", "description": ""}

    for index, pay in data_sorted.iterrows():
        pay_string["date"] = pay["Дата платежа"]
        pay_string["amount"] = pay["Сумма платежа"]
        pay_string["category"] = pay["Категория"]
        pay_string["description"] = pay["Описание"]
        result.append(pay_string.copy())

    cat_web_page_main_logger.debug("Обработка данных для 5 транзакций закончена")
    return result


def get_currency_rates():
    """
    возвращает курсы валют по отношению к рублю
    :return:
    """
    # Прочитать компании из настроек пользователя
    user_currencies = get_user_info(3)

    # Для каждой валюты считать курс
    currency_rates = []
    if user_currencies:
        currency_rate = {"currency": "", "rate": 0}
        for currency in user_currencies:
            currency_rate_response = get_currency_rate(currency)
            currency_rate["currency"] = currency
            currency_rate["rate"] = currency_rate_response["result"]
            currency_rates.append(currency_rate.copy())
    return currency_rates


def get_stocks():
    """
    возвращает цены на акции из списка в конфигурации пользователя
    :return:
    """
    # Прочитать компании из настроек пользователя
    company_list = get_user_info(2)

    stocks_data = []
    # Для каждой компании считать цену акций
    stock_string = {"stock": "", "price": 0}
    for company in company_list:
        stock_for_company = get_stock(company)
        stock_string["stock"] = company
        stock_string["price"] = stock_for_company["high"]
        stocks_data.append(stock_string.copy())
    return stocks_data
