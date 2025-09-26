import json

from src.cls_safe_vacancy_excel import SafeVacancyExcel
from src.cls_safe_vacancy_json import SafeVacancyJson
from src.cls_safe_vacancy_txt import SafeVacancyTxt
from src.cls_vacancy import HHVacancy
from src.cls_vacancy_file import VacancyFile
from src.cls_work_api import HeadHunterHAPI
from src.user_interact import user_interact

# from cls_safe_vacancy_excel import SafeVacancyExcel
# from cls_safe_vacancy_json import SafeVacancyJson
# from cls_safe_vacancy_txt import SafeVacancyTxt
# from cls_vacancy import HHVacancy
# from cls_vacancy_file import VacancyFile
# from cls_work_api import HeadHunterHAPI
# from user_interact import user_interact

print("1 - запустить демонстрацию работы классов, 2 - запустить функцию взаимодействия с пользователем")
ans = input()
if ans== "1":
    hh = HeadHunterHAPI()
    data_vac = hh.get_vacancies("Python")
    print("Вакансии по ключевому слову Python:")
    for vac in data_vac:
        obj_vac = HHVacancy(vac['id'], vac['name'], vac['area_name'], vac['salr_from'],
                            vac['salr_to'])
        print(obj_vac)

    print(json.dumps(data_vac, indent=4, ensure_ascii=False))

    UtVac = SafeVacancyJson()
    UtVac.safe_vacancy(data_vac, "data/vacancy_json.json")

    UtVac = SafeVacancyTxt()
    UtVac.safe_vacancy(data_vac, "data/vacancy_txt.txt")

    UtVac = SafeVacancyExcel()
    UtVac.safe_vacancy(data_vac, "data/vacancy_excel.xslx")

    data_vacobj_1 = HHVacancy(data_vac[0]['id'], data_vac[0]['name'], data_vac[0]['area_name'], data_vac[0]['salr_from'],
                              data_vac[0]['salr_to'])
    data_vacobj_2 = HHVacancy(data_vac[1]['id'], data_vac[1]['name'], data_vac[1]['area_name'], data_vac[1]['salr_from'],
                              data_vac[1]['salr_to'])

    print(data_vacobj_1)
    print(data_vacobj_2)
    print(data_vacobj_1 < data_vacobj_2)

    # Манипуляции с вакансиями
    # Получение вакансий из файла
    vac_f = VacancyFile("data/vacancy_json.json")
    vacancy_fromfile = vac_f.get_vacacny_fromfile()
    print("Вакансии из файла:")
    for vac in vacancy_fromfile:
        obj_vac = HHVacancy(vac['id'], vac['name'], vac['area_name'], vac['salr_from'],
                            vac['salr_to'])
        print(obj_vac)

    # Добавить вакансии в файл
    hh = HeadHunterHAPI()
    data_vac = hh.get_vacancies("Пекарь")
    vac_f.add_vacancy_tofile(data_vac)

    # Удалить вакансии из файла
    vac_f.del_vacancy_fromfile()
elif ans =="2":
    user_interact()