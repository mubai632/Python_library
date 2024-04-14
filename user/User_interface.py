# -*- coding: utf-8 -*-
# 用户界面
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow

# 自建模块
from user.Recommended_books import RecommendedBooks
from user.Registration_interface import RegistrationInterface

class UserLoginWindows(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi('./ui_user/user_interface.ui')
        self.ui.register_2.clicked.connect(self.OpenRegistrationInterface)
        self.ui.user_button.clicked.connect(self.OpenRecommended_books)

    # 定义按钮点击事件
    def OpenRegistrationInterface(self):
        self.RegistrationInterface = RegistrationInterface()
        self.RegistrationInterface.ui.show()
        self.ui.close()

    def OpenRecommended_books(self):
        self.RecommendedBooks = RecommendedBooks()
        self.RecommendedBooks.ui.show()
        self.ui.close()
