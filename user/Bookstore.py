# -*- coding:utf-8 -*-
# 书城
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from mysql import OpenMySql


class SearchThread1(QThread):
    # 根据搜索框进行搜索
    search_finished = pyqtSignal(object)  # 定义一个信号，在搜索完成时发射

    def __init__(self, db, cursor, name):
        super().__init__()
        self.name = name
        self.db = db
        self.cursor = cursor

    def run(self):
        # 查询数据库获取数据
        query = "SELECT * FROM bookstore WHERE book_name LIKE %s"
        self.cursor.execute(query, ('%' + self.name + '%',))
        data = self.cursor.fetchall()
        self.search_finished.emit(data)  # 发射信号，传递数据


class SearchThread2(QThread):
    # 根据combobox进行搜索
    search_finished = pyqtSignal(object)  # 定义一个信号，在搜索完成时发射

    def __init__(self, db, cursor, leibie):
        super().__init__()
        self.leibie = leibie
        self.db = db
        self.cursor = cursor

    def run(self):
        # 查询数据库获取数据
        query = "SELECT * FROM bookstore WHERE leibie_tow = %s"
        self.cursor.execute(query, (self.leibie,))
        data = self.cursor.fetchall()
        self.search_finished.emit(data)  # 发射信号，传递数据


class Bookstore(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi('./ui_user/Bookstore.ui')
        self.ui.tuijian_button.clicked.connect(self.OpenRecommended_books)
        self.ui.collect.clicked.connect(self.Opencollect)
        self.ui.reserve.clicked.connect(self.Openreserve)
        self.ui.report_loss.clicked.connect(self.OpenReportLoss)
        self.ui.personal_information.clicked.connect(self.OpenPersonalInformation)
        self.ui.pushButton_1.clicked.connect(self.ComboBoxSearch)
        self.ui.pushButton_2.clicked.connect(self.LineEditSearch)

        self.ui.comboBox.currentIndexChanged.connect(self.updateComboBox2)

    # 定义按钮点击事件
    def OpenRecommended_books(self):
        from user.Recommended_books import RecommendedBooks
        self.RecommendedBooks = RecommendedBooks()
        self.RecommendedBooks.ui.show()
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

    # 定义第一个ComboBox的索引更改事件处理函数
    def updateComboBox2(self, index):
        # 清除第二个ComboBox中的所有项
        self.ui.comboBox_2.clear()

        # 根据第一个ComboBox的索引确定要显示的内容
        if index == 0:  # 假设第一个ComboBox中的索引从0开始
            items = ["文学小说", "艺术与设计", "语言与文学", "电影与媒体"]  # 根据索引0显示的内容
        elif index == 1:
            items = ["历史与地理",]  # 根据索引1显示的内容
        elif index == 2:
            items = ["社会科学", "商业与管理", "法律与政治"]  # 根据索引2显示的内容
        elif index == 3:
            items = ["自然科学", "科普读物",]  # 根据索引3显示的内容
        elif index == 4:
            items = ["技术与工程",]  # 根据索引4显示的内容
        elif index == 5:
            items = ["健康与心理",]  # 根据索引5显示的内容
        elif index == 6:
            items = ["教育与教材",]  # 根据索引6显示的内容
        elif index == 7:
            items = ["宗教与哲学",]  # 根据索引7显示的内容
        elif index == 8:
            items = ["参考资料与工具书",]  # 根据索引8显示的内容
        elif index == 9:
            items = ["医学与健康",]  # 根据索引9显示的内容
        elif index == 10:
            items = ["农业与环境",]  # 根据索引10显示的内容
        elif index == 11:
            items = ["科学与技术",]  # 根据索引11显示的内容
        elif index == 12:
            items = ["旅行与地理",]  # 根据索引12显示的内容
        elif index == 13:
            items = ["食品与饮食",]  # 根据索引13显示的内容
        elif index == 14:
            items = ["体育与运动",]  # 根据索引14显示的内容
        elif index == 15:
            items = ["家庭与生活",]  # 根据索引15显示的内容
        elif index == 16:
            items = ["心灵与成长",]  # 根据索引16显示的内容
        else:
            items = []  # 如果索引不匹配任何条件，则显示空内容

        # 将新的内容添加到第二个ComboBox中
        self.ui.comboBox_2.addItems(items)

    def ComboBoxSearch(self):
        # 通过combobox进行搜索
        self.db = OpenMySql.open_connection()
        self.cursor = self.db.cursor()

        # 判断combobox中的内容
        leibie = self.ui.comboBox_2.currentText()

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
        self.table_widget.setColumnCount(8)  # 有8列
        column_labels = ["书名", "作者", "介绍", "第一大类", "第二大类", "图书编号", "收藏", "预约"]
        self.table_widget.setHorizontalHeaderLabels(column_labels)

        # 创建并启动线程执行查询
        self.search_thread = SearchThread2(self.db, self.cursor, leibie)
        self.search_thread.search_finished.connect(self.add_data_to_table)  # 连接信号到槽函数
        self.search_thread.start()

    def LineEditSearch(self):
        self.db = OpenMySql.open_connection()
        self.cursor = self.db.cursor()

        # 获取搜索框的内容
        name = self.ui.lineEdit.text().strip()

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
        self.table_widget.setColumnCount(8)  # 有8列
        column_labels = ["书名", "作者", "介绍", "第一大类", "第二大类", "图书编号", "收藏", "预约"]
        self.table_widget.setHorizontalHeaderLabels(column_labels)

        # 创建并启动线程执行查询
        self.search_thread = SearchThread1(self.db, self.cursor, name)
        self.search_thread.search_finished.connect(self.add_data_to_table)  # 连接信号到槽函数
        self.search_thread.start()

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

        # 添加收藏按钮
        btn = QPushButton("收藏")
        btn.clicked.connect(lambda state, row=current_row: self.collect_button_clicked_btn(row))
        self.table_widget.setCellWidget(current_row, 6, btn)  # 最后一列

        # 添加收藏按钮
        reserve = QPushButton("预约")
        reserve.clicked.connect(lambda state, row=current_row: self.collect_button_clicked_reserve(row))
        self.table_widget.setCellWidget(current_row, 7, reserve)  # 最后一列

    def collect_button_clicked_reserve(self, row):
        # 获取要预约的行的数据
        num_cols = self.table_widget.columnCount()
        items = []
        for col in range(num_cols):
            item = self.table_widget.item(row, col)
            if item is not None:
                items.append(item.text())

        try:
            # 创建一个游标并执行查询
            self.cursor = self.db.cursor()
            self.cursor.execute("SELECT id FROM dl_user")
            # 检索查询结果
            result = self.cursor.fetchone()
            dl_id = result[0]

            # 检索预约图书是否存在
            self.cursor.execute("SELECT COUNT(*) FROM book_reserve_table WHERE id = %s AND book_name = %s",
                                (dl_id, items[0]))
            result = self.cursor.fetchone()
            count = result[0]
            if count > 0:
                QMessageBox.warning(self, '提示', '已预约!!!')
            else:
                # 插入数据到预约列表数据库中
                sql = "INSERT INTO book_reserve_table (id, book_name, book_zuozhe, book_jieshao, leibie_one, leibie_tow, book_bianhao) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                self.cursor.execute(sql, (dl_id, *items,))
                self.db.commit()  # 提交事务
                QMessageBox.warning(self, "提示", "预约成功!!!")
        except Exception as e:
            print("Error:", e)

    def collect_button_clicked_btn(self, row):
        # 获取要收藏的行的数据
        num_cols = self.table_widget.columnCount()
        items = []
        for col in range(num_cols):
            item = self.table_widget.item(row, col)
            if item is not None:
                items.append(item.text())

        try:
            # 创建一个游标并执行查询
            self.cursor = self.db.cursor()
            self.cursor.execute("SELECT id FROM dl_user")
            # 检索查询结果
            result = self.cursor.fetchone()
            dl_id = result[0]

            # 检索收藏图书是否存在
            self.cursor.execute("SELECT COUNT(*) FROM book_collect_table WHERE id = %s AND book_name = %s",
                                (dl_id, items[0]))
            result = self.cursor.fetchone()
            count = result[0]
            if count > 0:
                QMessageBox.warning(self, '提示', '已在收藏目录中!!!')
            else:
                # 插入数据到收藏列表数据库中
                sql = "INSERT INTO book_collect_table (id, book_name, book_zuozhe, book_jieshao, leibie_one, leibie_tow, book_bianhao) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                self.cursor.execute(sql, (dl_id, *items,))
                self.db.commit()  # 提交事务
                QMessageBox.warning(self, "提示", "收藏成功!!!")
        except Exception as e:
            print("Error:", e)

    # 使用close函数关闭界面的时候,调用函数,关闭数据库
    def closeEvent(self, event):
        if self.cursor:
            self.cursor.close()
        if self.db:
            self.db.close()
        # 处理 Qt 事件队列，确保界面关闭前所有事件都被处理完毕
        QCoreApplication.processEvents()
