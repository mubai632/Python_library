# -*- coding:utf-8 -*-
# 预约书籍
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from mysql import OpenMySql

class SearchThread(QThread):
    search_finished = pyqtSignal(object)  # 定义一个信号，在搜索完成时发射

    def __init__(self, db, cursor, id):
        super().__init__()
        self.id = id
        self.db = db
        self.cursor = cursor

    def run(self):
        # 查询数据库获取数据
        query = "SELECT * FROM book_reserve_table WHERE id = %s"
        self.cursor.execute(query, (self.id,))
        data = self.cursor.fetchall()
        self.search_finished.emit(data)  # 发射信号，传递数据


class reserve(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi('./ui_user/reserve_Null.ui')
        # 连接到 MySQL 数据库
        self.db = OpenMySql.open_connection()
        if self.db:
            try:
                # 创建一个游标并执行查询
                self.cursor = self.db.cursor()
                self.cursor.execute("SELECT id FROM dl_user")
                # 检索查询结果
                result = self.cursor.fetchone()
                dl_id = result[0]

                # 创建查询语句
                self.cursor.execute("SELECT COUNT(*) FROM book_reserve_table WHERE id = %s",
                                    (dl_id,))
                result = self.cursor.fetchone()
                if result[0] != 0:
                    self.ui = uic.loadUi('./ui_user/reserve.ui')

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
                    self.table_widget.setColumnCount(8)  # 有8列
                    column_labels = ["用户id", "书名", "作者", "介绍", "第一大类", "第二大类", "图书编号", "删除"]
                    self.table_widget.setHorizontalHeaderLabels(column_labels)

                    # 创建并启动线程执行查询
                    self.search_thread = SearchThread(self.db, self.cursor, dl_id)
                    self.search_thread.search_finished.connect(self.add_data_to_table)  # 连接信号到槽函数
                    self.search_thread.start()
            except Exception as e:
                print("An error occurred:", e)

        self.ui.tuijian_button.clicked.connect(self.OpenRecommended_books)
        self.ui.book_button.clicked.connect(self.OpenBookstore)
        self.ui.collect.clicked.connect(self.Opencollect)
        self.ui.report_loss.clicked.connect(self.OpenReportLoss)
        self.ui.personal_information.clicked.connect(self.OpenPersonalInformation)

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

    def Opencollect(self):
        from user.collect import collect
        self.collect = collect()
        self.collect.ui.show()
        self.ui.close()

    def OpenReportLoss(self):
        from user.Report_loss import ReportLoss
        self.ReportLoss = ReportLoss()
        self.ReportLoss.ui.show()
        self.ui.close()
        # 如果存在旧的连接和游标，则先关闭它们
        self.close_old_connection_and_cursor()


    def OpenPersonalInformation(self):
        from user.personal_information import PersonalInformation
        self.PersonalInformation = PersonalInformation()
        self.PersonalInformation.ui.show()
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

        # 添加删除按钮
        book_delete = QPushButton("删除")
        book_delete.clicked.connect(lambda state, row=current_row: self.collect_button_clicked_book_delete(row))
        self.table_widget.setCellWidget(current_row, 7, book_delete)  # 最后一列

    def collect_button_clicked_book_delete(self, row):
        # 获取要删除的行的数据
        num_cols = self.table_widget.columnCount()
        items = []
        for col in range(num_cols):
            item = self.table_widget.item(row, col)
            if item is not None:
                items.append(item.text())
        try:
            # 创建一个游标并执行查询
            self.cursor = self.db.cursor()

            # 检索收藏图书是否存在
            self.cursor.execute("SELECT COUNT(*) FROM book_reserve_table WHERE id = %s AND book_name = %s",
                                (items[0], items[1]))
            result = self.cursor.fetchone()
            count = result[0]
            if count == 1:
                # 删除数据
                sql = "DELETE FROM book_reserve_table WHERE id = %s AND book_name = %s"
                self.cursor.execute(sql, (items[0], items[1],))
                self.db.commit()  # 提交事务
                QMessageBox.warning(self, "提示", "删除成功!!!")

                # 删除成功后重新加载数据到表格
                self.reload_table_data()  # 假设有一个函数用来重新加载数据
        except Exception as e:
            print("Error:", e)

    def reload_table_data(self):
        # 清空表格
        self.table_widget.clear()

        # 重新设置表格的列数
        self.table_widget.setColumnCount(7)

        try:
            # 创建一个游标并执行查询
            self.cursor = self.db.cursor()

            # 执行查询操作（假设这里是从数据库中获取数据的操作）
            self.cursor.execute("SELECT * FROM book_reserve_table")

            # 获取查询结果
            results = self.cursor.fetchall()

            # 将查询结果添加到表格中
            self.table_widget.setRowCount(len(results))
            for row_num, row_data in enumerate(results):
                for col_num, cell_data in enumerate(row_data):
                    item = QTableWidgetItem(str(cell_data))
                    self.table_widget.setItem(row_num, col_num, item)

                # 添加删除按钮到每一行的最后一列
                delete_button = QPushButton("删除")
                delete_button.clicked.connect(
                    lambda state, row=row_num: self.collect_button_clicked_book_delete(row))
                self.table_widget.setCellWidget(row_num, self.table_widget.columnCount() - 1, delete_button)

        except Exception as e:
            print("Error:", e)

    # 使用close函数关闭界面的时候,调用函数,关闭数据库
    def close_old_connection_and_cursor(self):
        if self.cursor:
            self.cursor.close()
        if self.db:
            self.db.close()
        # 处理 Qt 事件队列，确保界面关闭前所有事件都被处理完毕
        QCoreApplication.processEvents()