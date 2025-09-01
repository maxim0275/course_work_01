import numpy as np
import requests
from dotenv import load_dotenv

import json
import os
from datetime import datetime

import pandas as pd
from pandas import DataFrame, isna
from requests import request

np.set_printoptions(legacy='1.25')


def reading_operations_from_excel(file_path: str = "") -> DataFrame:
    """Преобразование файла из EXCEL в словарь"""
    # Получить имяя файла с операциями
    if file_path == "":
        file_path = os.path.join(os.path.dirname(__file__), "..", 'data', get_user_info(1))

    if not os.path.isfile(file_path):
        print("Файл не существует")
        return [{"Nothing"}]
    try:
        dataframe = pd.read_excel(file_path, engine="openpyxl")
    except Exception as e:
        print("Ошибка чтения файла")
        return [{"Nothing"}]

    # return dataframe.to_dict("records")
    return dataframe


def get_user_info(what_info_get):
    # 1: filename_opers_data, 2 : user_stocks, 3: user_currencies

    path_to_file: str = os.path.join(os.path.dirname(__file__), '../user_settings.json')
    with open(path_to_file, 'r', encoding='utf-8') as file:
        loaded_data = json.load(file)
        if what_info_get == 1:
            return loaded_data["filename_opers_data"]
        elif what_info_get == 2:
            return loaded_data["user_stocks"]
        else:
            return loaded_data["user_currencies"]


def get_card_out(data_cards, date_param):
    result = []
    # Границы диапазонов выборки
    date_end = datetime.strptime(date_param, "%Y-%m-%d")  # "2021-12-31"
    date_begin = date_end.replace(day=1)  # "2021-12-01"

    # Преобразовать столбец даты
    data_cards["Дата операции"] = pd.to_datetime(data_cards["Дата операции"], format="%d.%m.%Y %H:%M:%S")

    # Оставить из выборки только расходы
    cards_pays_only = data_cards.loc[
        (data_cards['Сумма платежа'] < 0) & (data_cards['Дата операции'] <= date_end)
        & (data_cards['Дата операции'] >= date_begin) & (data_cards['Номер карты'].isna() != True)]

    # Сформировать Series для сумм и кешбэка
    card_series_pay = cards_pays_only.groupby('Номер карты', dropna=False)['Сумма платежа'].sum()
    card_series_cashback = cards_pays_only.groupby('Номер карты', dropna=False)['Кэшбэк'].sum()

    # Для каждой карты занести сумму расходов и сумму кешбэка
    dicts = {"last_digits": "", "total_spent": 0, "cashback": 0}
    for card in card_series_pay.keys():
        dicts["last_digits"] = card[1:]
        dicts["total_spent"] = abs(card_series_pay.get(card))
        dicts["cashback"] = abs(card_series_cashback.get(card))
        result.append(dicts.copy())
    return result


def format_date_oper(date_str):
    result = date_str[6:10] + "-" + date_str[3:5] + "-" + date_str[0:2]
    return result


def get_top5_tran():
    """

    """
    result = []
    return result


def get_stocks():
    # Прочитать компании из настроек пользователя
    company_list = get_user_info(2)

    stocks_data = []
    # Для каждой компании считать цену акций
    stock_string = {"stock": "", "price": 0}
    for company in company_list:
        stock_for_company = get_stock(company)
        print(company)
        stock_string["stock"] = company
        stock_string["price"] = stock_for_company["high"]
        print(stock_string)
        stocks_data.append(stock_string.copy())
        print(stocks_data)
    return stocks_data


def get_stock(company_code):
    url = f'https://eodhd.com/api/real-time/{company_code}.US?api_token=68b537ae5548f1.52917953&fmt=json'
    payload = {}
    load_dotenv()
    api_key = os.getenv("API_KEY")
    headers = {"apikey": api_key}
    response = request("GET", url, headers=headers, data=payload)
    result = 0
    if response.status_code == 200:
        result_json = response.json()
    else:
        return []
    return result_json
