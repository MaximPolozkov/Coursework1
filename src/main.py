import datetime
import json
import logging
import os
import dotenv
from views import (get_current_time, reader_xlsx, get_currency, get_stocks, get_prices_ticker, sort_data,
                   get_currency_rates)

dotenv.load_dotenv()

ex_change_api = os.getenv('API_KEY_CURRENCY')
secret_api = os.getenv('API_KEY_SECURITY')
ticker_api = os.getenv('API_KEY_TICKER')

path = "../data/operations.xlsx"

log_dir = '../log'
log_file = os.path.join(log_dir, 'main.log')
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

logger = logging.getLogger(__name__)
file_handler = logging.FileHandler(log_file, "w", encoding="utf-8")
file_formatter = logging.Formatter('%(asctime)s %(filename)s %(funcName)s %(levelname)s: %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.ERROR)
logger.setLevel(logging.INFO)

cards_number = []
conclusion = {"greeting": "", "cards": [], "top_transactions": [], "currency_rates": [], "stock_prices": []}
currency = []


def date_tim(date: str):
    logger.info("Запуск функции")
    """Главная функция, принимающая на вход строку с датой"""
    start = input("Введите ???\n")

    time = get_current_time()

    if "???" in start:
        logger.info("Определение времени суток")
        if '6:00' <= str(time) <= '10:00':
            time_of_day = "Доброе утро"
            conclusion["greeting"] = time_of_day
        elif '10:00' <= str(time) <= '15:00':
            time_of_day = 'Добрый день'
            conclusion["greeting"] = time_of_day
        elif '15:00' <= str(time) <= '22:00':
            time_of_day = 'Добрый вечер'
            conclusion["greeting"] = time_of_day
        else:
            time_of_day = 'Доброй ночи'
            conclusion["greeting"] = time_of_day
        # print(conclusion["greeting"])

        cards = reader_xlsx(path)
        cards_number.append(cards)

        if date:
            # date_format = date.strftime("%d.%m.%Y")
            number_format = sort_data(cards_number, date)
            currency = number_format
        else:
            data_today = datetime.date.today()
            date_format = data_today.strftime("%d.%m.%Y")
            number_format = sort_data(cards_number, date_format)
            currency = number_format

        logger.info("Перебор списка cards_number для получения данных")
        filter_format = {}
        for c in currency:
            currencies = c['Валюта операции']
            numbers = c['Номер карты']
            summa = c['Сумма операции']
            bonuses = c['Бонусы (включая кэшбэк)']

            if currencies != "RUB":
                exchange_rate = get_currency_rates(currencies, "RUB", ex_change_api)
                summa = round(exchange_rate * summa, 2)
                currencies = "RUB"

                int(summa)
                int(bonuses)

            if numbers not in filter_format:
                filter_format[numbers] = {
                    "Номер карты": numbers,
                    "Общая сумма расходов": round(0, 2),
                    "Общая сумма бонусов": round(0, 2)
                }
            str(summa)
            str(bonuses)

            filter_format[numbers]["Общая сумма расходов"] += abs(summa)
            filter_format[numbers]["Общая сумма бонусов"] += bonuses

        card_list = list(filter_format.values())

        conclusion["cards"].append(card_list)

        logger.info("Перебор списка cards_number для получения 5 словарей")

        for i in range(min(5, len(currency))):
            card = currency[i]
            # print(f"Сумма платежа: {card['Сумма платежа']} {card['Валюта платежа']}\n")
            top_translations = {
                'Дата платежа': card['Дата платежа'],
                'Категория': card['Категория'],
                'Описание': card['Описание']
            }
            conclusion["top_transactions"].append(top_translations)

        list_usd = []
        list_eur = []

        usd = get_currency("USD", ex_change_api)
        list_usd.append(usd)

        eur = get_currency("EUR", ex_change_api)
        list_eur.append(eur)

        logger.info("Перебор списка list_usd для получения кура доллара")
        for i in list_usd:
            cycle_rub = i.get("RUB")
            list_rub = {"currency": "USD", "rate": cycle_rub}
            # print(f"{list_rub['currency']}: {list_rub['rate']} руб.\n")
            conclusion["currency_rates"].append(list_rub)

        logger.info("Перебор списка для получения курса евро")
        for q in list_eur:
            cycle_rub = q.get("RUB")
            list_rub = {"currency": "EUR", "rate": cycle_rub}
            # print(f"{list_rub['currency']}: {list_rub['rate']} руб.\n")
            conclusion["currency_rates"].append(list_rub)

        list_top = []
        stock_top = get_stocks(secret_api)
        ticker_top = get_prices_ticker(stock_top, ticker_api)
        list_top.append(ticker_top)

        logger.info("Перебор списка для получения названия и цены акции")
        for w in list_top[0]:
            list_sy = w["symbol"]
            list_ask = w["ask"]
            list_plus = {
                "stock": list_sy,
                "price": list_ask
            }
            # print(f"Название акции: {list_sy}\n Цена: {list_ask}\n")
            conclusion["stock_prices"].append(list_plus)

        jsun_response = json.dumps(conclusion, ensure_ascii=False, indent=4)
        return jsun_response

    else:
        logger.info("Перезапуск функции")
        date_tim(time)


if __name__ == '__main__':
    x = date_tim("12.01.2018")
    print(x)
