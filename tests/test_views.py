import datetime

import requests
import os
import unittest
import pandas as pd

from typing import List, Dict, Any

from unittest.mock import patch, Mock
from dotenv import load_dotenv

from views import get_currency, get_stocks, sort_data, reader_xlsx, get_current_time

load_dotenv()

ex_change_api = os.getenv('API_KEY_CURRENCY')
source_api = os.getenv('API_KEY_SECURITY')


class TestReaderXLSX(unittest.TestCase):
    """Тесты для функции чтение файла XLSX"""

    def test_reader_xlsx_valid_file(self):
        """Проверяем, что функция правильно читает данные из xlsx файла."""
        xlsx_file = '../data/operations.xlsx'
        result = reader_xlsx(xlsx_file)
        self.assertEqual(result, result)


class TestSortData(unittest.TestCase):
    """Тесты для функции сортировки операций с 1 числа месяца"""

    def test_sort_data_valid_item(self):
        """Тест с валидным элементом в пределах диапазона дат."""
        date_column = "24.12.2021 19:53:32"
        expected_item = reader_xlsx('../data/operations.xlsx')
        result = sort_data(expected_item, date_column)
        self.assertEqual(result, result)

    def test_sort_data_empty_list(self):
        """Тест с пустым списком."""
        files_patch: List[Dict[str, Any]] = []
        date_column = "24.12.2021 19:53:32"
        result = sort_data(files_patch, date_column)
        self.assertEqual(result, result)

    def test_sort_data_missing_date(self):
        """Тест когда нет даты операции."""
        files_patch = reader_xlsx('../data/operations.xlsx')
        date_column = ""
        result = sort_data(files_patch, date_column)
        self.assertEqual(result, result)


class TestGetCurrency(unittest.TestCase):
    """Тесты для функции рубль к курсу валют"""

    @patch('requests.get')
    def test_get_currency_success(self, mock_get):
        """Тест успешного получения данных."""
        mock_response = Mock()
        mock_response.json.return_value = {'conversion_rates': {'RUB': 70.0}}
        mock_response.raise_for_status.return_value = 200
        result = get_currency(base='USD', token=ex_change_api)
        self.assertEqual(result, result)

    @patch('requests.get')
    def test_get_currency_request_error(self, mock_get):
        """Тест ошибки при запросе."""
        mock_get.side_effect = requests.exceptions.RequestException("Request failed")
        with self.assertRaises(requests.exceptions.HTTPError):
            get_currency(base="USD", token='test_token')


class TestGetStocks(unittest.TestCase):
    """Тесты для функции получения цен акций"""

    @patch('requests.get')
    def test_get_stocks_success(self, mock_get):
        """Тест успешного получения данных."""
        mock_response = Mock()
        mock_response.raise_for_status.return_value = 200
        mock_get.return_value = mock_response

        result = get_stocks(token=source_api)
        self.assertEqual(result, result)

    @patch('requests.get')
    def test_get_stocks_request_error(self, mock_get):
        """Тест ошибки при запросе."""
        mock_get.side_effect = requests.exceptions.RequestException("Request failed")
        with self.assertRaises(requests.exceptions.RequestException):
            get_stocks(token='test_token')


class TestGetCurrentTime(unittest.TestCase):
    """Тестирует функцию get_current_time."""
    @patch('datetime.datetime')
    @patch('builtins.input', return_value='Test User')
    def test_get_current_time(self, mock_input, mock_datetime):
        mock_datetime.now.return_value = datetime.datetime(2023, 10, 27, 12, 30)
        get_current_time()
        self.assertEqual("12:30", "12:30")
        mock_input.assert_called_once_with("Введите ваше имя\n")