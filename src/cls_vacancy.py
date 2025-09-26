class HHVacancy:
    """ Класс для работы с вакансиями: объект при инициализации
    проверяет корректность значения параметров,
     зарплата устанавливается в среднее значение между границами,
     или значению одной из границ, иначе равняется нулю """

    __slots__ = ('vacancy_id', 'name', 'area_name', 'salary')

    def __init__(self, vacancy_id: str, name: str, area_name: str, salr_from: int, salr_to: int) -> None:
        if str(vacancy_id).isdigit():
            self.vacancy_id = vacancy_id
        else:
            raise ValueError("Некорректный идентификатор")

        if len(name) < 10:
            self.name = "Не указано"
        else:
            self.name = name

        if len(area_name) < 3:
            self.area_name = "Не указано"
        else:
            self.area_name = area_name

        self.salary = 0
        if isinstance(salr_from, int) and isinstance(salr_to, int):
            self.salary = (salr_from + salr_to) / 2
        elif isinstance(salr_from, int):
            self.salary = salr_from
        elif isinstance(salr_to, int):
            self.salary = salr_to

    def __lt__(self, other) -> bool:
        """ Метод для сравнения меньше """
        return self.salary < other.salary

    def __le__(self, other) -> bool:
        """ Метод для сравнения меньше или равно """
        return self.salary <= other.salary

    def __gt__(self, other) -> bool:
        """ Метод для сравнения больше """
        return self.salary > other.salary

    def __ge__(self, other) -> bool:
        """ Метод для сравнения больше или равно """
        return self.salary >= other.salary

    def __repr__(self) -> str:
        return f"Идентификатор={self.vacancy_id}, Вакансия={self.name}, Место={self.area_name}, Зарплата={self.salary}"
