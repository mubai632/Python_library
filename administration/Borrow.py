# -*- coding: utf-8 -*-
# 借阅书籍
from PyQt5 import uic
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import *
from datetime import datetime
from mysql import OpenMySql


class SearchThread(QThread):
    search_finished = pyqtSignal(object)  # 定义一个信号，在搜索完成时发射

    def __init__(self, db, cursor):
        super().__init__()
        self.db = db
        self.cursor = cursor

    def run(self):
        # 查询数据库获取数据
        query = "SELECT * FROM admin_borrow ORDER BY yymmdd DESC"
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        self.search_finished.emit(data)  # 发射信号，传递数据


class Borrow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.book_name = ""  # 初始化 self.book_name
        self.ui = uic.loadUi('./ui_administrator/Borrow.ui')
        self.ui.Return.clicked.connect(self.OpenReturn)
        self.ui.book_information.clicked.connect(self.OpenBookInformation)
        self.ui.reserve.clicked.connect(self.OpenReserve)
        self.ui.user_info.clicked.connect(self.OpenUserInfo)
        self.ui.setting.clicked.connect(self.OpenSetting)

        self.ui.pushButton.clicked.connect(self.InsterInto)
        self.ui.number.focusOutEvent = self.handle_focus_out_event  # 将文本框的焦点离开事件连接到自定义方法

        self.db = OpenMySql.open_connection()
        self.cursor = self.db.cursor()
        layout = self.ui.scrollAreaWidgetContents.layout()
        # 创建表格部件
        self.table_widget = QTableWidget()
        layout.addWidget(self.table_widget)  # 添加表格到布局中
        # 设置表格的列数和对应的标题文字
        self.table_widget.setColumnCount(7)  # 有7列
        column_labels = ["书籍编号", "书名", "借阅期限", "用户id", "用户姓名", "手机号", "借阅时间"]
        self.table_widget.setHorizontalHeaderLabels(column_labels)

        # 创建并启动线程执行查询
        self.search_thread = SearchThread(self.db, self.cursor)
        self.search_thread.search_finished.connect(self.add_data_to_table)  # 连接信号到槽函数
        self.search_thread.start()

    # 定义按钮点击事件
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

    def InsterInto(self):
        bianhao = self.ui.number.text()
        book_name = self.ui.book_name.text()
        borrow_day = self.ui.time.currentText()
        user_id = self.ui.ID.text()
        name = self.ui.name.text()
        numberphone = self.ui.numberphone.text()
        # 获取当前时间
        current_time = datetime.now()
        # 将时间格式化为与 SQL 中的 DATETIME 类型相似的格式
        time = current_time.strftime('%Y-%m-%d %H:%M:%S')
        sql = "INSERT INTO admin_borrow (book_id, book_name, borrow_day, user_id, user_name, phone_number, yymmdd) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        # 执行 SQL 查询
        value = (bianhao, book_name, borrow_day, user_id, name, numberphone, time)
        self.cursor.execute(sql, value)
        self.db.commit()
        QMessageBox.warning(self, "提示", "录入成功!!!")

    def UpdateBookName(self):
        query = "SELECT book_bianhao.id, bookstore.book_bianhao FROM bookstore, book_bianhao WHERE bookstore.leibie_tow = book_bianhao.leibie_tow"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        for row in result:
            bianhao = self.ui.number.text().strip()
            if bianhao == (row[0] + "-" + row[1]):
                query = "SELECT book_name FROM bookstore WHERE book_bianhao = %s"
                self.cursor.execute(query, (row[1]), )
                self.book_name = self.cursor.fetchall()
                self.ui.book_name.setText(str(self.book_name[0][0]))

    def handle_focus_out_event(self, event):
        # 当焦点离开文本框时执行比对操作
        self.UpdateBookName()
        event.accept()

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

    # 使用close函数关闭界面的时候,调用函数,关闭数据库
    def closeEvent(self, event):
        # 关闭数据库连接
        if self.cursor:
            self.cursor.close()
        if self.db:
            self.db.close()
        # 接受关闭事件
        event.accept()
