# -*- coding: utf-8 -*-
# 用户信息
from PyQt5 import uic
from PyQt5.QtWidgets import *


class UserInfo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi('./ui_administrator/user_info.ui')
        self.ui.borrow.clicked.connect(self.OpenBorrow)
        self.ui.Return.clicked.connect(self.OpenReturn)
        self.ui.book_information.clicked.connect(self.OpenBookInformation)
        self.ui.reserve.clicked.connect(self.OpenReserve)
        self.ui.setting.clicked.connect(self.OpenSetting)
        self.create_table_in_scroll1_area()
        self.create_table_in_scroll2_area()
        self.create_table_in_scroll3_area()
        self.create_table_in_scroll4_area()

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

    def create_table_in_scroll1_area(self):
        # 清除所有子部件
        layout = self.ui.scrollAreaWidgetContents_4.layout()
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # 创建表格部件
        self.table_widget = QTableWidget()
        layout.addWidget(self.table_widget)  # 添加表格到布局中

        # 设置表格的列数
        self.table_widget.setColumnCount(10)  # 有8列
        column_labels = ["书名", "作者", "介绍", "第一大类", "第二大类", "图书编号", "收藏", "预约"]
        self.table_widget.setHorizontalHeaderLabels(column_labels)

    def create_table_in_scroll2_area(self):
        # 清除所有子部件
        layout = self.ui.scrollAreaWidgetContents.layout()
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # 创建表格部件
        self.table_widget = QTableWidget()
        layout.addWidget(self.table_widget)  # 添加表格到布局中

        # 设置表格的列数
        self.table_widget.setColumnCount(10)  # 有8列
        column_labels = ["书名", "作者", "介绍", "第一大类", "第二大类", "图书编号", "收藏", "预约"]
        self.table_widget.setHorizontalHeaderLabels(column_labels)

    def create_table_in_scroll3_area(self):
        # 清除所有子部件
        layout = self.ui.scrollAreaWidgetContents_2.layout()
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # 创建表格部件
        self.table_widget = QTableWidget()
        layout.addWidget(self.table_widget)  # 添加表格到布局中

        # 设置表格的列数
        self.table_widget.setColumnCount(10)  # 有8列
        column_labels = ["书名", "作者", "介绍", "第一大类", "第二大类", "图书编号", "收藏", "预约"]
        self.table_widget.setHorizontalHeaderLabels(column_labels)

    def create_table_in_scroll4_area(self):
        # 清除所有子部件
        layout = self.ui.scrollAreaWidgetContents_3.layout()
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # 创建表格部件
        self.table_widget = QTableWidget()
        layout.addWidget(self.table_widget)  # 添加表格到布局中

        # 设置表格的列数
        self.table_widget.setColumnCount(10)  # 有8列
        column_labels = ["书名", "作者", "介绍", "第一大类", "第二大类", "图书编号", "收藏", "预约"]
        self.table_widget.setHorizontalHeaderLabels(column_labels)
