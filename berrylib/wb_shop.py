import datetime
import requests
import json
import pandas as pd

class WbShop:
    """
    That class represents your shop that you have on Wildberries
    """
    def __init__(self, api_key = '0', name = 'Shop', test = False) -> None:
        self.api = api_key
        self.name = name
        if test == True:
            self.test_add = '-sandbox'
        else:
            self.test_add = ''

    def __str__(self):
         return f"{self.name}"
    
    @staticmethod
    def get_last_week():
        """
        Returns 2 values of the last week. Monday and Sunday
        """
        days_until_sunday = (datetime.date.today().weekday() - 6) % 7
        last_sunday = datetime.date.today() - datetime.timedelta(days = days_until_sunday)
        monday = last_sunday - datetime.timedelta(days = 6)
        return monday, last_sunday
    
    def get_request(self,url,js_params, d_type = 'origin'):
        """
        Allows you to make a manual request. Returns requests.models.Response in origin format
        """

        # Authorization parameters
        headers = {
            'Authorization': self.api}
        # Request
        response = requests.get(url,
                                headers=headers,
                                params=js_params)
        # Choosing type of exported data
        if response.ok:
            if d_type == 'json':
                jdata = json.loads(response.text)
                return jdata
            elif d_type == 'text':
                return response.text
            elif d_type == 'origin':
                return response
            elif d_type == 'df':
                return pd.DataFrame(json.loads(response.text))
        else:
            return None
             

    def rsr(self, date_from = datetime.date(1997,8,10), date_to = datetime.date(1997,8,10), data_type = 'json'):
        """
        Returns realization sales report
        Default timespan is from the last monday to the last sunday
        dateFrom and dateTo has to be a datetime.datetime objects
        :data_type: can be "json" "text" "origin" "df" "df_grouped"
        """
        # !!!!!!!!!!!!!!!!!!!! Rework df_grouped and add df_grouped_rus data type !!!!!!!!!!!!!!!!!!!!!!!!!
        if date_from == datetime.date(1997,8,10) and date_to == datetime.date(1997,8,10):
            date_from, date_to = self.get_last_week()
        
        if data_type == "df_grouped":
            df_report = self.get_request(url = f'https://statistics-api{self.test_add}.wildberries.ru/api/v1/supplier/reportDetailByPeriod',
                                    js_params={"dateFrom":date_from, "dateTo":date_to, 'rrdid':0},
                                    d_type = 'df')
            return df_report.groupby(by=["sa_name",'nm_id',"doc_type_name","supplier_oper_name",])\
                                                    [['quantity','retail_amount','retail_price_withdisc_rub',
                                                    'ppvz_for_pay', 'delivery_amount',
                                                    'return_amount', 'delivery_rub',
                                                    'penalty', 'additional_payment', ]]\
                                                    .sum(numeric_only=True)
            
        else:
            return self.get_request(url = f'https://statistics-api{self.test_add}.wildberries.ru/api/v1/supplier/reportDetailByPeriod',
                                    js_params={"dateFrom":date_from, "dateTo":date_to, 'rrdid':0},
                                    d_type = data_type)