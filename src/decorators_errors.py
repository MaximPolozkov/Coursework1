import functools
import json
import os
import traceback

import logging

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


def handle_excel_errors(func):
    """Декоратор для обработки ошибок чтения XLSX."""
    logger.info("Запуск декоратора при чтении exel файла")

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError:
            print("Файл не найден.")
            logger.error('Файл не найден')
            return []
        except ImportError:
            print("Библиотека openpyxl не установлена.")
            logger.error('Библиотека openpyxl не установлена.')
            return []
        except Exception as e:
            print(f"Ошибка при перезаписи файла: {e}")
            logger.error(f"Ошибка при перезаписи файла: {e}")
            return []
    logger.info("Возвращает работу функции")
    return wrapper


def handle_date_errors(func):
    """Декоратор для обработки ошибок, связанных с датами."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            logger.error(f"Ошибка при обработке даты: {e}")
            print(f"Ошибка при обработке даты: {e}")
            return []
        except Exception as e:
            logger.error(f"Произошла ошибка в декораторе: {e}")
            print(f"Произошла ошибка в декораторе: {e}\nTraceback: {traceback.format_exc()}")
            return []
    return wrapper
