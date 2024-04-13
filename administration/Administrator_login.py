# -*- coding: utf-8 -*-
from PyQt5 import uic
from PyQt5.QtWidgets import *


class AdministratorLogin(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi('./ui_administrator/administrator_interface.ui')
