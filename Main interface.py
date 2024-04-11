# -*- coding: utf-8 -*-
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *



class MainWindow:
    def __init__(self):
        self.ui = uic.loadUi('./ui/主界面.ui')


app = QApplication(sys.argv)
MainWindow = MainWindow()
MainWindow.ui.show()
app.exec()
