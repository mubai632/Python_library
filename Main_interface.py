# -*- coding: utf-8 -*-
from PyQt5 import uic
from user.User_interface import *
from administration.Administrator_login import *


class MainWindow(QMainWindow):  # 创建一个MainWindows主窗口类
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi('./ui/主界面.ui')  # 导入ui界面文件
        self.ui.user_button.clicked.connect(self.OpenUserLogin)
        self.ui.gl_button.clicked.connect(self.OpenAdministrator)

    # 定义按钮点击事件
    def OpenUserLogin(self):    # 用户登录界面调用
        self.UserLogin = UserLoginWindows()     # 创建实例; 将UserLoginWindows类赋给当前实例的UserLogin属性
        self.UserLogin.ui.show()    # 调用实例的ui属性调用show方法, 显示界面
        self.ui.close()     # 调用实例ui属性的close方法, 关闭实例

    def OpenAdministrator(self):
        self.Administration = AdministratorLogin()
        self.Administration.ui.show()
        self.ui.close()

