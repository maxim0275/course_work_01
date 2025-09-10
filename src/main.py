from src.views import (generate_report, generate_report_wo_filename, get_cat_services_profitable_cashback,
                       get_cat_web_page_main)

print(get_cat_web_page_main("2021-12-31 23:00:00"))
print(get_cat_services_profitable_cashback())

# Вызов функции-отчета
generate_report()

# Вызов функции-отчета
generate_report_wo_filename()
