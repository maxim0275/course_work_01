from datetime import datetime

import pandas as pd

from src.utils import date_add_month

import numpy as np

np.set_printoptions(legacy='1.25')

def get_profitable_cashback(data, year_par="2021", month_par="12"):
    result = {}

    # Преобразовать столбец даты
    data["Дата платежа"] = pd.to_datetime(data["Дата платежа"], format="%d.%m.%Y")

    # Границы диапазонов выборки
    date_begin = datetime.strptime(".".join(["01", month_par, year_par]), "%d.%m.%Y")  # "2021-12-31"
    date_end = date_add_month(date_begin)

    # Оставить данные только за выбранный период
    data_for_period = data.loc[(data['Дата платежа'] <= date_end) & (data['Дата платежа'] >= date_begin)]

    # Оставить данные только с кешбэком
    data_for_non_emt_cashback = data_for_period.loc[(data_for_period['Кэшбэк'].isna() != True) & (data_for_period['Статус'] == "OK")]

    # Удалить неиспользуемые данные
    data_for_period = []

    # Посчитать кешбэк по категориям
    series_cashback_cats = data_for_non_emt_cashback.groupby('Категория', dropna=False)['Кэшбэк'].sum().sort_values(ascending=False)
    # for category in series_cashback_cats.keys():
    #     result[category] = series_cashback_cats.get(category)

    return dict(series_cashback_cats)
