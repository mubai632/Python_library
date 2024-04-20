# -*- coding: utf-8 -*-
# 预约记录
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from mysql import OpenMySql


class SearchThread(QThread):
    search_finished = pyqtSignal(object)  # 定义一个信号，在搜索完成时发射

    def __init__(self, db, cursor):
        super().__init__()
        self.db = db
        self.cursor = cursor

    def run(self):
        # 查询数据库获取数据
        query = "SELECT * FROM book_reserve_table"
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        self.search_finished.emit(data)  # 发射信号，传递数据


class Reserve(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi('./ui_administrator/Reserve.ui')

        # 连接到 MySQL 数据库
        self.db = OpenMySql.open_connection()
        if self.db:
            try:
                # 创建一个游标并执行查询
                self.cursor = self.db.cursor()
                # 清除所有子部件
                layout = self.ui.scrollAreaWidgetContents.layout()
                while layout.count():
                    child = layout.takeAt(0)
                    if child.widget():
                        child.widget().deleteLater()

                # 创建表格部件
                self.table_widget = QTableWidget()
                layout.addWidget(self.table_widget)  # 添加表格到布局中

                # 设置表格的列数和对应的标题文字
                self.table_widget.setColumnCount(7)  # 有7列
                column_labels = ["用户id", "书名", "作者", "介绍", "第一大类", "第二大类", "编号"]
                self.table_widget.setHorizontalHeaderLabels(column_labels)

                # 创建并启动线程执行查询
                self.search_thread = SearchThread(self.db, self.cursor)
                self.search_thread.search_finished.connect(self.add_data_to_table)  # 连接信号到槽函数
                self.search_thread.start()
            except Exception as e:
                print("An error occurred:", e)

        self.ui.borrow.clicked.connect(self.OpenBorrow)
        self.ui.Return.clicked.connect(self.OpenReturn)
        self.ui.book_information.clicked.connect(self.OpenBookInformation)
        self.ui.user_info.clicked.connect(self.OpenUserInfo)
        self.ui.setting.clicked.connect(self.OpenSetting)

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


    def OpenUserInfo(self):
        from administration.user_info import UserInfo
        self.UserInfo = UserInfo()
        self.UserInfo.ui.show()
        self.ui.close()

    def OpenSetting(self):
        from administration.setting import Setting
        self.Setting = Setting()
        self.Setting.ui.show()
        self.ui.close()

    def add_data_to_table(self, data):
        # 将数据添加到表格中
        for row_data in data:
            self.add_row_to_table(row_data)

    def add_row_to_table(self, row_data):
        # 获取表格的当前行数
        current_row = self.table_widget.rowCount()

        # 插入新的一行
        self.table_widget.insertRow(current_row)

        # 在新行中添加数据
        for col_num, cell_data in enumerate(row_data):
            item = QTableWidgetItem(str(cell_data))
            self.table_widget.setItem(current_row, col_num, item)
