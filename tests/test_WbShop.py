import unittest
from berrylib import WbShop
import datetime

class TestWbShop(unittest.TestCase):

    def test_get_last_week(self):
        test_shop = WbShop(test=True)
        self.assertIsNotNone(test_shop.get_last_week()[0])
        self.assertIsNotNone(test_shop.get_last_week()[1])
        self.assertEqual(datetime.datetime.weekday(test_shop.get_last_week()[0]),0)
        self.assertEqual(datetime.datetime.weekday(test_shop.get_last_week()[1]),6)
        self.assertEqual(type(test_shop.get_last_week()[0]), datetime.date)
        self.assertEqual(type(test_shop.get_last_week()[1]), datetime.date)