import unittest
from unittest.mock import patch
import json
from datetime import time
# from main import date_tim
from src.main import date_tim


class TestDateTim(unittest.TestCase):

    @patch('src.views.reader_xlsx') # Замените '__main__' на имя модуля, где определена reader_xlsx
    @patch('src.views.get_currency') # Аналогично для get_currency
    @patch('src.views.get_stocks')   # Аналогично для get_stocks
    @patch('src.views.get_prices_ticker') # Аналогично для get_prices_ticker
    @patch('builtins.input', return_value="???")
    @patch('src.views.logger') #Аналогично для logger
    def test_date_tim(self, mock_logger, mock_input, mock_get_prices_ticker, mock_get_stocks, mock_get_currency, mock_reader_xlsx,):
        # Подготовка моковых данных
        mock_reader_xlsx.return_value = [{"Номер карты": "1234", "Сумма операции": 100, "Валюта операции": "RUB", "Бонусы (включая кэшбэк)": 10, "Дата платежа": "01.01.2024", "Категория": "Продукты", "Описание": "Пятерочка", "Сумма платежа": 50, "Валюта платежа": "RUB"}]
        mock_get_currency.return_value = {"RUB": 90}
        mock_get_stocks.return_value = "AAPL"
        mock_get_prices_ticker.return_value = [{"symbol": "AAPL", "ask": 150}]
        #Тестируемая функция



        date_tim(time(12, 0))

        #Здесь можно добавить asserts для проверки вызовов моков, вывода и записи в файл.
        mock_logger.info.assert_called()#Пример
        mock_reader_xlsx.assert_called()
