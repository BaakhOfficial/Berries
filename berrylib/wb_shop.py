import datetime
import requests
import json

class WbShop:
    """
    That class represents your shop that you have on Wildberries
    """
    def __init__(self, api_key, name = 'Shop') -> None:
        self.api = api_key
        self.name = name

    def __str__(self):
         return f"{self.name}"

    def rsr(self, date_from = datetime.date(1997,8,10), date_to = datetime.date(1997,8,10), data_type = 'json'):
        """
        Returns realization sales report
        Default timespan is from the last monday to the last sunday
        dateFrom and dateTo has to be a datetime.datetime objects
        """
        if date_from == datetime.date(1997,8,10) and date_to == datetime.date(1997,8,10):
            days_until_sunday = (datetime.date.today().weekday() - 6) % 7
            last_sunday = datetime.date.today() - datetime.timedelta(days = days_until_sunday)
            monday = last_sunday - datetime.timedelta(days = 6)
            date_from = monday
            date_to = last_sunday
        
        # Authorization parameters
        headers = {
            'Authorization': self.api}
        # request
        response = requests.get('https://statistics-api.wildberries.ru/api/v1/supplier/reportDetailByPeriod',
                                headers=headers,
                                params={"dateFrom":date_from, "dateTo":date_to, 'rrdid':0})
        if data_type == 'json':
            jdata = json.loads(response.text)
            return jdata