import os
import datetime
from typing import Any, List, Dict
import requests
import pandas as pd
from dotenv import load_dotenv

from decorators_errors import handle_excel_errors, handle_date_errors

import logging

load_dotenv()

xsxl = os.getenv("PATH_XLSX")

log_dir = '../log'
log_file = os.path.join(log_dir, 'views.log')
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

logger = logging.getLogger(__name__)
file_handler = logging.FileHandler(log_file, "w", encoding="utf-8")
file_formatter = logging.Formatter('%(asctime)s %(filename)s %(funcName)s %(levelname)s: %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.ERROR)
logger.setLevel(logging.INFO)

filename_currency_json = os.getenv("PATH_CURRENCY_jSON")
filename_price_json = os.getenv("PATH_PRICE_JSON")
path = os.getenv("PATH_XLSX")
secret_api = os.getenv('API_KEY_SECURITY')
ex_change_api = os.getenv('API_KEY_CURRENCY')

list_ticker = []


@handle_excel_errors
def reader_xlsx(str_xlsx: str):
    """Функция для чтения xlsx файлов и записи в json файл"""

    logger.info("Запускаем функцию")
    logger.info("Читаем файл exel")
    df = pd.read_excel(str_xlsx, engine="openpyxl")
    logger.info("Записываем в словарь")
    transaction = df.to_dict(orient="records")
    logger.info("Возвращаем записанный словарь")
    return transaction


@handle_date_errors
def sort_data(files_patch: List[Dict[str, Any]], date_column: str) -> List[Dict[str, Any]]:
    """Функция для сортировки операций с 1 числа месяца по текущую"""

    logger.info("Запускаем функцию")

    # if not date_column:
        # logger.info("Столбец с датой не указан или пуст.")
        # logger.info("Возвращаем пустой словарь")
        # return []

    end_date = datetime.datetime.strptime(date_column.split()[0], "%d.%m.%Y").date()
    logger.info("Записываем дату в end_date формате день, месяц, год")
    start_date = datetime.date(end_date.year, end_date.month, 1)
    logger.info("Записываем 1 число данного месяца и года в start_date")
    append_files = []
    for item in files_patch[0]:
        if item.get("Дата операции"):
            logger.info("Запускаем цикл для переданного списка в функцию со словарями")
            item_data_str = item.get("Дата операции")
            logger.info("Ищем поле дату операции с ее ключом")
            if not item_data_str:
                logger.info("Если нету даты операции пропускаем и продолжаем работу цикла")
                continue

            item_data = datetime.datetime.strptime(item_data_str.split()[0], "%d.%m.%Y").date()
            logger.info("Если дата имеет не верный формат делаем правильный и записываем в переменную item_data")
            if start_date <= item_data <= end_date:
                logger.info("Происходит получение операций по дате с первого числа данного месяца по принятую в функции")
                append_files.append(item)

    append_files.sort(key=lambda c: c["Дата операции"])
    logger.info("Возвращаем те операции которые были отсортированы по дате")

    return append_files


def get_currency(base: str, token: str) -> List[Dict[str, Any]]:  # token: ex_change_api
    """Функция получает через API курс валют к рублю"""
    logger.info("Запускаем функцию")
    url = f" https://v6.exchangerate-api.com/v6/{token}/latest/{base}"
    logger.info("Адрес API в переменной url")
    response = requests.request("GET", url)
    logger.info("Полученные данные response")
    response.raise_for_status()
    logger.info("Проверяем статус ошибки")
    data = response.json()
    logger.info("Записываем в json формат")
    logger.info("Возвращаем данные по полю 'conversion_rates'")
    return data['conversion_rates']


def get_currency_rates(base: str, symbol: str, token: str) -> List[Dict[str, Any]]:
    """Функция для конвертирования валют"""
    logger.info("Запускаем функцию")
    url = f' https://v6.exchangerate-api.com/v6/{token}/pair/{base}/{symbol}'  # token: ex_change_api
    logger.info("Передаем url")
    response = requests.request("GET", url)
    logger.info("Получаем данные и записываем в response")
    response.raise_for_status()
    logger.info("Получаем статус подключения")
    data = response.json()
    logger.info("Записываем в формат json")
    logger.info("Возвращаем в формате json")
    return data["conversion_rate"]


def get_stocks(token: str) -> List[Dict[str, Any]]:  # token: secret_api
    """Функция получает через API курсы акций"""
    logger.info("Запускаем функцию")
    url = f"https://api.tiingo.com/iex?token={token}"
    logger.info("Передаем url")
    headers = {"Content-Type": "application/json"}
    logger.info("Передаем формат в запрос")
    response = requests.get(url, headers=headers)
    logger.info("Происходит подключение к API")
    response.raise_for_status()
    logger.info("Получаем статус ошибки")
    item = response.json()
    logger.info("Записываем в формат json")
    logger.info("Возвращаем полученные данные")
    return item


def get_prices_ticker(stocks: List[Dict[str, Any]], token: str) -> List[Dict[str, Any]]:  # token ticker_api
    """Функция для получения цен на акции"""
    logger.info("Запускаем функцию")
    t = []
    logger.info("Создаем список для хранения поля названия акции")
    logger.info("Создаем список для фильтрации названия акций")
    filtered_t = []
    logger.info("Создаем счетчик чтобы ограничить количество записей")
    count = 0
    logger.info("Запускаем цикл для получения акций и их фильтрации")
    for x in stocks:
        if count >= 10:
            break
        if x["ticker"] and x["ticker"] is not None:
            if x["ticker"].isalpha():
                ticker_price = x["ticker"]
                url = f"https://api.finage.co.uk/last/stock/{ticker_price}?apikey={token}"
                headers = {"Content-Type": "application/json"}
                response = requests.request("GET", url, headers=headers)
                result = response.json()
                t.append(result)
                count += 1
    for p in t:
        if 'error' not in p:
            filtered_t.append(p)
    return filtered_t


def get_current_time():
    """Получает и возвращает текущее время."""
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M")
    return current_time


# if __name__ == "__main__":
    # r = reader_xlsx(xsxl)
    # print(r)
    # c = get_stocks(secret_api)
    # e = get_prices_ticker(c, "API_KEYa079XDRJJR9vKUvsYs8K5VXLrhS2nbtzH5WxzjV0tXzDRL")
    # print(e)
