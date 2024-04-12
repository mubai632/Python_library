# -*- coding: utf-8 -*-
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication


class User_login_windows(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi('./ui_user/user_界面.ui')

