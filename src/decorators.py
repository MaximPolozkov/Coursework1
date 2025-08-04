import datetime
import functools
import logging
import os

import pandas as pd
from typing import List, Dict, Any
from dotenv import load_dotenv

load_dotenv()


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


def reader_xlsx_decorators(func):
    """Декоратор для чтения XLSX файлов"""
    @functools.wraps(func)
    def wrapper(str_json: str):
        result = func(str_json)

        if not str_json:
            return result
        try:
            df = pd.read_excel(str_json, engine='openpyxl')
            transaction = df.to_dict(orient="records")
            return transaction
        except Exception as e:
            print(f"Ошибка при перезаписи файла: {e}")
        except (ValueError, KeyError) as e:
            print(f"Ошибка при обработке: {e}")
            return result

    return wrapper


def sort_data_decorator(func):
    """Декоратор для сортировки операций по дате."""
    @functools.wraps(func)
    def wrapper(files_patch: List[Dict[str, Any]], date_column: str) -> List[Dict[str, Any]]:
        """Обертка для исходной функции."""
        result = func(files_patch, date_column)  # Получаем результат исходной функции

        if not files_patch:
            return result

        try:
            sorted_data = sorted(files_patch, key=lambda x: datetime.datetime.strptime(x["Дата операции"].split()[0], '%d.%m.%Y').date() if x.get("Дата операции") else datetime.date(1900, 1, 1))
            return sorted_data
        except (ValueError, KeyError) as e:
            print(f"Ошибка при сортировке данных: {e}")
            return files_patch

    return wrapper


def report_decorator(filename=None):
    """Декоратор для функций-отчетов, записывающий результат в файл."""
    logger.info("Запускаем функцию")

    def decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            file_name = filename
            if not file_name:
                logger.info("Проверяем есть ли файл для записи если нету создаем")
                file_name = f"{func.__name__}_{datetime.date.today().strftime('%Y%m%d')}.txt"
            try:
                logger.info("Записываем данные в фаил")
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(str(result)) # Записываем результат в файл
                print(f"Отчет записан в файл: {file_name}")
            except Exception as e:
                logger.error(f"Если есть ошибка отображаем ее {e}")
                print(f"Ошибка при записи в файл: {e}")
            return result
        return wrapper
    return decorator






