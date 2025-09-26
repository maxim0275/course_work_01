import os

import requests
from dotenv import load_dotenv

from src.cls_base_work_api import GetVacAPI
from src.utils import get_currency_rate


class HeadHunterHAPI(GetVacAPI):
    """Класс для получения вакансий с сайта с помощью API"""

    def __init__(self):
        self._answer = None

    def _connect_to_api(self, params=None) -> requests.models.Response:
        """
        Метод подключения к API HH и получения данных о вакансиях

        :param params: Словарь параметров запроса
        :return: Ответ от API или None в случае ошибки
        """
        load_dotenv()
        url_site = os.getenv("HH_API")
        url_api = url_site + "vacancies"

        try:
            # Выполнение GET-запроса к API
            response = requests.get(url_api, params=params)

            # Проверка успешности запроса
            response.raise_for_status()

            # Возврат JSON-ответа
            return response

        except requests.RequestException as e:
            # Обработка ошибок подключения
            print(f"Ошибка при подключении к API: {e}")
            return None

    def get_vacancies(self, key_word: str = None) -> list:
        """Метод для получения вакансий с сайта с помощью API"""
        """ Метод получает вакансии по запросу, в зависимости от параметров. Если key_word=False,
        то запрос выполняется по всем вакансиям с указанной зарплатой
        """
        if key_word:
            params = {"text": key_word, "currency": "RUR", "only_with_salary": "true", "page": 0, "per_page": 50}
        else:
            params = {"currency": "RUR", "only_with_salary": "true", "salary": "1000000", "page": 0, "per_page": 50}

        # получить вакансии
        response = self._connect_to_api(params)

        vacancy_list = response.json()["items"]
        vacancy_cutted_list = []
        if response.status_code == 200 and len(vacancy_list) > 0:

            def cut_attr(vacancy_dict) -> list:
                """Вернуть список со словарями только с указанными ключами"""
                return {k: vacancy_dict[k] for k in attr_dest}

            def convert_to_rur(src_val, koeff) -> float:
                """Если задан коэффициент, то вернуть сумму, умноженную на коэффициент"""
                if isinstance(src_val, int):
                    return src_val * koeff
                else:
                    return src_val

            def to_process_rate_curr(rate_curr) -> None:
                if rate_curr not in rates.keys():
                    queried_rate_curr = get_currency_rate(rate_curr)
                    if not queried_rate_curr:
                        print(f"для валюты {rate_curr} не найден курс. Коэффициент преревода в рубли установлен в 1")
                        rates[rate_curr] = 1
                    else:
                        rates[rate_curr] = queried_rate_curr["result"]

            # вынести на первый уровень словаря
            #   name из area; from, to из salary
            rates = {"RUR": 1}
            for vacancy in vacancy_list:
                vacancy["area_name"] = vacancy.get("area").get("name", "нет")

                # обработать валюту вакансии. Если курса валюты нет в списке - запросить через API и добавить
                to_process_rate_curr(vacancy.get("salary").get("currency", "нет"))

                # если указаны числовые значения границ зарплат, то привести их к рублю
                vacancy["salr_from"] = convert_to_rur(
                    vacancy.get("salary").get("from", 0), rates[vacancy.get("salary").get("currency", "нет")]
                )
                vacancy["salr_to"] = convert_to_rur(
                    vacancy.get("salary").get("to", 0), rates[vacancy.get("salary").get("currency", "нет")]
                )

            # Оставить только нужные ключи в списке
            attr_dest = ["id", "name", "area_name", "salr_from", "salr_to"]
            vacancy_cutted_list = list(map(cut_attr, vacancy_list))

        return vacancy_cutted_list

    @property
    def answer(self):
        return self._answer
