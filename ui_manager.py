from ui.main_window import Ui_MainWindow
from ui.user_settings_window import Ui_user_settings_window
from ui.ads_settings_window import Ui_ads_settings_wnd
from PyQt5 import QtWidgets
import sys


def show_user_settings_window():
    user_settings_window.show()


def show_ads_settings_window():
    ads_settings_window.show()


app = QtWidgets.QApplication(sys.argv)

MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)

user_settings_window = QtWidgets.QDialog()
user_settings_ui = Ui_user_settings_window()
user_settings_ui.setupUi(user_settings_window)

ads_settings_window = QtWidgets.QDialog()
ads_settings_ui = Ui_ads_settings_wnd()
ads_settings_ui.setupUi(ads_settings_window)

ui.user_settings_act.triggered.connect(show_user_settings_window)
ui.ads_settings_act.triggered.connect(show_ads_settings_window)
