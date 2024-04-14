# -*- coding: utf-8 -*-
from PyQt5 import uic
from PyQt5.QtWidgets import *


class AdministratorLogin(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi('./ui_administrator/administrator_interface.ui')
        self.ui.user_button.clicked.connect(self.login)

    # 定义按钮点击事件
    def login(self):
        from administration.Borrow import Borrow
        self.Borrow = Borrow()
        self.Borrow.ui.show()
        self.ui.close()

