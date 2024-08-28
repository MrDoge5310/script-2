# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ads_settings_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import json


class Ui_ads_settings_wnd(object):
    def setupUi(self, ads_settings_wnd):
        ads_settings_wnd.setObjectName("ads_settings_wnd")
        ads_settings_wnd.resize(511, 422)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(ads_settings_wnd)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.groupBox = QtWidgets.QGroupBox(ads_settings_wnd)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.sell_eth_no_input = QtWidgets.QLineEdit(self.groupBox)
        self.sell_eth_no_input.setObjectName("sell_eth_no_input")
        self.verticalLayout.addWidget(self.sell_eth_no_input)
        self.buy_eth_no_input = QtWidgets.QLineEdit(self.groupBox)
        self.buy_eth_no_input.setObjectName("buy_eth_no_input")
        self.verticalLayout.addWidget(self.buy_eth_no_input)
        self.verticalLayout_4.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(ads_settings_wnd)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.sell_btc_no_input = QtWidgets.QLineEdit(self.groupBox_2)
        self.sell_btc_no_input.setObjectName("sell_btc_no_input")
        self.verticalLayout_2.addWidget(self.sell_btc_no_input)
        self.buy_btc_no_input = QtWidgets.QLineEdit(self.groupBox_2)
        self.buy_btc_no_input.setObjectName("buy_btc_no_input")
        self.verticalLayout_2.addWidget(self.buy_btc_no_input)
        self.verticalLayout_4.addWidget(self.groupBox_2)
        self.groupBox_3 = QtWidgets.QGroupBox(ads_settings_wnd)
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.sell_bnb_no_input = QtWidgets.QLineEdit(self.groupBox_3)
        self.sell_bnb_no_input.setObjectName("sell_bnb_no_input")
        self.verticalLayout_3.addWidget(self.sell_bnb_no_input)
        self.buy_bnb_no_input = QtWidgets.QLineEdit(self.groupBox_3)
        self.buy_bnb_no_input.setObjectName("buy_bnb_no_input")
        self.verticalLayout_3.addWidget(self.buy_bnb_no_input)
        self.verticalLayout_4.addWidget(self.groupBox_3)
        self.buttonBox = QtWidgets.QDialogButtonBox(ads_settings_wnd)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_4.addWidget(self.buttonBox)

        self.warning = QtWidgets.QMessageBox(parent=ads_settings_wnd)
        self.warning.setWindowTitle("Ошибка!")
        self.warning.setText("Что-то пошло не так")
        self.warning.setIcon(QtWidgets.QMessageBox.Warning)
        self.warning.setStandardButtons(QtWidgets.QMessageBox.Ok)

        self.success = QtWidgets.QMessageBox(parent=ads_settings_wnd)
        self.success.setWindowTitle("Успех!")
        self.success.setText("Настройки сохранены успешно!")
        self.success.setIcon(QtWidgets.QMessageBox.Information)
        self.success.setStandardButtons(QtWidgets.QMessageBox.Ok)

        self.retranslateUi(ads_settings_wnd)
        self.buttonBox.accepted.connect(ads_settings_wnd.accept)  # type: ignore
        self.buttonBox.accepted.connect(self.save_settings)  # type: ignore
        self.buttonBox.rejected.connect(ads_settings_wnd.reject)  # type: ignore
        QtCore.QMetaObject.connectSlotsByName(ads_settings_wnd)

    def retranslateUi(self, ads_settings_wnd):
        _translate = QtCore.QCoreApplication.translate
        ads_settings_wnd.setWindowTitle(_translate("ads_settings_wnd", "Настройки обьявлений"))
        self.groupBox.setTitle(_translate("ads_settings_wnd", "ETH"))
        self.sell_eth_no_input.setPlaceholderText(_translate("ads_settings_wnd", "Номер обьявления продажа ETH"))
        self.buy_eth_no_input.setPlaceholderText(_translate("ads_settings_wnd", "Номер обьявления покупка ETH"))
        self.groupBox_2.setTitle(_translate("ads_settings_wnd", "BTC"))
        self.sell_btc_no_input.setPlaceholderText(_translate("ads_settings_wnd", "Номер обьявления продажа BTC"))
        self.buy_btc_no_input.setPlaceholderText(_translate("ads_settings_wnd", "Номер обьявления покупка BTC"))
        self.groupBox_3.setTitle(_translate("ads_settings_wnd", "BNB"))
        self.sell_bnb_no_input.setPlaceholderText(_translate("ads_settings_wnd", "Номер обьявления продажа BNB"))
        self.buy_bnb_no_input.setPlaceholderText(_translate("ads_settings_wnd", "Номер обьявления покупка BNB"))

    def save_settings(self):
        try:
            with open('../ads_no.json', 'r') as f:
                data = json.load(f)
        except:
            self.warning.exec_()

        print(data)

        if self.sell_eth_no_input.text() != '':
            data['sell_eth_no'] = self.sell_eth_no_input.text()

        if self.buy_eth_no_input.text() != '':
            data['buy_eth_no'] = self.buy_eth_no_input.text()

        if self.sell_btc_no_input.text() != '':
            data['sell_btc_no'] = self.sell_btc_no_input.text()

        if self.buy_btc_no_input.text() != '':
            data['buy_btc_no'] = self.buy_btc_no_input.text()

        if self.sell_bnb_no_input.text() != '':
            data['sell_bnb_no'] = self.sell_bnb_no_input.text()

        if self.buy_bnb_no_input.text() != '':
            data['buy_bnb_no'] = self.buy_bnb_no_input.text()

        with open('../ads_no.json', 'w') as f:
            json.dump(data, f)

        self.success.exec_()
