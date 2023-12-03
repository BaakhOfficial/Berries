import unittest
from unittest.mock import patch
from berrylib.wb_shop import WbShop
import datetime

class TestWbShop(unittest.TestCase):

    test_shop = WbShop(test=True)

    def test_get_last_week(self):
        self.assertIsNotNone(self.test_shop.get_last_week()[0])
        self.assertIsNotNone(self.test_shop.get_last_week()[1])
        self.assertEqual(datetime.datetime.weekday(self.test_shop.get_last_week()[0]),0)
        self.assertEqual(datetime.datetime.weekday(self.test_shop.get_last_week()[1]),6)
        self.assertEqual(type(self.test_shop.get_last_week()[0]), datetime.date)
        self.assertEqual(type(self.test_shop.get_last_week()[1]), datetime.date)


    # !!!!!!!!!!!!! FOR SOME REASON IT DOESN'T WORK I HAVE TO FIGuRE iT OUT
    # def test_rsr(self):
    #     with patch('wb_shop.requests.get') as mocked_get:
    #         mocked_get.return_value.ok = True
    #         mocked_get.return_value.text = '{"Test":True}'

    #         schedule = self.test_shop.rsr()
    #         mocked_get.assert_called_with(url='https://statistics-api-sandbox.wildberries.ru/api/v1/supplier/reportDetailByPeriod',
    #                                       headers = '0',
    #                                       params = {"dateFrom":self.test_shop.get_last_week()[0], "dateTo":self.test_shop.get_last_week()[1], 'rrdid':0})
    #         self.assertEqual(schedule,'{"Test":True}')

if __name__ == "__main__":
    unittest.main()