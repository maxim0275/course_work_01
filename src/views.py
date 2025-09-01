from src.utils import reading_operations_from_excel, get_card_out


def get_main():
    data = {"greeting": "", "cards": "", "top_transactions": "", "currency_rates": "", "stock_prices": ""}

    # Записать приветствие
    greeting = "Добрый день"

    # Прочитать данные операций
    operations_data = reading_operations_from_excel()
    # print(operations_data)

    # Записать расходы по картам
    cards_out_data = get_card_out(operations_data, '2021-12-31')
    # print(cards_out_data)

    # Записать Топ-5 транзакций по сумме платежа
    # top5_transactions = get_top5_tran()

    # Записать Курс валют
    # Записать Стоимость акций из S&P500

    data["greeting"] = "Добрый вечер"
    data["cards"] = cards_out_data
    return data


print(get_main())
