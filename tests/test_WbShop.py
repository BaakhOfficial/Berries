import unittest
from berrylib import WbShop
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

if __name__ == "__main__":
    unittest.main()