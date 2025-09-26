import xlsxwriter

from src.cls_base_safe_vacancy import BaseSafeVacancy


class SafeVacancyExcel(BaseSafeVacancy):
    """Класс для сохранения данных о вакансиях в файл Excel"""

    def safe_vacancy(self, data: list, filename: str) -> None:
        """Метод для сохранения данных о вакансиях в файл Excel"""
        list_dict = [list(item.values()) for item in data]
        with xlsxwriter.Workbook(filename) as wb:
            ws = wb.add_worksheet("Лист 1")
            if len(data) == 0:
                ws.write_row("A1", [])
            else:
                ws.write_row("A1", data[0].keys())
                for row_index, vac_dict in enumerate(list_dict, start=1):
                    ws.write_row(row_index, 0, vac_dict)
