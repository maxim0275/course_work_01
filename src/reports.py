import functools
import json
import logging
import os
from datetime import datetime
from typing import Optional

import numpy as np
import pandas as pd
from dateutil.relativedelta import relativedelta

np.set_printoptions(legacy="1.25")

reports = logging.getLogger("reports")
reports.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(filename)s - %(levelname)s - %(message)s")
path_to_file: str = os.path.join(os.path.dirname(__file__), "../logs/reports.log")
file_handler = logging.FileHandler(path_to_file, encoding="utf-8", mode="w")
file_handler.setFormatter(formatter)
reports.addHandler(file_handler)


def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> str:
    """
    возвращает суммы трат по выбранной категории за три месяца от переданной даты
    """
    reports.debug("Обработка данных для выборки сумм по дням недели начата")
    if date is None:
        date_end = datetime.strptime("31.12.2021", "%d.%m.%Y")
    else:
        date_end = datetime.strptime(date, "%d.%m.%Y")
    date_begin = date_end - relativedelta(months=3)

    # Преобразовать столбец даты
    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], format="%d.%m.%Y %H:%M:%S")

    # Оставить только данные с нужной категорией и статусом ОК и только платежи (отрицательные суммы)
    date_cat = transactions.loc[
        (transactions["Категория"] == category)
        & (transactions["Статус"] == "OK")
        & (transactions["Сумма операции"] < 0)
    ]

    # Оставить только данные за требуемый период
    data_need = date_cat.loc[((date_cat["Дата операции"] >= date_begin) & (date_cat["Дата операции"] <= date_end))]

    data_need["День недели"] = data_need["Дата операции"].dt.day_name()
    # data_need["День недели"] = data_need["Дата операции"].apply(
    #     lambda x: format_date(x, format='EEEE', locale='ru')
    # )
    data_need["Сумма операции"] = data_need["Сумма операции"].abs()

    average_spending_by_day = data_need.groupby("День недели")["Сумма операции"].mean().round().sort_index()

    result_dicts = []

    for day, avg_spending in average_spending_by_day.items():
        result_dict = {"День недели": day, "Средние траты": avg_spending}
        result_dicts.append(result_dict)

    result_json = json.dumps(result_dicts, ensure_ascii=False, indent=2)
    reports.debug("Обработка данных для выборки сумм по дням недели закончена")
    return result_json


def report_decorator(filename):
    """
    Декоратор функции генерирования отчета с передачей имени файла
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)  # вызов функции-отчета
            with open(filename, "w", encoding="utf-8") as file:
                file.write(str(result) + "\n")  # запись результата в файл
            return result

        return wrapper

    return decorator


def report_decorator_wo_filename():
    """
     Декоратор функции генерирования отчета без передачи имени файла
    """

    root_dir = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(
        root_dir, "..", "data", "report_spending_by_category_" + datetime.strftime(datetime.now(), "%Y-%m-%d") + ".txt"
    )

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)  # вызов функции-отчета
            with open(filename, "w", encoding="utf-8") as file:
                file.write(str(result) + "\n")  # запись результата в файл
            return result

        return wrapper

    return decorator
