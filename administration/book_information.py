# -*- coding: utf-8 -*-
# 书籍信息
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


class BookInformation(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi('./ui_administrator/book_information.ui')
        self.ui.borrow.clicked.connect(self.OpenBorrow)
        self.ui.Return.clicked.connect(self.OpenReturn)
        self.ui.reserve.clicked.connect(self.OpenReserve)
        self.ui.user_info.clicked.connect(self.OpenUserInfo)
        self.ui.setting.clicked.connect(self.OpenSetting)

        self.ui.pushButton.clicked.connect(self.LineEdit)
        self.ui.add_book.clicked.connect(self.NewWindowAddBook)
        self.ui.delete_book.clicked.connect(self.deleteSelectedRows)
        self.ui.revise.clicked.connect(self.updateBookInformation)

        self.db = OpenMySql.open_connection()
        self.cursor = self.db.cursor()

        # 获取搜索框的内容
        name = self.ui.lineEdit.text().strip()

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
        self.table_widget.setColumnCount(7)  # 有7列
        column_labels = ["书名", "作者", "介绍", "第一大类", "第二大类", "图书编号", "数量"]
        self.table_widget.setHorizontalHeaderLabels(column_labels)

        # 创建并启动线程执行查询
        self.search_thread = SearchThread1(self.db, self.cursor, name)
        self.search_thread.search_finished.connect(self.add_data_to_table)  # 连接信号到槽函数
        self.search_thread.start()

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

    def LineEdit(self):
        self.db = OpenMySql.open_connection()
        self.cursor = self.db.cursor()

        # 获取搜索框的内容
        name = self.ui.lineEdit.text().strip()

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
        self.table_widget.setColumnCount(7)  # 有7列
        column_labels = ["书名", "作者", "介绍", "第一大类", "第二大类", "图书编号", "数量"]
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

        # # 添加收藏按钮
        # btn = QPushButton("收藏")
        # btn.clicked.connect(lambda state, row=current_row: self.collect_button_clicked_btn(row))
        # self.table_widget.setCellWidget(current_row, 6, btn)  # 最后一列
        #
        # # 添加收藏按钮
        # reserve = QPushButton("预约")
        # reserve.clicked.connect(lambda state, row=current_row: self.collect_button_clicked_reserve(row))
        # self.table_widget.setCellWidget(current_row, 7, reserve)  # 最后一列

    def NewWindowAddBook(self):
        # 定义存储标签的列表
        self.labels = []
        # 存储lineedit和combobox
        self.input_widgets = []

        # 创建新窗口
        self.new_window = QWidget()
        self.new_window.setWindowTitle("添加书籍信息")

        # 创建表格布局
        self.grid_layout = QGridLayout(self.new_window)

        # 添加行和列
        labels = ["书名", "作者", "介绍", "第一大类", "第二大类", "图书编号", "数量"]
        for row, label_name in enumerate(labels):  # 遍历标签和行索引
            label = QLabel(label_name + ": ")  # 创建 QLabel，并设置名称
            self.grid_layout.addWidget(label, row, 0)  # 将 QLabel 添加到第 row 行第一列
            if label_name == "第一大类":  # 如果是指定的标签
                combo_box = QComboBox()
                combo_box.addItems(["文学与艺术", "历史与地理", "社会科学", "自然科学", "技术与工程", "健康与心理", "教育与教材", "宗教与哲学", "参考资料与工具书", "医学与健康", "农业与环境", "科学与技术", "旅行与地理", "食品与饮食", "体育与运动", "家庭与生活", "心灵与成长"])
                combo_box.setCurrentIndex(-1)  # 设置默认索引为 -1，即没有选项被选择
                combo_box.currentIndexChanged.connect(self.updateSecondCategory)
                self.grid_layout.addWidget(combo_box, row, 1)
                self.input_widgets.append(combo_box)
            elif label_name == "第二大类":
                combo_box = QComboBox()
                self.grid_layout.addWidget(combo_box, row, 1)
                self.input_widgets.append(combo_box)
            else:
                line_edit = QLineEdit()  # 创建 QLineEdit
                self.grid_layout.addWidget(line_edit, row, 1)  # 将 QLineEdit 添加到第 row 行第二列
                self.input_widgets.append(line_edit)  # 将 QLineEdit 添加到列表
            # 将标签添加到列表
            self.labels.append(label)


        # 添加确认和清空按钮
        self.clear_button = QPushButton("清空")
        self.confirm_button = QPushButton("确认")
        self.grid_layout.addWidget(self.clear_button, 7, 0)  # 第8行第一列
        self.grid_layout.addWidget(self.confirm_button, 7, 1)  # 第8行第二列

        self.clear_button.clicked.connect(self.ClearLineEditNewWindow)
        self.confirm_button.clicked.connect(self.InsertIntoBookInformationForMySQL)
        # 显示新窗口
        self.new_window.show()

    @pyqtSlot(int)
    def updateSecondCategory(self):
        # 清空第二大类组合框中的当前项目
        second_category_combo_box = self.input_widgets[4]
        second_category_combo_box.clear()

        # 获取第一大类组合框中的选定项目
        first_category_combo_box = self.input_widgets[3]
        selected_item = first_category_combo_box.currentText()

        # 根据选定项目更新第二大类组合框
        if selected_item == "文学与艺术":
            second_category_combo_box.addItems(["文学小说", "艺术与设计", "语言与文学", "电影与媒体"])
        elif selected_item == "历史与地理":
            second_category_combo_box.addItems(["历史与地理"])
        elif selected_item == "社会科学":
            second_category_combo_box.addItems(["社会科学", "商业与管理", "法律与政治"])
        elif selected_item == "自然科学":
            second_category_combo_box.addItems(["自然科学", "科普读物"])
        elif selected_item == "技术与工程":
            second_category_combo_box.addItems(["技术与工程"])
        elif selected_item == "健康与心理":
            second_category_combo_box.addItems(["健康与心理"])
        elif selected_item == "教育与教材":
            second_category_combo_box.addItems(["教育与教材"])
        elif selected_item == "宗教与哲学":
            second_category_combo_box.addItems(["宗教与哲学"])
        elif selected_item == "参考资料与工具书":
            second_category_combo_box.addItems(["参考资料与工具书"])
        elif selected_item == "医学与健康":
            second_category_combo_box.addItems(["医学与健康"])
        elif selected_item == "农业与环境":
            second_category_combo_box.addItems(["农业与环境"])
        elif selected_item == "科学与技术":
            second_category_combo_box.addItems(["科学与技术"])
        elif selected_item == "旅行与地理":
            second_category_combo_box.addItems(["旅行与地理"])
        elif selected_item == "食品与饮食":
            second_category_combo_box.addItems(["食品与饮食"])
        elif selected_item == "体育与运动":
            second_category_combo_box.addItems(["体育与运动"])
        elif selected_item == "家庭与生活":
            second_category_combo_box.addItems(["家庭与生活"])
        elif selected_item == "心灵与成长":
            second_category_combo_box.addItems(["心灵与成长"])

    def ClearLineEditNewWindow(self):
        # 清除所有输入框和组合框的内容
        for widget in self.input_widgets:
            if isinstance(widget, QLineEdit):
                widget.clear()
            elif isinstance(widget, QComboBox):
                widget.setCurrentIndex(-1)  # 设置为空

    def InsertIntoBookInformationForMySQL(self):
        lineEdit = []
        db = OpenMySql.open_connection()
        cursor = db.cursor()
        for widget in self.input_widgets:
            if isinstance(widget, QLineEdit):
                lineEdit.append(widget.text().strip())
            elif isinstance(widget, QComboBox):
                lineEdit.append(widget.currentText().strip())
        print(lineEdit)
        sql = "INSERT INTO bookstore (book_name, book_zuozhe, book_jieshao, leibie_one, leibie_tow, book_bianhao, shuliang) VALUE (%s, %s, %s, %s, %s, %s, %s)"
        try:
            cursor.execute(sql, lineEdit)
            db.commit()  # 提交事务
            QMessageBox.warning(self, "提示", "添加成功")
        except Exception as e:
            QMessageBox.warning(self, "错误", f"添加失败：{str(e)}")
        finally:
            cursor.close()  # 关闭游标
            db.close()  # 关闭数据库连接

    def deleteSelectedRows(self):
        selected_rows = []

        # 获取选中的行
        selected_items = self.table_widget.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "提示", "没有选中要删除的行!!!")
        else:
            for item in selected_items:
                row = item.row()
                if row not in selected_rows:
                    selected_rows.append(row)

            # 删除数据库中的行
            self.db = OpenMySql.open_connection()
            self.cursor = self.db.cursor()
            for row in selected_rows:
                # 获取表格中的数据
                row_data = []
                for column in range(self.table_widget.columnCount()):
                    item = self.table_widget.item(row, column)
                    if item is not None:
                        row_data.append(item.text())
                    else:
                        row_data.append(None)

                # 从数据库中删除相应的行
                # 请根据您的数据库模式和删除逻辑修改以下代码
                sql = "DELETE FROM bookstore WHERE leibie_tow = %s AND book_bianhao = %s"  # 假设每行有一个唯一的 id
                try:
                    self.cursor.execute(sql, (row_data[4], row_data[5],))  # 假设 id 在数据中的索引为 0
                    self.db.commit()
                    QMessageBox.warning(self, "提示", "删除成功")
                except Exception as e:
                    self.db.rollback()
                    print("删除失败：", str(e))

        # 删除表格中的行
        for row in selected_rows:
            self.table_widget.removeRow(row)

        # 关闭数据库连接
        self.cursor.close()
        self.db.close()

    def updateBookInformation(self):
        selected_rows_data = []

        # 获取选中的行
        selected_items = self.table_widget.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "提示", "没有选中要修改的行!!!")
        else:
            # 获取选中行的数据
            for item in selected_items:
                row = item.row()
                row_data = []
                for column in range(self.table_widget.columnCount()):
                    item = self.table_widget.item(row, column)
                    if item is not None:
                        row_data.append(item.text())
                    else:
                        row_data.append(None)
                selected_rows_data.append(row_data)

            # 调用新窗口并传递选中行的数据
            self.NewWindowForUpdateBookInformation(selected_rows_data)

    def NewWindowForUpdateBookInformation(self, selected_rows_data):
        # 定义存储标签的列表
        self.labels = []
        # 存储lineedit和combobox
        self.input_widgets = []
        # 创建新窗口
        self.new_window = QWidget()
        self.new_window.setWindowTitle("修改书籍信息")

        # 创建表格布局
        self.grid_layout = QGridLayout(self.new_window)

        # 添加行和列
        labels = ["书名", "作者", "介绍", "第一大类", "第二大类", "图书编号", "数量"]
        for row, label_name in enumerate(labels):  # 遍历标签和行索引
            label = QLabel(label_name + ": ")  # 创建 QLabel，并设置名称
            self.grid_layout.addWidget(label, row, 0)  # 将 QLabel 添加到第 row 行第一列
            if label_name == "图书编号":  # 如果是指定的标签
                line_edit = QLineEdit()  # 创建 QLineEdit
                line_edit.setEnabled(False)  # 设置为只读
                self.grid_layout.addWidget(line_edit, row, 1)  # 将 QLineEdit 添加到第 row 行第二列
                self.input_widgets.append(line_edit)
            elif label_name == "第一大类":
                combo_box = QComboBox()
                combo_box.addItems(
                    ["文学与艺术", "历史与地理", "社会科学", "自然科学", "技术与工程", "健康与心理", "教育与教材",
                     "宗教与哲学", "参考资料与工具书", "医学与健康", "农业与环境", "科学与技术", "旅行与地理",
                     "食品与饮食", "体育与运动", "家庭与生活", "心灵与成长"])
                combo_box.setCurrentIndex(-1)  # 设置默认索引为 -1，即没有选项被选择
                combo_box.currentIndexChanged.connect(self.updateSecondCategory)
                self.grid_layout.addWidget(combo_box, row, 1)
                self.input_widgets.append(combo_box)
            elif label_name == "第二大类":
                combo_box = QComboBox()
                self.grid_layout.addWidget(combo_box, row, 1)
                self.input_widgets.append(combo_box)
            else:
                line_edit = QLineEdit()  # 创建 QLineEdit
                self.grid_layout.addWidget(line_edit, row, 1)  # 将 QLineEdit 添加到第 row 行第二列
                self.input_widgets.append(line_edit)

        # 填充选中行的数据到输入字段中
        for index, data in enumerate(selected_rows_data):
            for col, value in enumerate(data):
                if labels[col] == "第一大类":
                    combo_box = self.input_widgets[3]
                    combo_box.setCurrentText(value)
                elif labels[col] == "第二大类":
                    combo_box = self.input_widgets[4]
                    combo_box.setCurrentText(value)
                else:
                    line_edit = self.input_widgets[col]
                    line_edit.setText(value)

        # 添加确认和清空按钮
        self.clear_button = QPushButton("清空")
        self.confirm_button = QPushButton("确认")
        self.grid_layout.addWidget(self.clear_button, 7, 0)  # 第8行第一列
        self.grid_layout.addWidget(self.confirm_button, 7, 1)  # 第8行第二列

        self.clear_button.clicked.connect(self.ClearLineEditNewWindow)
        self.confirm_button.clicked.connect(self.UpdateBookInformationForMySQL)

        # 显示新窗口
        self.new_window.show()

    def UpdateBookInformationForMySQL(self):
        lineEdit = []
        db = OpenMySql.open_connection()
        cursor = db.cursor()
        for widget in self.input_widgets:
            if isinstance(widget, QLineEdit):
                lineEdit.append(widget.text().strip())
            elif isinstance(widget, QComboBox):
                lineEdit.append(widget.currentText().strip())
        sql = "UPDATE bookstore SET book_name = %s, book_zuozhe = %s, book_jieshao = %s, leibie_one = %s, leibie_tow = %s, book_bianhao = %s, shuliang = %s WHERE book_bianhao = %s"
        value = (*lineEdit, lineEdit[-2],)
        try:
            cursor.execute(sql, value)
            db.commit()  # 提交事务
            QMessageBox.warning(self, "提示", "修改成功")
            self.new_window.close()  # 关闭窗口
            self.db = OpenMySql.open_connection()
            self.cursor = self.db.cursor()

            # 获取搜索框的内容
            name = self.ui.lineEdit.text().strip()

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
            self.table_widget.setColumnCount(7)  # 有7列
            column_labels = ["书名", "作者", "介绍", "第一大类", "第二大类", "图书编号", "数量"]
            self.table_widget.setHorizontalHeaderLabels(column_labels)

            # 创建并启动线程执行查询
            self.search_thread = SearchThread1(self.db, self.cursor, name)
            self.search_thread.search_finished.connect(self.add_data_to_table)  # 连接信号到槽函数
            self.search_thread.start()
        except Exception as e:
            QMessageBox.warning(self, "错误", f"修改失败：{str(e)}")
        finally:
            cursor.close()  # 关闭游标
            db.close()  # 关闭数据库连接

