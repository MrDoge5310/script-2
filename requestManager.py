import niquests
import json
import hashlib
import hmac
import os
from urllib.parse import urlencode
import time
import asyncio
from binance import Client


class RequestManager:
    def __init__(self):
        self.client = Client()
        self.base_url = "https://api.binance.com"
        self.market_link = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"

        self.user_data = None
        self.load_user_data()

        self.usdt_competitor = None

        self.session = niquests.Session(multiplexed=True)
        self.async_session = niquests.AsyncSession(multiplexed=True)

        server_time = self.session.get(self.base_url + "/api/v3/time").json()
        server_time = int(server_time["serverTime"])
        client_time = int(time.time() * 1000)
        self.recvWindow = server_time - client_time

        self.params = {
        "fiat": "UAH",
        "page": 1,
        "rows": 20,
        "countries": [],
        "proMerchantAds": False,
        "shieldMerchantAds": False,
        "publisherType": 'merchant',
        "payTypes": None,
        "classifies": ["mass", "profession"]
        }

    def load_user_data(self):
        file_path = os.path.abspath("keys.json")
        with open(file_path, 'r') as file:
            self.user_data = json.load(file)

    def generateSignaturedUrl(self, endpoint, api_secret_ex, params=None):
        timestamp = int(time.time() * 1000) + self.recvWindow
        if params:
            query_string = urlencode(params)
            # replace single quote to double quote
            query_string = query_string.replace("%27", "%22")
            if query_string:
                query_string = "{}&recvWindow=30000&timestamp={}".format(query_string, timestamp)
        else:
            query_string = "&recvWindow=60000&timestamp={}".format(timestamp)

        signature = hmac.new(api_secret_ex.encode("utf-8"), query_string.encode("utf-8"), hashlib.sha256).hexdigest()
        url = (self.base_url + endpoint + "?" + query_string + "&signature=" + signature)

        return url

    def get_usdt_competitor(self):
        params = self.params
        params['asset'] = "USDT"
        params['transAmount'] = 5000
        params["tradeType"] = "SELL"
        params["payTypes"] = ['Monobank']

        response = self.session.post(self.market_link, json=params).json()
        advertisements = response['data']

        for adv in advertisements:
            adv_max_cur = float(adv['adv']['tradableQuantity']) * float(adv['adv']['price'])
            adv_max = float(adv['adv']['maxSingleTransAmount'])
            if adv_max_cur < adv_max:
                adv_max = adv_max_cur
            adv_min = float(adv['adv']['minSingleTransAmount'])

            if adv_max - adv_min >= 4000 and adv_max - 5000 >= 5000:
                print(adv['advertiser']['nickName'], "-->", round(float(adv['adv']['price']) + 0.01, 2))
                self.usdt_competitor = adv
                break
            else:
                pass

    def get_competitor(self, adv_):
        if adv_.trade_type == 'SELL':
            tr_tp = "BUY"
        else:
            tr_tp = "SELL"
        params = self.params
        print(adv_.symbol)
        params['asset'] = adv_.symbol[:3]
        params['transAmount'] = None
        params["tradeType"] = tr_tp
        params["payTypes"] = adv_.payTypes

        response = self.session.post(self.market_link, json=self.params, stream=True)
        response = response.json()
        advertisements = response['data']

        self.get_usdt_competitor()
        usdt_competitor = self.usdt_competitor

        if tr_tp == 'BUY':
            buy_usdt_price = round(float(usdt_competitor['adv']['price']) + 0.01, 2)
        elif tr_tp == 'SELL':
            buy_usdt_price = round(float(usdt_competitor['adv']['price']) - 0.01, 2)

        for adv in advertisements:
            adv_max_cur = float(adv['adv']['tradableQuantity']) * float(adv['adv']['price'])
            adv_max = float(adv['adv']['maxSingleTransAmount'])
            if adv_max_cur < adv_max:
                adv_max = adv_max_cur
            adv_min = float(adv['adv']['minSingleTransAmount'])

            if tr_tp == 'BUY':
                cur_clearance = float(adv['adv']['price']) / adv_.spot_price - buy_usdt_price
            elif tr_tp == 'SELL':
                cur_clearance = buy_usdt_price - float(adv['adv']['price']) / adv_.spot_price

            minSingleTransAmount = int(adv_.min_order_limit)
            maxSingleTransAmount = int(adv_.max_order_limit)

            if (minSingleTransAmount + 5000 <= adv_max
                    and maxSingleTransAmount > adv_min
                    and adv_max - adv_min >= 4000
                    and adv['adv']['advNo'] != adv_.No
                    and cur_clearance > adv_.min_clearance):
                print(f"Спред {adv_.trade_type} {adv_.symbol[:3]}--> {round(cur_clearance, 2)} UAH --> {round(cur_clearance / 0.4, 2)}% --> {adv['advertiser']['nickName']}")
                adv_.current_clearance = round(cur_clearance, 2)
                adv_.price = adv['adv']['price']
                break
            else:
                pass

    def get_user_adv_data(self, adNo):
        params = {"adsNo": adNo}

        endpoint = "/sapi/v1/c2c/ads/getDetailByNo"

        headers = {"X-MBX-APIKEY": self.user_data['api_key'],
                   "clientType": "web"}

        url = self.generateSignaturedUrl(endpoint, self.user_data['secret_key'], params)

        response = self.session.post(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"Данные обьявления {data['data']['tradeType']} {data['data']['asset']} успешно получены")
            return data['data']
        else:
            print(f"Данные обьявления №: {adNo}, НЕ получены")
            return None

    def update_adv(self, adv):
        self.get_competitor(adv)
        param = {"advNo": adv.No, "price": adv.price}

        headers = {"Content-Type": "application/json;charset=utf-8",
                   "X-MBX-APIKEY": self.user_data['api_key'],
                   "clientType": "web"}

        endpoint = "/sapi/v1/c2c/ads/update"
        url = self.generateSignaturedUrl(endpoint, self.user_data['secret_key'])
        try:
            response = self.session.post(url, headers=headers, data=json.dumps(param))
            data = response.json()
            print(f"Обьявление {adv.trade_type} {adv.symbol[:3]} обновлено")
            print("---------------------")
        except:
             print("Помилка відправки запиту")

    def get_spot_price(self, symbol1):
        try:
            ticker = self.client.get_symbol_ticker(symbol=symbol1)
            return float(ticker['price'])
        except:
            return None