import json
import logging
import os
from datetime import datetime

import numpy as np
import pandas as pd

from src.utils import date_add_month

np.set_printoptions(legacy="1.25")

services = logging.getLogger("services")
services.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(filename)s - %(levelname)s - %(message)s")
path_to_file: str = os.path.join(os.path.dirname(__file__), "../logs/services.log")
file_handler = logging.FileHandler(path_to_file, encoding="utf-8", mode="w")
file_handler.setFormatter(formatter)
services.addHandler(file_handler)


def get_profitable_cashback(data, year_par="2021", month_par="12"):
    """
    возвращает выгодные позиции кешбэка
    """
    services.debug("Обработка данных для выгодного кешбэка начата")
    # Преобразовать столбец даты
    data["Дата платежа"] = pd.to_datetime(data["Дата платежа"], format="%d.%m.%Y")

    # Границы диапазонов выборки
    date_begin = datetime.strptime(".".join(["01", month_par, year_par]), "%d.%m.%Y")  # "2021-12-31"
    date_end = date_add_month(date_begin)

    # Оставить данные только за выбранный период
    data_for_period = data.loc[(data["Дата платежа"] <= date_end) & (data["Дата платежа"] >= date_begin)]

    # Оставить данные только с кешбэком
    data_for_non_emt_cashback = data_for_period.loc[
        (data_for_period["Кэшбэк"].isna() is not True) & (data_for_period["Статус"] == "OK")
    ]

    # Удалить неиспользуемые данные
    data_for_period = []

    # Посчитать кешбэк по категориям
    series_cashback_cats = (
        data_for_non_emt_cashback.groupby("Категория", dropna=False)["Кэшбэк"].sum().sort_values(ascending=False)
    )
    json_output = json.dumps(dict(series_cashback_cats), ensure_ascii=False, indent=2)
    services.debug("Обработка данных для выгодного кешбэка закончена")
    return json_output
