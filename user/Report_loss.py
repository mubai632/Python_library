# -*- coding:utf-8 -*-
# 挂失
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import time

from mysql import OpenMySql


# class SearchThread1(QThread):
#     search_finished = pyqtSignal(object)  # 定义一个信号，在搜索完成时发射
#
#     def __init__(self, db, cursor):
#         super().__init__()
#         self.db = db
#         self.cursor = cursor
#
#     def run(self):
#         sql ="SELECT id FROM dl_user"
#         self.cursor.execute(sql)
#         result = self.cursor.fetchone()
#
#         # 查询数据库获取数据
#         query = "SELECT * FROM admin_borrow WHERE user_id = %s ORDER BY yymmdd DESC"
#         self.cursor.execute(query, (result[0],))
#         data1 = self.cursor.fetchall()
#         time.sleep(2)
#         self.search_finished.emit(data1)  # 发射信号，传递数据
#
#
# class SearchThread2(QThread):
#     search_finished = pyqtSignal(object)  # 定义一个信号，在搜索完成时发射
#
#     def __init__(self, db, cursor):
#         super().__init__()
#         self.db = db
#         self.cursor = cursor
#
#     def run(self):
#         sql ="SELECT id FROM dl_user"
#         self.cursor.execute(sql)
#         result = self.cursor.fetchone()
#         if result is not None:
#             # 查询数据库获取数据
#             query = "SELECT * FROM book_report_loss WHERE user_id = %s"
#             self.cursor.execute(query, (result[0],))
#             data2 = self.cursor.fetchall()
#             time.sleep(2)
#             self.search_finished.emit(data2)  # 发射信号，传递数据


class ReportLoss(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi('./ui_user/report_loss.ui')
        self.ui.tuijian_button.clicked.connect(self.OpenRecommended_books)
        self.ui.book_button.clicked.connect(self.OpenBookstore)
        self.ui.collect.clicked.connect(self.Opencollect)
        self.ui.reserve.clicked.connect(self.Openreserve)
        self.ui.personal_information.clicked.connect(self.OpenPersonalInformation)

        self.db = OpenMySql.open_connection()
        self.cursor = self.db.cursor()

        # 在进入报告界面之后的初始化函数中调用
        QTimer.singleShot(100, self.load_data)

    # 定义按钮点击事件
    def OpenRecommended_books(self):
        from user.Recommended_books import RecommendedBooks
        self.RecommendedBooks = RecommendedBooks()
        self.RecommendedBooks.ui.show()
        self.ui.close()
        # 如果存在旧的连接和游标，则先关闭它们
        self.close_old_connection_and_cursor()

    def OpenBookstore(self):
        from user.Bookstore import Bookstore
        self.Bookstore = Bookstore()
        self.Bookstore.ui.show()
        self.ui.close()
        # 如果存在旧的连接和游标，则先关闭它们
        self.close_old_connection_and_cursor()

    def Opencollect(self):
        from user.collect import collect
        self.collect = collect()
        self.collect.ui.show()
        self.ui.close()
        # 如果存在旧的连接和游标，则先关闭它们
        self.close_old_connection_and_cursor()

    def Openreserve(self):
        from user.reserve import reserve
        self.reserve = reserve()
        self.reserve.ui.show()
        self.ui.close()
        # 如果存在旧的连接和游标，则先关闭它们
        self.close_old_connection_and_cursor()

    def OpenPersonalInformation(self):
        from user.personal_information import PersonalInformation
        self.PersonalInformation = PersonalInformation()
        self.PersonalInformation.ui.show()
        self.ui.close()
        # 如果存在旧的连接和游标，则先关闭它们
        self.close_old_connection_and_cursor()

    def sss1(self):
        layout1 = self.ui.scrollAreaWidgetContents.layout()
        # 创建表格部件
        self.table_widget_1 = QTableWidget()
        layout1.addWidget(self.table_widget_1)  # 添加表格到布局中
        # 设置表格的列数和对应的标题文字
        self.table_widget_1.setColumnCount(8)  # 有8列
        column_labels = ["书籍编号", "书名", "借阅期限", "用户id", "用户姓名", "手机号", "借阅时间", "挂失"]
        self.table_widget_1.setHorizontalHeaderLabels(column_labels)

        sql = "SELECT id FROM dl_user"
        self.cursor.execute(sql)
        result = self.cursor.fetchone()

        # 查询数据库获取数据
        query = "SELECT * FROM admin_borrow WHERE user_id = %s ORDER BY yymmdd DESC"
        self.cursor.execute(query, (result[0],))
        data1 = self.cursor.fetchall()
        self.add_data_to_table_1(data1)

    def sss2(self):
        layout2 = self.ui.scrollAreaWidgetContents_2.layout()
        # 创建表格部件
        self.table_widget_2 = QTableWidget()
        layout2.addWidget(self.table_widget_2)  # 添加表格到布局中
        # 设置表格的列数和对应的标题文字
        self.table_widget_2.setColumnCount(4)  # 有4列
        column_labels = ["书籍编号", "书名", "用户id", "取消挂失"]
        self.table_widget_2.setHorizontalHeaderLabels(column_labels)

        sql = "SELECT id FROM dl_user"
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        if result is not None:
            # 查询数据库获取数据
            query = "SELECT * FROM book_report_loss WHERE user_id = %s"
            self.cursor.execute(query, (result[0],))
            data2 = self.cursor.fetchall()
            self.add_data_to_table_2(data2)

    def add_data_to_table_1(self, data):
        # 如果数据为空，则直接返回，不执行后续操作
        if not data:
            return
        # 删除之前的空行
        self.table_widget_1.removeRow(0)
        # 将数据添加到表格1中
        self.add_row_to_table1(data)

    def add_data_to_table_2(self, data):
        # 如果数据为空，则直接返回，不执行后续操作
        if not data:
            return
        # 删除之前的空行
        self.table_widget_2.removeRow(0)

        self.add_row_to_table2(data)

    def add_row_to_table1(self, row_data):
        # 获取表格的当前行数
        current_row = self.table_widget_1.rowCount()

        # 在新行中添加数据
        for row_number, data in enumerate(row_data):
            self.table_widget_1.insertRow(current_row + row_number)  # 使用 current_row + row_number 作为新行的索引
            for column_number, column_data in enumerate(data):
                item = QTableWidgetItem(str(column_data))
                self.table_widget_1.setItem(current_row + row_number, column_number, item)

            # 添加挂失按钮
            book_delete = QPushButton("挂失")
            book_delete.clicked.connect(lambda state, row=current_row + row_number: self.ReportLoss(row))
            self.table_widget_1.setCellWidget(current_row + row_number, 7, book_delete)  # 在每行的最后一列添加按钮

    def add_row_to_table2(self, row_data):
        # 获取表格的当前行数
        current_row = self.table_widget_2.rowCount()

        # 在新行中添加数据
        for row_number, data in enumerate(row_data):
            self.table_widget_2.insertRow(current_row + row_number)  # 使用 current_row + row_number 作为新行的索引
            for column_number, column_data in enumerate(data):
                item = QTableWidgetItem(str(column_data))
                self.table_widget_2.setItem(current_row + row_number, column_number, item)

            # 添加取消挂失按钮
            book_delete = QPushButton("取消挂失")
            book_delete.clicked.connect(lambda state, row=current_row + row_number: self.NoReportLoss(row))
            self.table_widget_2.setCellWidget(current_row + row_number, 3, book_delete)  # 在每行的最后一列添加按钮

    def ReportLoss(self, row):
        # 获取要挂失的行的数据
        num_cols = self.table_widget_1.columnCount()
        items = []
        for col in range(num_cols):
            item = self.table_widget_1.item(row, col)
            if item is not None:
                items.append(item.text())
        try:
            # 检索借阅图书是否存在
            self.cursor.execute("SELECT COUNT(*) FROM admin_borrow WHERE book_id = %s AND user_id = %s",
                                (items[0], items[3]))
            result = self.cursor.fetchone()
            count = result[0]
            if count == 1:
                # 检索挂失图书是否已挂失
                self.cursor.execute("SELECT COUNT(*) FROM book_report_loss WHERE book_id = %s AND user_id = %s",
                                    (items[0], items[3]))
                result1 = self.cursor.fetchone()
                count = result1[0]
                if count == 0:
                    # 插入数据
                    sql = "Insert into book_report_loss VALUES (%s, %s, %s)"
                    self.cursor.execute(sql, (items[0], items[1], items[3]))
                    self.db.commit()  # 提交事务
                    QMessageBox.warning(self, "提示", "挂失成功!!!")
                else:
                    QMessageBox.warning(self, "提示", "挂失中!!!")

        except Exception as e:
            print("Error:", e)
        self.refresh_table()

    def NoReportLoss(self, row):
        # 获取要删除的行的数据
        num_cols = self.table_widget_2.columnCount()
        items = []
        for col in range(num_cols):
            item = self.table_widget_2.item(row, col)
            if item is not None:
                items.append(item.text())
        try:
            # 创建一个游标并执行查询
            self.cursor = self.db.cursor()
            # 检索收藏图书是否存在
            self.cursor.execute("SELECT COUNT(*) FROM book_report_loss WHERE book_id = %s AND user_id = %s",
                                (items[0], items[2]))
            result = self.cursor.fetchone()
            count = result[0]
            if count > 0:
                # 删除数据
                sql = "DELETE FROM book_report_loss WHERE book_id = %s AND user_id = %s"
                self.cursor.execute(sql, (items[0], items[2],))
                self.db.commit()  # 提交事务
                QMessageBox.warning(self, "提示", "删除成功!!!")

                # 删除成功后更新表格中的数据
                self.table_widget_2.removeRow(row)

        except Exception as e:
            print("Error:", e)
        self.refresh_table()

    def refresh_table(self):
        # 清空表格
        self.table_widget_2.clearContents()
        self.table_widget_2.setRowCount(0)

        # 重新加载表格数据
        data_from_database = self.get_data_from_database()  # 从数据库获取数据的函数
        self.add_row_to_table2(data_from_database)  # 使用新数据重新填充表格

    def get_data_from_database(self):
        sql = "SELECT id FROM dl_user"
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        if result is not None:
            # 查询数据库获取数据
            query = "SELECT * FROM book_report_loss WHERE user_id = %s"
            self.cursor.execute(query, (result[0],))
            data = self.cursor.fetchall()
            return data
        else:
            return None

    def load_data(self):
        self.sss1()
        self.sss2()

    # 使用close函数关闭界面的时候,调用函数,关闭数据库
    def close_old_connection_and_cursor(self):
        if self.cursor:
            self.cursor.close()
        if self.db:
            self.db.close()
        # 处理 Qt 事件队列，确保界面关闭前所有事件都被处理完毕
        QCoreApplication.processEvents()
