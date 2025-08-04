import json
import logging
import os
import dotenv
from views import get_current_time, reader_xlsx, get_currency, get_stocks, get_prices_ticker

dotenv.load_dotenv()

ex_change_api = os.getenv('API_KEY_CURRENCY')
secret_api = os.getenv('API_KEY_SECURITY')
ticker_api = os.getenv('API_KEY_TICKER')

filename_json = os.getenv('PATH_SETTING_JSON')


time = get_current_time()
path = os.getenv('PATH_XLSX')

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


def date_tim(times: time):
    logger.info("Запуск функции")
    """Главная функция, принимающая на вход строку с датой и временем"""
    start = input("Введите ???\n")
    if "???" in start:
        logger.info("Определение времени суток")
        if '6:00' <= str(times) <= '10:00':
            time_of_day = "Доброе утро"
            conclusion["greeting"] = time_of_day
        elif '10:00' <= str(times) <= '15:00':
            time_of_day = 'Добрый день'
            conclusion["greeting"] = time_of_day
        elif '15:00' <= str(times) <= '22:00':
            time_of_day = 'Добрый вечер'
            conclusion["greeting"] = time_of_day
        else:
            time_of_day = 'Доброй ночи'
            conclusion["greeting"] = time_of_day
        print(conclusion["greeting"])

        cards = reader_xlsx(path)
        cards_number.append(cards)
        logger.info("Перебор списка cards_number для получения данных")
        for c in cards_number[0]:
            currencies = c['Валюта операции']
            numbers = c['Номер карты']
            summa = c['Сумма операции']
            bonuses = c['Бонусы (включая кэшбэк)']
            number_for = {
                'Номер карты': numbers,
                'Общая сумма расходов': summa,
                'Валюта операции': currencies,
                'Бонусы (включая кэшбэк)': bonuses
            }
            conclusion["cards"].append(number_for)

            print(f"Номер карты: {numbers}\n Общая сумма расходов: {summa} {currencies}\n  Бонусы (включая кэшбэк): {bonuses}\n")

        cards_number[0].sort(key=lambda c: c["Сумма операции"])

        logger.info("Перебор списка cards_number для получения 5 словарей")
        for i in range(min(5, len(cards_number[0]))):
            card = cards_number[0][i]
            print(f"Сумма платежа: {card['Сумма платежа']} {card['Валюта платежа']}\n")
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
            print(f"{list_rub['currency']}: {list_rub['rate']} руб.\n")
            conclusion["currency_rates"].append(list_rub)

        logger.info("Перебор списка для получения курса евро")
        for q in list_eur:
            cycle_rub = q.get("RUB")
            list_rub = {"currency": "EUR", "rate": cycle_rub}
            print(f"{list_rub['currency']}: {list_rub['rate']} руб.\n")
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
            print(f"Название акции: {list_sy}\n Цена: {list_ask}\n")
            conclusion["stock_prices"].append(list_plus)

        logger.info("Запись в json файл")
        with open(filename_json, "w", encoding="utf-8") as f:
            json.dump(conclusion, f, ensure_ascii=False, indent=4)

    else:
        logger.info("Перезапуск функции")
        date_tim(time)


if __name__ == '__main__':
    date_tim(time)
