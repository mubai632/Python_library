# -*- coding: utf-8 -*-
# 归还书籍
from datetime import datetime

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
        query = "SELECT * FROM admin_return ORDER BY yymmdd DESC"
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        self.search_finished.emit(data)  # 发射信号，传递数据

class Return(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi('./ui_administrator/Return.ui')
        self.ui.borrow.clicked.connect(self.OpenBorrow)
        self.ui.book_information.clicked.connect(self.OpenBookInformation)
        self.ui.reserve.clicked.connect(self.OpenReserve)
        self.ui.user_info.clicked.connect(self.OpenUserInfo)
        self.ui.setting.clicked.connect(self.OpenSetting)

        self.ui.user_id.focusOutEvent = self.handle_focus_out_event  # 将文本框的焦点离开事件连接到自定义方法
        self.ui.pushButton.clicked.connect(self.InsertInto)

        self.db = OpenMySql.open_connection()
        self.cursor = self.db.cursor()
        layout = self.ui.scrollAreaWidgetContents.layout()
        # 创建表格部件
        self.table_widget = QTableWidget()
        layout.addWidget(self.table_widget)  # 添加表格到布局中
        # 设置表格的列数和对应的标题文字
        self.table_widget.setColumnCount(8)  # 有7列
        column_labels = ["书籍编号", "书名", "借阅期限", "是否损坏", "手机号", "用户id", "用户姓名", "归还时间"]
        self.table_widget.setHorizontalHeaderLabels(column_labels)

        # 创建并启动线程执行查询
        self.search_thread = SearchThread(self.db, self.cursor)
        self.search_thread.search_finished.connect(self.add_data_to_table)  # 连接信号到槽函数
        self.search_thread.start()

    # 定义按钮点击事件
    def OpenBorrow(self):
        from administration.Borrow import Borrow
        self.Borrow = Borrow()
        self.Borrow.ui.show()
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

    def handle_focus_out_event(self, event):
        # 当焦点离开文本框时执行比对操作
        self.UpdateBookName()
        event.accept()

    def UpdateBookName(self):
        bianhao = self.ui.bianhao.text().strip()
        user_id = self.ui.user_id.text().strip()
        # 查询book_name
        sql = "SELECT book_name FROM admin_borrow WHERE book_id = %s and user_id = %s"
        # 执行 SQL 查询
        value = (bianhao, user_id)
        self.cursor.execute(sql, value)
        reulet = self.cursor.fetchone()
        if reulet is not None:
            self.ui.book_name.setText(str(reulet[0]))
        else:
            self.ui.book_name.setText("无")

    def InsertInto(self):
        text = self.ui.book_name.text()
        if text == "无":
            QMessageBox.warning(self, "提示", "没有图书借阅的记录")
            return
        bianhao = self.ui.bianhao.text().strip()
        user_id = self.ui.user_id.text().strip()
        book_name = self.ui.book_name.text().strip()
        combobox = self.ui.comboBox.currentText().strip()
        phonenumber = self.ui.phone_number.text().strip()

        # 查询book_name
        sql = "SELECT borrow_day, user_name FROM admin_borrow WHERE book_id = %s and user_id = %s"
        # 执行 SQL 查询
        value = (bianhao, user_id)
        self.cursor.execute(sql, value)
        reulet = self.cursor.fetchone()

        # 获取当前时间
        current_time = datetime.now()
        # 将时间格式化为与 SQL 中的 DATETIME 类型相似的格式
        time = current_time.strftime('%Y-%m-%d %H:%M:%S')

        sql = "INSERT INTO admin_return (book_id, book_name, borrow_day, sunhuai, phone_number, user_id, user_name, yymmdd) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        # 执行 SQL 查询
        value = (bianhao, book_name, reulet[0], combobox, phonenumber, user_id, reulet[1], time)
        self.cursor.execute(sql, value)
        self.db.commit()
        if self.db.commit:
            if combobox == "是":
                sql = "INSERT INTO damaged_books (book_id, book_name, borrow_day, sunhuai, phone_number, user_id, user_name, yymmdd) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                # 执行 SQL 查询
                value = (bianhao, book_name, reulet[0], combobox, phonenumber, user_id, reulet[1], time)
                self.cursor.execute(sql, value)
                self.db.commit()
                if self.db.commit:
                    QMessageBox.warning(self, "提示", "录入成功!!!")
                else:
                    QMessageBox.warning(self, "提示", "归还失败!!!")
        else:
            QMessageBox.warning(self, "提示", "归还失败!!!")

        # 删除借阅表的内容
        sql = "DELETE FROM admin_borrow WHERE book_id = %s and user_id = %s"
        value = (bianhao, user_id)
        self.cursor.execute(sql, value)
        self.db.commit()

        # 刷新表格界面
        self.refresh_table()

    def add_data_to_table(self, data):
        # 将数据添加到表格中
        for row_data in data:
            # 获取表格的当前行数
            current_row = self.table_widget.rowCount()

            # 插入新的一行
            self.table_widget.insertRow(current_row)

            # 在新行中添加数据
            for col_num, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.table_widget.setItem(current_row, col_num, item)

    def refresh_table(self):
        # 清空表格
        self.table_widget.clearContents()
        # 删除表格行
        self.table_widget.setRowCount(0)
        # 重新查询数据并添加到表格中
        self.search_thread.start()
