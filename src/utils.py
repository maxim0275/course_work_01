import calendar
import json
import logging
import os
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from dotenv import load_dotenv
from pandas import DataFrame
from requests import request

np.set_printoptions(legacy="1.25")

utils_logger = logging.getLogger("utils")
utils_logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(filename)s - %(levelname)s - %(message)s")
path_to_file: str = os.path.join(os.path.dirname(__file__), "../logs/utils.log")
file_handler = logging.FileHandler(path_to_file, encoding="utf-8", mode="w")
file_handler.setFormatter(formatter)
utils_logger.addHandler(file_handler)


def get_user_info(what_info_get):
    """
    возвращает пользовательские настройки
    """
    # 1: filename_opers_data, 2 : user_stocks, 3: user_currencies

    path_to_file: str = os.path.join(os.path.dirname(__file__), "../user_settings.json")
    utils_logger.debug("Чтение файла с настройками")

    with open(path_to_file, "r", encoding="utf-8") as file:
        loaded_data = json.load(file)
        if what_info_get == 1:
            return loaded_data["filename_opers_data"]
        elif what_info_get == 2:
            return loaded_data["user_stocks"]
        else:
            return loaded_data["user_currencies"]


def reading_operations_from_excel(file_path: str = "") -> list[set[str]] | DataFrame:
    """
    возвращает dataframe с данными транзакций
    """
    # Получить имя файла с операциями
    if file_path == "":
        file_path = os.path.join(os.path.dirname(__file__), "..", "data", get_user_info(1))

    if not os.path.isfile(file_path):
        print("Файл не существует")
        return [{"Nothing"}]
    try:
        utils_logger.debug("Чтение файла с данными")
        dataframe = pd.read_excel(file_path, engine="openpyxl")
    except Exception:
        utils_logger.error("Ошибка чтения файла с транзакциями")
        print("Ошибка чтения файла")
        return [{"Nothing"}]

    return dataframe


def get_stock(company_code):
    """
    возвращает цену акций компании
    """
    url = f"https://eodhd.com/api/real-time/{company_code}.US?api_token=68b537ae5548f1.52917953&fmt=json"
    payload = {}
    load_dotenv()
    api_key = os.getenv("API_KEY")
    headers = {"apikey": api_key}
    response = request("GET", url, headers=headers, data=payload)
    if response.status_code == 200:
        result_json = response.json()
    else:
        return []
    return result_json


def get_currency_rate(currency):
    """
    возвращает через вызов API курс валюты по отношению к рублю
    """
    payload = {}
    load_dotenv()
    api_key = os.getenv("API_KEY1")
    headers = {"access_key": api_key}
    url_for_rates = f"https://api.currencylayer.com/convert?access_key={api_key}&from={currency}&to=RUB&amount=1"
    response = request("GET", url_for_rates, headers=headers, data=payload)
    if response.status_code == 200:
        result_json = response.json()
    else:
        return []
    return result_json


def date_add_month(date_src):
    """
    возвращает дата на месяц  ранее переданной даты
    """
    days_in_month = calendar.monthrange(date_src.year, date_src.month)[1]
    date_dst = date_src + timedelta(days=days_in_month - 1)
    return date_dst


def greeting(date_par):
    """
    Возвращает нужно приветствие в зависимости от времени суток
    """
    utils_logger.debug("Формирование приветствия")
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
    utils_logger.debug("Обработка данных для выборки трат по картам начата")
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

    utils_logger.debug("Обработка данных для выборки трат по картам закончена")
    return result


def get_top5_tran(data_oper, date_param):
    """
    возвращает 5 самых больших транзакций
    """
    result = []
    utils_logger.debug("Обработка данных для 5 транзакций начата")
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

    utils_logger.debug("Обработка данных для 5 транзакций закончена")
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
