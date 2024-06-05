# -*- coding: utf-8 -*-
# 用户信息
from PyQt5 import uic
from PyQt5.QtWidgets import *
from mysql import *


class UserInfo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi('./ui_administrator/user_info.ui')
        self.ui.borrow.clicked.connect(self.OpenBorrow)
        self.ui.Return.clicked.connect(self.OpenReturn)
        self.ui.book_information.clicked.connect(self.OpenBookInformation)
        self.ui.reserve.clicked.connect(self.OpenReserve)
        self.ui.setting.clicked.connect(self.OpenSetting)
        # self.create_table_in_scroll1_area()
        # self.create_table_in_scroll2_area()
        # self.create_table_in_scroll3_area()
        # self.create_table_in_scroll4_area()

        self.UserButton()
        self.OverdueButton()
        self.DamageButton()
        self.LostBooksButton()

        self.ui.user_button.clicked.connect(self.UserButton)  # 用户管理搜索
        self.ui.overdue_button.clicked.connect(self.OverdueButton)  # 逾期用户搜索
        self.ui.damage_button.clicked.connect(self.DamageButton)  # 书籍损坏搜索
        self.ui.lost_books_button.clicked.connect(self.LostBooksButton)  # 书籍挂失搜索

    # 定义按钮点击事件
    def OpenBorrow(self):
        from administration.Borrow import Borrow
        self.Borrow = Borrow()
        self.Borrow.ui.show()
        self.ui.close()

    def OpenReturn(self):
        from administration.Return import Return
        self.Return = Return()
        self.Return.ui.show()
        self.ui.close()

    def OpenBookInformation(self):
        from administration.book_information import BookInformation
        self.BookInformation = BookInformation()
        self.BookInformation.ui.show()
        self.ui.close()

    def OpenReserve(self):
        from administration.reserve import Reserve
        self.Reserve = Reserve()
        self.Reserve.ui.show()
        self.ui.close()

    def OpenSetting(self):
        from administration.setting import Setting
        self.Setting = Setting()
        self.Setting.ui.show()
        self.ui.close()

    # 用户管理
    # def create_table_in_scroll1_area(self):
    #     # 清除所有子部件
    #     layout = self.ui.scrollAreaWidgetContents_4.layout()
    #     while layout.count():
    #         child = layout.takeAt(0)
    #         if child.widget():
    #             child.widget().deleteLater()
    #
    #     # 创建表格部件
    #     self.table_widget = QTableWidget()
    #     layout.addWidget(self.table_widget)  # 添加表格到布局中
    #
    #     # 设置表格的列数
    #     self.table_widget.setColumnCount(5)  # 有8列
    #     column_labels = ["学号/工号", "姓名", "email", "手机号", "专业"]
    #     self.table_widget.setHorizontalHeaderLabels(column_labels)

    def UserButton(self):
        db = OpenMySql.open_connection()
        if db:
            try:
                cursor = db.cursor()
                usersearch = self.ui.user_search.text().strip()
                if usersearch:
                    sql = "SELECT student_account.id, student_information.name, email, phonenumber, student_account.major FROM student_account, student_information WHERE student_information.id = student_account.id AND student_account.id = %s"
                    cursor.execute(sql, (usersearch,))
                    data = cursor.fetchall()
                    self.refresh_table_data1(data)
                else:
                    sql = "SELECT student_account.id, student_information.name, email, phonenumber, student_account.major FROM student_account, student_information WHERE student_information.id = student_account.id"
                    cursor.execute(sql)
                    data = cursor.fetchall()
                    self.refresh_table_data1(data)
                    cursor.close()
            except Exception as e:
                print(e)
        else:
            QMessageBox.warning(self, "错误", "数据库连接失败")
        db.close()

    def refresh_table_data1(self, data):
        # 清除所有子部件
        layout = self.ui.scrollAreaWidgetContents_4.layout()
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # 创建表格部件
        self.table_widget = QTableWidget()
        layout.addWidget(self.table_widget)  # 添加表格到布局中

        # 设置表格的列数和列标签
        self.table_widget.setColumnCount(5)  # 有5列
        column_labels = ["学号/工号", "姓名", "email", "手机号", "专业"]
        self.table_widget.setHorizontalHeaderLabels(column_labels)

        # 插入数据到表格中
        if data:
            for row_number, row_data in enumerate(data):
                self.table_widget.insertRow(row_number)
                for column_number, column_data in enumerate(row_data):
                    item = QTableWidgetItem(str(column_data))
                    self.table_widget.setItem(row_number, column_number, item)

    # 逾期用户
    # def create_table_in_scroll2_area(self):
    #     # 清除所有子部件
    #     layout = self.ui.scrollAreaWidgetContents.layout()
    #     while layout.count():
    #         child = layout.takeAt(0)
    #         if child.widget():
    #             child.widget().deleteLater()
    #
    #     # 创建表格部件
    #     self.table_widget = QTableWidget()
    #     layout.addWidget(self.table_widget)  # 添加表格到布局中
    #
    #     # 设置表格的列数
    #     self.table_widget.setColumnCount(10)  # 有8列
    #     column_labels = ["书名", "作者", "介绍", "第一大类", "第二大类", "图书编号", "收藏", "预约"]
    #     self.table_widget.setHorizontalHeaderLabels(column_labels)

    def OverdueButton(self):
        db = OpenMySql.open_connection()
        if db:
            try:
                cursor = db.cursor()
                overdue = self.ui.user_overdue.text().strip()
                if overdue:
                    sql = "SELECT student_account.id, student_information.name, email, phonenumber, student_account.major FROM student_account, student_information WHERE student_information.id = student_account.id AND student_account.id = %s"
                    cursor.execute(sql, (overdue,))
                    data = cursor.fetchall()
                    self.refresh_table_data2(data)
                else:
                    sql = "SELECT student_account.id, student_information.name, email, phonenumber, student_account.major FROM student_account, student_information WHERE student_information.id = student_account.id"
                    cursor.execute(sql)
                    data = cursor.fetchall()
                    self.refresh_table_data2(data)
            except Exception as e:
                print(e)
        else:
            QMessageBox.warning(self, "错误", "数据库连接失败")

    def refresh_table_data2(self, data):
        # 清除所有子部件
        layout = self.ui.scrollAreaWidgetContents.layout()
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # 创建表格部件
        self.table_widget = QTableWidget()
        layout.addWidget(self.table_widget)  # 添加表格到布局中

        # 设置表格的列数和列标签
        self.table_widget.setColumnCount(5)  # 有5列
        column_labels = ["学号/工号", "姓名", "email", "手机号", "专业"]
        self.table_widget.setHorizontalHeaderLabels(column_labels)

        # 插入数据到表格中
        if data:
            for row_number, row_data in enumerate(data):
                self.table_widget.insertRow(row_number)
                for column_number, column_data in enumerate(row_data):
                    item = QTableWidgetItem(str(column_data))
                    self.table_widget.setItem(row_number, column_number, item)

    # 书籍损坏
    # def create_table_in_scroll3_area(self):
    #     # 清除所有子部件
    #     layout = self.ui.scrollAreaWidgetContents_2.layout()
    #     while layout.count():
    #         child = layout.takeAt(0)
    #         if child.widget():
    #             child.widget().deleteLater()
    #
    #     # 创建表格部件
    #     self.table_widget = QTableWidget()
    #     layout.addWidget(self.table_widget)  # 添加表格到布局中
    #
    #     # 设置表格的列数
    #     self.table_widget.setColumnCount(8)  # 有8列
    #     column_labels = ["书籍id", "书名", "借阅天数", "是否损坏", "手机号", "学号\工号", "姓名", "时间"]
    #     self.table_widget.setHorizontalHeaderLabels(column_labels)

    def DamageButton(self):
        db = OpenMySql.open_connection()
        if db:
            try:
                cursor = db.cursor()
                bookdamage = self.ui.book_damage.text().strip()
                if bookdamage:
                    sql = "SELECT book_id, book_name, borrow_day, sunhuai, phone_number, user_id, user_name, yymmdd FROM damaged_books WHERE user_id = %s"
                    cursor.execute(sql, (bookdamage,))
                    data = cursor.fetchall()
                    self.refresh_table_data3(data)
                else:
                    sql = "SELECT book_id, book_name, borrow_day, sunhuai, phone_number, user_id, user_name, yymmdd FROM damaged_books"
                    cursor.execute(sql)
                    data = cursor.fetchall()
                    self.refresh_table_data3(data)
            except Exception as e:
                print(e)
        else:
            QMessageBox.warning(self, "错误", "数据库连接失败")

    def refresh_table_data3(self, data):
        # 清除所有子部件
        layout = self.ui.scrollAreaWidgetContents_2.layout()
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # 创建表格部件
        self.table_widget = QTableWidget()
        layout.addWidget(self.table_widget)  # 添加表格到布局中

        # 设置表格的列数和列标签
        self.table_widget.setColumnCount(8)  # 有8列
        column_labels = ["书籍id", "书名", "借阅天数", "是否损坏", "手机号", "学号\工号", "姓名", "时间"]
        self.table_widget.setHorizontalHeaderLabels(column_labels)

        # 插入数据到表格中
        if data:
            for row_number, row_data in enumerate(data):
                self.table_widget.insertRow(row_number)
                for column_number, column_data in enumerate(row_data):
                    item = QTableWidgetItem(str(column_data))
                    self.table_widget.setItem(row_number, column_number, item)

    # 书籍挂失搜索
    # def create_table_in_scroll4_area(self):
    #     # 清除所有子部件
    #     layout = self.ui.scrollAreaWidgetContents_3.layout()
    #     while layout.count():
    #         child = layout.takeAt(0)
    #         if child.widget():
    #             child.widget().deleteLater()
    #
    #     # 创建表格部件
    #     self.table_widget = QTableWidget()
    #     layout.addWidget(self.table_widget)  # 添加表格到布局中
    #
    #     # 设置表格的列数
    #     self.table_widget.setColumnCount(3)  # 有8列
    #     column_labels = ["书籍id", "书名", "学号\工号"]
    #     self.table_widget.setHorizontalHeaderLabels(column_labels)

    def LostBooksButton(self):
        db = OpenMySql.open_connection()
        if db:
            try:
                cursor = db.cursor()
                lostbooks = self.ui.lost_books.text().strip()
                if lostbooks:
                    sql = "SELECT book_id, book_name, user_id FROM book_report_loss WHERE user_id = %s"
                    cursor.execute(sql, (lostbooks,))
                    data = cursor.fetchall()
                    self.refresh_table_data4(data)
                else:
                    sql = "SELECT book_id, book_name, user_id FROM book_report_loss"
                    cursor.execute(sql)
                    data = cursor.fetchall()
                    self.refresh_table_data4(data)
            except Exception as e:
                print(e)
        else:
            QMessageBox.warning(self, "错误", "数据库连接失败")

    def refresh_table_data4(self, data):
        # 清除所有子部件
        layout = self.ui.scrollAreaWidgetContents_3.layout()
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # 创建表格部件
        self.table_widget = QTableWidget()
        layout.addWidget(self.table_widget)  # 添加表格到布局中

        # 设置表格的列数和列标签
        self.table_widget.setColumnCount(3)  # 有3列
        column_labels = ["书籍id", "书名", "学号\工号"]
        self.table_widget.setHorizontalHeaderLabels(column_labels)

        # 插入数据到表格中
        if data:
            for row_number, row_data in enumerate(data):
                self.table_widget.insertRow(row_number)
                for column_number, column_data in enumerate(row_data):
                    item = QTableWidgetItem(str(column_data))
                    self.table_widget.setItem(row_number, column_number, item)
