import json
import os
from time import sleep
from advertisments import Advertisment
from ui_manager import app, ui, MainWindow
import threading


class Script:
    def __init__(self):
        self.sell_eth_adv = None
        self.buy_eth_adv = None

        self.sell_btc_adv = None
        self.buy_btc_adv = None

        self.sell_bnb_adv = None
        self.buy_bnb_adv = None

        self.btc_spot_price = None
        self.eth_spot_price = None
        self.bnb_spot_price = None

    def get_advs(self):
        path = os.path.abspath("ads_no.json")
        with open(path, "r") as file:
            data = json.load(file)

        sell_eth_no = data.get("sell_eth_no", None)
        if sell_eth_no:
            self.sell_eth_adv = Advertisment(sell_eth_no)

        buy_eth_no = data.get("buy_eth_no", None)
        if buy_eth_no:
            self.buy_eth_adv = Advertisment(buy_eth_no)

        sell_btc_no = data.get("sell_btc_no", None)
        if sell_btc_no:
            self.sell_btc_adv = Advertisment(sell_btc_no)

        buy_btc_no = data.get("buy_btc_no", None)
        if buy_btc_no:
            self.buy_btc_adv = Advertisment(buy_btc_no)

        sell_bnb_no = data.get("sell_bnb_no", None)
        if sell_bnb_no:
            self.sell_bnb_adv = Advertisment(sell_bnb_no)

        buy_bnb_no = data.get("buy_bnb_no", None)
        if buy_bnb_no:
            self.buy_bnb_adv = Advertisment(buy_bnb_no)

    def switch_activity(self, asset, trigger, clearance):
        match asset:
            case 'sell_eth':
                self.sell_eth_adv.switch_activity(trigger, clearance)
            case 'buy_eth':
                self.buy_eth_adv.switch_activity(trigger, clearance)
            case 'sell_btc':
                self.sell_btc_adv.switch_activity(trigger, clearance)
            case 'buy_btc':
                self.buy_btc_adv.switch_activity(trigger, clearance)
            case 'sell_bnb':
                self.sell_bnb_adv.switch_activity(trigger, clearance)
            case 'buy_bnb':
                self.buy_bnb_adv.switch_activity(trigger, clearance)

    def get_ads_info(self):
        ads_info = {}
        if self.sell_eth_adv:
            ads_info['sell_eth_adv'] = self.sell_eth_adv.get_info()
        if self.buy_eth_adv:
            ads_info['buy_eth_adv'] = self.buy_eth_adv.get_info()

        if self.sell_btc_adv:
            ads_info['sell_btc_adv'] = self.sell_btc_adv.get_info()
        if self.buy_btc_adv:
            ads_info['buy_btc_adv'] = self.buy_btc_adv.get_info()

        if self.sell_bnb_adv:
            ads_info['sell_bnb_adv'] = self.sell_bnb_adv.get_info()
        if self.buy_bnb_adv:
            ads_info['buy_bnb_adv'] = self.buy_bnb_adv.get_info()

        return ads_info

    def update_adv(self, ):
        if self.sell_eth_adv and self.sell_eth_adv.active:
            self.sell_eth_adv.set_new_price()
        if self.buy_eth_adv and self.buy_eth_adv.active:
            self.buy_eth_adv.set_new_price()

        if self.sell_btc_adv and self.sell_btc_adv.active:
            self.sell_btc_adv.set_new_price()
        if self.buy_btc_adv and self.buy_btc_adv.active:
            self.buy_btc_adv.set_new_price()

        if self.sell_bnb_adv and self.sell_bnb_adv.active:
            self.sell_bnb_adv.set_new_price()
        if self.buy_bnb_adv and self.buy_bnb_adv.active:
            self.buy_bnb_adv.set_new_price()


def main():
    while True:
        bot.update_adv()
        ui.display_info(bot.get_ads_info())
        sleep(1)
        os.system('cls')


bot = Script()
bot.get_advs()
MainWindow.show()
ui.sell_eth_update_btn.clicked.connect(lambda: bot.switch_activity('sell_eth', ui.sell_eth_active_btn.isChecked(),
                                                                   ui.sell_eth_clearance_input.text()))
ui.buy_eth_update_btn.clicked.connect(lambda: bot.switch_activity('buy_eth', ui.buy_eth_active_btn.isChecked(),
                                                                  ui.buy_eth_clearance_input.text()))
ui.sell_btc_update_btn.clicked.connect(lambda: bot.switch_activity('sell_btc', ui.sell_btc_active_btn.isChecked(),
                                                                   ui.sell_btc_clearance_input.text()))
ui.buy_btc_update_btn.clicked.connect(lambda: bot.switch_activity('buy_btc', ui.buy_btc_active_btn.isChecked(),
                                                                  ui.buy_btc_clearance_input.text()))
ui.sell_bnb_update_btn.clicked.connect(lambda: bot.switch_activity('sell_bnb', ui.sell_bnb_active_btn.isChecked(),
                                                                   ui.sell_bnb_clearance_input.text()))
ui.buy_bnb_update_btn.clicked.connect(lambda: bot.switch_activity('buy_bnb', ui.buy_bnb_active_btn.isChecked(),
                                                                  ui.buy_bnb_clearance_input.text()))

thread = threading.Thread(target=main, daemon=True)
thread.start()
app.exec_()
