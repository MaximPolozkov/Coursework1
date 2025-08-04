import datetime
import json
import logging
import os
from dotenv import load_dotenv
from views import reader_xlsx

load_dotenv()

path = os.getenv("PATH_XLSX")
filename_cashback = os.getenv("PATH_SETTING_CASHBACK")

log_dir = '../log'
log_file = os.path.join(log_dir, 'services.log')
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

logger = logging.getLogger(__name__)
file_handler = logging.FileHandler(log_file, "w", encoding="utf-8")
file_formatter = logging.Formatter('%(asctime)s %(filename)s %(funcName)s %(levelname)s: %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.ERROR)
logger.setLevel(logging.INFO)


def analyze_cashback_categories(data: str, year: int, month: int):
    """Анализирует категории кэшбэка"""
    logger.info("Запускаем функцию")

    cashback = {}
    analyze = []

    reader_categories = reader_xlsx(data)
    analyze.append(reader_categories)
    date_operation = []
    logger.info("Запускаем цикл для списка analyze")

    for e in analyze[0]:
        analyze_data = e['Дата операции']
        time_list = datetime.datetime.strptime(analyze_data.split()[0], "%d.%m.%Y").date()
        year_from_date = time_list.year
        month_from_date = time_list.month

        if int(year_from_date) == year and int(month_from_date) == month:
            date_operation.append(e)

    date_operation.sort(key=lambda c: c["Дата операции"])
    logger.info("Запускаем цикл для date_operation")

    for c in date_operation:
        bonus_cashback = c["Бонусы (включая кэшбэк)"]
        categories = c["Категория"]
        int(bonus_cashback)
        if bonus_cashback > 0:
            cashback[categories] = bonus_cashback

    logger.info("Записываем в файл user_settings_cashback")
    with open(filename_cashback, "w", encoding="utf-8") as f:
        json.dump(cashback, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    analyze_cashback_categories(path, 2019, 4)
