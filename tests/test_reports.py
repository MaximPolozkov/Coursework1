import datetime
import unittest
from unittest.mock import patch

import pandas as pd

from reports import wastes_category


class TestWastesCategory(unittest.TestCase):

    @patch('reports.datetime.date')
    def test_wastes_category_default_date(self, mock_date):
        # Настраиваем mock для datetime.date.today()
        mock_date.today.return_value = datetime.date(2024, 1, 15)

        # Создаем DataFrame для теста
        data = {'Дата операции': ['10.01.2024', '20.10.2023'], 'Категория': ['Топливо', 'Продукты'], 'Сумма': [100, 500]}
        df = pd.DataFrame(data)

        # Вызываем функцию с тестовыми данными
        result_df = wastes_category(df, 'Топливо', '20.10.2023')

        # Проверяем результат
        self.assertEqual(len(result_df), 0)
        self.assertEqual(result_df['Сумма'].iloc[0], 100)
        #mock_date.today.assert_called_once()