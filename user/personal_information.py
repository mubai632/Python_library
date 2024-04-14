# -*- coding:utf-8 -*-
# 个人信息
from PyQt5 import uic
from PyQt5.QtWidgets import *


class PersonalInformation(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi('./ui_user/personal_information.ui')
        self.ui.tuijian_button.clicked.connect(self.OpenRecommended_books)
        self.ui.book_button.clicked.connect(self.OpenBookstore)
        self.ui.collect.clicked.connect(self.Opencollect)
        self.ui.reserve.clicked.connect(self.Openreserve)
        self.ui.report_loss.clicked.connect(self.OpenReportLoss)

    # 定义按钮点击事件
    def OpenRecommended_books(self):
        from user.Recommended_books import RecommendedBooks
        self.RecommendedBooks = RecommendedBooks()
        self.RecommendedBooks.ui.show()
        self.ui.close()

    def OpenBookstore(self):
        from user.Bookstore import Bookstore
        self.Bookstore = Bookstore()
        self.Bookstore.ui.show()
        self.ui.close()

    def Opencollect(self):
        from user.collect import collect
        self.collect = collect()
        self.collect.ui.show()
        self.ui.close()

    def Openreserve(self):
        from user.reserve import reserve
        self.reserve = reserve()
        self.reserve.ui.show()
        self.ui.close()

    def OpenReportLoss(self):
        from user.Report_loss import ReportLoss
        self.ReportLoss = ReportLoss()
        self.ReportLoss.ui.show()
        self.ui.close()




