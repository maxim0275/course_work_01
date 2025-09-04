from datetime import datetime
from typing import Optional
import pandas as pd
from dateutil.relativedelta import relativedelta
import functools


def spending_by_category(transactions: pd.DataFrame,
                         category: str,
                         date: Optional[str] = None) -> pd.DataFrame:
    if date is None:
        date_end = datetime.strptime("31.12.2021", "%d.%m.%Y")
    else:
        date_end = datetime.strptime(date, "%d.%m.%Y")
    date_begin = date_end - relativedelta(months=3)

    # Преобразовать столбец даты
    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], format="%d.%m.%Y %H:%M:%S")

    # Оставить только данные с нужной категорией и статусом ОК
    date_cat = transactions.loc[(transactions["Категория"] == category) & (transactions["Статус"] == "OK")]

    # Оставить только данные за требуемый период
    data_need = date_cat.loc[((date_cat["Дата операции"] >= date_begin) & (date_cat["Дата операции"] <= date_end))]
    pd.set_option('display.max_columns', None)
    return data_need


# my_date = datetime.strptime("01.11.2025", "%d.%m.%Y").date()
# print(my_date)
#
# # my_date1 = date_add_month(my_date)
# # print(my_date1)
# #
# # my_date2 = my_date - datetime.timedelta(months=3)
# # print(my_date2)
# #
#
# last_month = my_date - relativedelta(months=3)
# print(last_month)
# # need to specify %Y%m%d as your output format
# print(last_month.strftime("%Y%m%d"))


def report_decorator(filename):
    """
    Декоратор с передачей имени файла
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)  # вызов функции-отчета
            with open(filename, 'w') as file:
                file.write(str(result) + '\n')  # запись результата в файл
            return result

        return wrapper

    return decorator


def report_decorator_wo_filename():
    """
    Декоратор с передачей имени файла
    """
    filename = '/data/report_spending_by_category_' + datetime.strftime(datetime.now(), "%Y-%m-%d") + '.txt'

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)  # вызов функции-отчета
            with open(filename, 'w') as file:
                file.write(str(result) + '\n')  # запись результата в файл
            return result

        return wrapper

    return decorator
