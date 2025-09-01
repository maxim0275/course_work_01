import numpy as np
np.set_printoptions(legacy='1.25')

import json
import os
from datetime import datetime

import pandas as pd
from pandas import DataFrame, isna


def reading_operations_from_excel(file_path: str = "") -> DataFrame:
    """Преобразование файла из EXCEL в словарь"""
    # Получить имяя файла с операциями
    if file_path == "":
        file_path = os.path.join(os.path.dirname(__file__), "..", 'data', get_filename_opers_data())

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


def get_filename_opers_data():
    path_to_file: str = os.path.join(os.path.dirname(__file__), '../user_settings.json')
    with open(path_to_file, 'r', encoding='utf-8') as file:
        loaded_data = json.load(file)
    return loaded_data["filename_opers_data"]


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

        print(dicts)

        result.append(dicts)
    return result


def format_date_oper(date_str):
    result = date_str[6:10] + "-" + date_str[3:5] + "-" + date_str[0:2]
    return result


# print(format_date_oper("31.12.2021 16:44:00"))
#
# date_end = "2021-12-31"  # datetime.strptime(date_param, "%Y-%m-%d")
# date_begin = "2021-12-1"  # date_end.replace(day=1)

# print(date_end>date_begin)

# import pandas as pd
#
# # Представим, что у нас есть DataFrame
# df = pd.DataFrame({
#     'date': ['31.12.2020 16:44:00', '31.12.2021 16:44:00', '31.12.2022 16:44:00'],
#     'value': [10, 20, None]
# })
#
# print(df)
#
# df1 = df.loc[df['value'].isna() == True]
#
# print(df1)

# df["date"] = pd.to_datetime(df["date"], format="%d.%m.%Y %H:%M:%S")
# print(df)
# # Теперь мы проведем фильтрацию по интервалу с '2023-01-10' по '2023-01-31'
# filtered_df = df[(df['date'] >= '2023-01-10') & (df['date'] <= '2023-01-31')]
# print(filtered_df)


def get_top5_tran():
    """

    """
    result = []
    return result
