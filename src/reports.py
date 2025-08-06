import datetime
import logging
import os
from typing import List, Dict, Any

from dotenv import load_dotenv

import pandas as pd

from decorators import report_decorator
from views import reader_xlsx

load_dotenv()

xlsx = "../data/operations.xlsx"

log_dir = '../log'
log_file = os.path.join(log_dir, 'reports.log')
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

logger = logging.getLogger(__name__)
file_handler = logging.FileHandler(log_file, "w", encoding="utf-8")
file_formatter = logging.Formatter('%(asctime)s %(filename)s %(funcName)s %(levelname)s: %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.ERROR)
logger.setLevel(logging.INFO)


@report_decorator(filename="../fuel_report.txt")
def wastes_category(category: pd.DataFrame, name_category: str, optional_data: str) -> pd.DataFrame:
    """Функция траты по категории"""
    logger.info("Запускаем функцию")

    if optional_data:
        logger.info("Проверяем есть ли переданная дата")
        data_obj = datetime.datetime.strptime(optional_data, "%d.%m.%Y").date()
        logger.info("Если есть переданная дата то получаем только дату в формате datetime")
    else:
        logger.info("Если переданной даты нету берем текущую")
        data_obj = datetime.date.today()

    logger.info("Получаем отсчитываем три месяца")
    three_month_ago = data_obj - datetime.timedelta(days=90)

    if "Дата операции" not in category.columns:
        logger.info("Проверяем есть ли поле в Датафрейме если нету возврощаем пустой Датафрейм")
        print("Ошибка: столбец 'Дата операции' не найден в DataFrame.")
        return pd.DataFrame()

    if not "Категория" in category.columns:
        logger.info("Проверяем есть ли поле Категория в Датафрэйме если нету возврощаем пустой Датафрэйм")
        print("Ошибка: столбец 'Категория' не найден в DataFrame.")
        return pd.DataFrame()

    if "Сумма операции с округлением" not in category.columns:
        logger.info("Проверяем есть ли Сумма операции с округлением в Датафрэйме если нету возврощаем пустой Датафрейм")
        print("Ошибка: столбец 'Сумма операции с округлением' не найден в DataFrame.")
        return pd.DataFrame()

    category["Дата операции"] = pd.to_datetime(category["Дата операции"].str.split().str[0], format="%d.%m.%Y").dt.date
    logger.info("Получаем дату по полю Дата операции и преобразуем ее в объект datetime")
    category["Категория операции"] = name_category
    logger.info("Получаем поле Категория операции в Датафрэйме и приравниваем к категирии которую получили в функции")
    category["Сумма операции с округлением"] = category["Сумма операции с округлением"].astype(str)
    logger.info("Получаем поле Сумма операции с округлением")

    logger.info("Создаем Датафрэйм с условиями")
    filtered_category = category[
        (category["Дата операции"] >= three_month_ago) &
        #(category["Дата операции"] <= data_obj) &
        (category["Категория"] == name_category) &
        (category["Сумма операции с округлением"] != "")
        ].copy()

    logger.info("Возврощаем созданный Датафрэйм")
    return filtered_category


if __name__ == "__main__":
    x = reader_xlsx(xlsx)
    df = pd.DataFrame(x)
    t = wastes_category(df, "Супермаркеты", "04.01.2018")

