# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'user_settings_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import json
import os


class Ui_user_settings_window(object):
    def setupUi(self, user_settings_window):
        user_settings_window.setObjectName("user_settings_window")
        user_settings_window.resize(336, 249)
        self.verticalLayout = QtWidgets.QVBoxLayout(user_settings_window)
        self.verticalLayout.setObjectName("verticalLayout")
        self.api_input = QtWidgets.QLineEdit(user_settings_window)
        self.api_input.setObjectName("api_input")
        self.verticalLayout.addWidget(self.api_input)
        self.secret_input = QtWidgets.QLineEdit(user_settings_window)
        self.secret_input.setObjectName("secret_input")
        self.verticalLayout.addWidget(self.secret_input)
        self.userNo_input = QtWidgets.QLineEdit(user_settings_window)
        self.userNo_input.setObjectName("userNo_input")
        self.verticalLayout.addWidget(self.userNo_input)
        self.buttonBox = QtWidgets.QDialogButtonBox(user_settings_window)
        self.buttonBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Save)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.warning = QtWidgets.QMessageBox(parent=user_settings_window)
        self.warning.setWindowTitle("Ошибка!")
        self.warning.setText("Неправильно введены API или Secret ключи!")
        self.warning.setIcon(QtWidgets.QMessageBox.Warning)
        self.warning.setStandardButtons(QtWidgets.QMessageBox.Ok)

        self.success = QtWidgets.QMessageBox(parent=user_settings_window)
        self.success.setWindowTitle("Успех!")
        self.success.setText("Настройки сохранены успешно!")
        self.success.setIcon(QtWidgets.QMessageBox.Information)
        self.success.setStandardButtons(QtWidgets.QMessageBox.Ok)


        self.retranslateUi(user_settings_window)
        self.buttonBox.accepted.connect(user_settings_window.accept)
        self.buttonBox.accepted.connect(self.save_settings)
        self.buttonBox.rejected.connect(user_settings_window.reject)  # type: ignore
        QtCore.QMetaObject.connectSlotsByName(user_settings_window)

    def retranslateUi(self, user_settings_window):
        _translate = QtCore.QCoreApplication.translate
        user_settings_window.setWindowTitle(_translate("user_settings_window", "Настройки пользователя"))
        self.api_input.setPlaceholderText(_translate("user_settings_window", "API ключ"))
        self.secret_input.setPlaceholderText(_translate("user_settings_window", "Secret ключ"))
        self.userNo_input.setPlaceholderText(_translate("user_settings_window", "Номер пользователя (userNo)"))


    def save_settings(self):
        if self.api_input.text() != '' and len(self.api_input.text()) == 64:
            api_key = self.api_input.text()
        else:
            self.warning.exec_()
            return

        if self.secret_input != '' and len(self.secret_input.text()) == 64:
            secret_key = self.secret_input.text()
        else:
            self.warning.exec_()
            return

        if self.userNo_input.text() != '':
            user_no = self.userNo_input.text()
        else:
            self.warning.exec_()
            return

        data = {"api_key": api_key,
                "secret_key": secret_key,
                "userNo":  user_no}

        path = os.path.abspath("keys.json")
        with open(path, 'w') as outfile:
            json.dump(data, outfile)

        self.success.exec_()
