# -*- coding:utf-8 -*-
# 推荐书籍
from PyQt5 import uic
from PyQt5.QtWidgets import *

from mysql import OpenMySql


class RecommendedBooks(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi('./ui_user/Recommended_books_Null.ui')
        # 连接到 MySQL 数据库
        self.db = OpenMySql.open_connection()
        if self.db:
            try:
                # 创建游标对象
                cursor = self.db.cursor()

                # 创建查询语句
                cursor.execute("SELECT major,id FROM student_account WHERE id = (SELECT id FROM dl_user)")
                result = cursor.fetchone()
                if result[0]:
                    self.ui = uic.loadUi('./ui_user/Recommended_books.ui')
                cursor.close()
                self.db.close()
            except Exception as e:
                print("An error occurred:", e)

        self.ui.book_button.clicked.connect(self.OpenBookstore)
        self.ui.collect.clicked.connect(self.Opencollect)
        self.ui.reserve.clicked.connect(self.Openreserve)
        self.ui.report_loss.clicked.connect(self.OpenReportLoss)
        self.ui.personal_information.clicked.connect(self.OpenPersonalInformation)

    # 定义按钮点击事件
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

    def OpenPersonalInformation(self):
        from user.personal_information import PersonalInformation
        self.PersonalInformation = PersonalInformation()
        self.PersonalInformation.ui.show()
        self.ui.close()

