# -*- coding: utf-8 -*-
import sys
from Main_interface import *

app = QApplication(sys.argv)
MainWindow = MainWindow()
MainWindow.ui.show()
app.exec_()


# from PyQt5.QtSql import QSqlDatabase
#
# print(QSqlDatabase.drivers())