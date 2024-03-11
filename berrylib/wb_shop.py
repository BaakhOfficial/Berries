import datetime
import requests
import json
import pandas as pd

class WbShop:
    """pip
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
    def get_week(offset = 0):
        """
        Returns 2 values of the last week. Monday and Sunday
        """
        days_until_sunday = (datetime.date.today().weekday() - 6) % 7
        last_sunday = datetime.date.today() - datetime.timedelta(days = days_until_sunday) - datetime.timedelta(days = offset * 7)
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
        print(f'GET API request completed with code {response.status_code}')
        if response.ok:
            if d_type == 'json':
                json_ad_data = json.loads(response.text)
                return json_ad_data
            elif d_type == 'text':
                return response.text
            elif d_type == 'origin':
                return response
            elif d_type == 'df':
                return pd.DataFrame(json.loads(response.text))
        else:
            return None
             

    def rsr(self, date_from = datetime.date(1997,8,10), date_to = datetime.date(1997,8,10), data_type = 'json', offset = 0):
        """
        Returns realization sales report
        Default timespan is from the last monday to the last sunday
        dateFrom and dateTo has to be a datetime.datetime objects
        :data_type: can be "json" "text" "origin" "df" "df_grouped"
        """
        # !!!!!!!!!!!!!!!!!!!! Rework df_grouped and add df_grouped_rus data type !!!!!!!!!!!!!!!!!!!!!!!!!
        if date_from == datetime.date(1997,8,10) and date_to == datetime.date(1997,8,10):
            date_from, date_to = self.get_week(offset = offset)
            print(f'RSR export\nStart date: {date_from}\nEnd date: {date_to}')

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
        

    def ad_period_summary(self, date_from = datetime.date(1997,8,10), date_to = datetime.date(1997,8,10), offset = 0):
        """
        Exports Ad data from Wildberries. Right now returns only df type of data
        """
         #!!!!!!!!! ADD DATA TYPES !!!!!!!
         # SHITS WITH A NEW API

        if date_from == datetime.date(1997,8,10) and date_to == datetime.date(1997,8,10):
            date_from, date_to = self.get_week(offset = offset)

        print(f'Starts advertisement data export:\nStart date: {date_from}\nEnd date: {date_to}')
        json_report = self.get_request(url = f'https://advert-api{self.test_add}.wb.ru/adv/v1/upd',
                                    js_params={"from":date_from.strftime("%Y-%m-%d"), "to":date_to.strftime("%Y-%m-%d")},
                                    d_type = 'json')
        
        if json_report is not None:
            df_report = pd.DataFrame(json_report)
            df_report = df_report.groupby(by=['campName','paymentType','advertId','advertType'])['updSum'].sum().reset_index()
            df_report['nms'] = 0
            for j in range(len(df_report)):
                json_ad_data = self.get_request(url = f'https://advert-api{self.test_add}.wb.ru/adv/v0/advert',
                                    js_params={"id":df_report['advertId'][j]},
                                    d_type = 'json')
                if json_ad_data['type'] == 8:
                    df_report.loc[j,'nms'] = json_ad_data['autoParams']['nms'][0]
                elif json_ad_data['type'] == 9:
                    df_report.loc[j,'nms'] = json_ad_data['unitedParams']['nms'][0]
                elif json_ad_data['type'] in {4,5,6,7}:
                    df_report.loc[j,'nms'] = json_ad_data['params'][0]['nms'][0]['nm']

            df_report['startDate'] = date_from
            df_report['toDate'] = date_to
            df_report['entity'] = self.name
            return df_report
        
        else: print("There's no data in that time")
