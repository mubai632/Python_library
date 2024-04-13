# -*- coding: utf-8 -*-
# 用户注册界面
from PyQt5 import uic
from PyQt5.QtWidgets import *

from user.User_interface import *


class RegistrationInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi('./ui_user/Registration_interface.ui')
        self.ui.register_2.clicked.connect(self.registerSuccess)
        self.ui.clean.clicked.connect(self.resetFields)

    # 需要一些函数


    def registerSuccess(self):
        from user.User_interface import UserLoginWindows  # 因为循环打入的问题使用函数导入模块
        registration_dialog = QMessageBox(self)
        registration_dialog.setWindowTitle('提示...')
        registration_dialog.setText('注册成功!!!')
        registration_dialog.addButton('去登录...', QMessageBox.AcceptRole)
        registration_dialog.accepted.connect(self.goToLogin)  # 连接accepted信号到goToLogin槽函数
        registration_dialog.exec_()
        self.UserLogin = UserLoginWindows()
        self.UserLogin.ui.show()
        self.ui.close()

    def goToLogin(self):
        self.close()  # 关闭当前的注册界面


    def resetFields(self):
        # 清除所有文本框内容
        self.ui.id.clear()
        self.ui.password_1.clear()
        self.ui.password_2.clear()
        self.ui.email_1.clear()
