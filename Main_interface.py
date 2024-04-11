# -*- coding: utf-8 -*-
from PyQt5 import uic
from User_login import *


class MainWindow(QMainWindow):  # 创建一个MainWindows主窗口类
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi('./ui/主界面.ui')  # 导入ui界面文件
        self.ui.user_button.clicked.connect(self.Open_user_login)

    def Open_user_login(self):
        self.User_login = User_login_windows()
        self.User_login.ui.show()
        self.ui.close()


