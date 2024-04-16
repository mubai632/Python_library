# -*- coding:utf-8 -*-
# 个人信息
from PyQt5 import uic
from PyQt5.QtWidgets import *

from mysql import OpenMySql


class PersonalInformation(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi('./ui_user/personal_information.ui')
        self.ui.tuijian_button.clicked.connect(self.OpenRecommended_books)
        self.ui.book_button.clicked.connect(self.OpenBookstore)
        self.ui.collect.clicked.connect(self.Opencollect)
        self.ui.reserve.clicked.connect(self.Openreserve)
        self.ui.report_loss.clicked.connect(self.OpenReportLoss)
        self.ui.pushButton.clicked.connect(self.user_performance)

        # 获取数据库内容
        # 连接到 MySQL 数据库
        self.db = OpenMySql.open_connection()
        if self.db:
            try:
                # 创建游标对象
                cursor = self.db.cursor()

                # 创建查询语句
                # 检查 ID 内容
                cursor.execute("SELECT id FROM dl_user")
                result = cursor.fetchone()
                cursor.close()

                # 在表中获取对应的基本信息
                # 创建游标对象
                cursor = self.db.cursor()
                cursor.execute("SELECT student_account.id, student_information.name, student_account.email, student_account.gender, student_information.major, student_account.phonenumber FROM student_account, student_information WHERE student_account.id=student_information.id and student_information.id = %s", (result[0],))
                results = cursor.fetchall()
                new_results = []
                # 遍历每个查询结果
                for row in results:
                    # 如果查询结果为 None，则使用空字符串替换
                    new_row = tuple('' if field is None else field for field in row)
                    new_results.append(new_row)
                cursor.close()
                self.db.close()
                self.ui.lineEdit_id.setText(new_results[0][0])
                self.ui.lineEdit_name.setText(new_results[0][1])
                self.ui.lineEdit_email.setText(new_results[0][2])
                self.ui.lineEdit_gender.setText(new_results[0][3])
                self.ui.lineEdit_major.setText(new_results[0][4])
                self.ui.lineEdit_phone_number.setText(new_results[0][5])
            except Exception as e1:
                print("An error occurred:", e1)
        else:
            QMessageBox.warning(self, '提示', '数据库连接失败')

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

    def user_performance(self):
        # 提交信息
        student_id = self.ui.lineEdit_id.text().strip()
        gender = self.ui.lineEdit_gender.text().strip()
        major = self.ui.lineEdit_major.text().strip()
        phone_number = self.ui.lineEdit_phone_number.text().strip()

        # 连接数据库
        self.db = OpenMySql.open_connection()
        # 创建一个新的游标
        cursor = self.db.cursor()
        sql = "UPDATE student_account SET gender = %s, major = %s, phonenumber = %s WHERE id = %s"
        value = (gender, major, phone_number, student_id)
        true = cursor.execute(sql, value)
        if true:
            self.db.commit()
            QMessageBox.warning(self, '提示', '提交成功')
        else:
            QMessageBox.warning(self, '提示', '提交失败')
        cursor.close()
        self.db.close()










