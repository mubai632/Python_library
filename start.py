# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import *
from Main_interface import *

app = QApplication(sys.argv)
MainWindow = MainWindow()
MainWindow.ui.show()
app.exec_()
