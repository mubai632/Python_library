# -*- coding: utf-8 -*-
# 归还书籍
from PyQt5 import uic
from PyQt5.QtWidgets import *


class Return(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi('./ui_administrator/Return.ui')
        self.ui.borrow.clicked.connect(self.OpenBorrow)
        self.ui.book_information.clicked.connect(self.OpenBookInformation)
        self.ui.reserve.clicked.connect(self.OpenReserve)
        self.ui.user_info.clicked.connect(self.OpenUserInfo)
        self.ui.setting.clicked.connect(self.OpenSetting)

    # 定义按钮点击事件
    def OpenBorrow(self):
        from administration.Borrow import Borrow
        self.Borrow = Borrow()
        self.Borrow.ui.show()
        self.ui.close()


    def OpenBookInformation(self):
        from administration.book_information import BookInformation
        self.BookInformation = BookInformation()
        self.BookInformation.ui.show()
        self.ui.close()

    def OpenReserve(self):
        from administration.reserve import Reserve
        self.Reserve = Reserve()
        self.Reserve.ui.show()
        self.ui.close()

    def OpenUserInfo(self):
        from administration.user_info import UserInfo
        self.UserInfo = UserInfo()
        self.UserInfo.ui.show()
        self.ui.close()

    def OpenSetting(self):
        from administration.setting import Setting
        self.Setting = Setting()
        self.Setting.ui.show()
        self.ui.close()

