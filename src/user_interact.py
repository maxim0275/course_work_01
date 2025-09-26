from src.cls_vacancy import HHVacancy
from src.cls_work_api import HeadHunterHAPI


def user_interact() -> None:
    cond_keyword = ""
    cond_salary = ""
    user_answer = ""

    while user_answer != "5":
        print("Возможные действия:")
        print("1. Ввести ключевое слово для поиска вакансий")
        print("2. Ввести количество вакансий к получению по убыванию зарплаты.")
        print("3. Получить вакансии по ключевому слову.")
        print("4. Получить вакансии по зарплате")
        print("5. Выход из программы")
        print("===============================================================")
        print("Текущие условия:")
        print(f"Фильтр для отбора по зарплате: {cond_salary}")
        print(f"Фильтр для отбора по ключевому слову: {cond_keyword}")
        print("===============================================================")
        print("Ожидается ввод пользователя: (1, 2, 3, 4, 5): ____")

        user_answer = input()

        if user_answer == "1":
            print("1. Ввести ключевое слово для поиска вакансий:")
            cond_keyword = input()
        elif user_answer == "2":
            print("2. Ввести количество вакансий к получению по зарплате:")
            cond_salary = input()
        elif user_answer == "3":
            if not cond_keyword:
                print("Не указано ключевое слово")
            else:
                hh = HeadHunterHAPI()
                getted_vacancy = hh.get_vacancies(cond_keyword)
                for vac in getted_vacancy:
                    obj_vac = HHVacancy(vac["id"], vac["name"], vac["area_name"], vac["salr_from"], vac["salr_to"])
                    print(obj_vac)

        elif user_answer == "4":
            if not cond_salary:
                print("Не указано количество вакансий по зарплате.")
            else:
                hh = HeadHunterHAPI()
                getted_vacancy = hh.get_vacancies()
                for vac in getted_vacancy[: int(cond_salary)]:
                    obj_vac = HHVacancy(vac["id"], vac["name"], vac["area_name"], vac["salr_from"], vac["salr_to"])
                    print(obj_vac)
