import asyncio
from requestManager import RequestManager


class Advertisment:
    def __init__(self, advNo):
        self.symbol = None
        self.trade_type = None
        self.active = False
        self.No = advNo
        self.spot_price = None
        self.min_order_limit = None
        self.max_order_limit = None
        self.payTypes = []
        self.min_clearance = 1
        self.price = None

        self.current_clearance = None

        self.rm = RequestManager()
        self.get_user_data()

    def get_user_data(self):
        data = self.rm.get_user_adv_data(self.No)

        if data:
            print(data)
            self.trade_type = data['tradeType']
            self.symbol = data['asset'] + "USDT"
            self.min_order_limit = data['minSingleTransAmount']
            self.max_order_limit = data['maxSingleTransAmount']

            for tm in data['tradeMethods']:
                self.payTypes.append(tm['payType'])

    def switch_activity(self, trigger):
        if trigger:
            self.active = True
        else:
            self.active = False

    def get_info(self):
        return {
            'symbol': self.symbol,
            'trade_type': self.trade_type,
            'active': self.active,
            'pay_types': self.payTypes,
            'min_order_limit': self.min_order_limit,
            'max_order_limit': self.max_order_limit,
            'cur_clearance': self.current_clearance
        }

    def set_new_price(self):
        temp = self.spot_price
        self.spot_price = self.rm.get_spot_price(self.symbol)
        if not self.spot_price:
            self.spot_price = temp

        self.rm.update_adv(self)


