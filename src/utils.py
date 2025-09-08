import calendar
import json
import logging
import os
from datetime import timedelta

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
