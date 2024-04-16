# -*- coding: utf-8 -*-
from PyQt5 import uic
from PyQt5.QtWidgets import *

from mysql import OpenMySql


class AdministratorLogin(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi('./ui_administrator/administrator_interface.ui')
        self.ui.user_button.clicked.connect(self.login)

    # 定义按钮点击事件
    def login(self):
        # 连接到 MySQL 数据库
        self.db = OpenMySql.open_connection()
        if self.db:
            try:
                # 创建游标对象
                cursor = self.db.cursor()

                # 创建查询语句
                # 检查要登录的 ID 是否存在
                id_to_check = self.ui.user_number_text.text().strip()
                cursor.execute("SELECT id FROM administrator WHERE id = %s", (id_to_check,))
                result = cursor.fetchone()
                cursor.close()

                if result:
                    password = self.ui.password_2.text().strip()

                    # 创建一个新的游标
                    cursor = self.db.cursor()

                    # 创建查询语句
                    # 检查要登录的 ID 对应的密码是否与输入密码相同
                    id_to_check = self.ui.user_number_text.text().strip()
                    cursor.execute("SELECT password FROM administrator WHERE id = %s", (id_to_check,))
                    sqlpassword = cursor.fetchone()  # 获取的是元组不是字符串

                    # 关闭游标和数据库连接
                    cursor.close()
                    self.db.close()

                    if sqlpassword[0] == password:
                        # 打开借阅管理界面
                        from administration.Borrow import Borrow
                        self.Borrow = Borrow()
                        self.Borrow.ui.show()
                        self.ui.close()
                        QMessageBox.warning(self, '提示', '登录成功!!!')
                    else:
                        QMessageBox.warning(self, '提示', '密码为空或不正确!!!')
                        self.ui.password_2.clear()
                else:
                    QMessageBox.warning(self, '提示', '账号为空或不存在!!!')
                    self.ui.user_number_text.clear()
                    self.ui.password_2.clear()
            except Exception as e:
                print("An error occurred:", e)
        else:
            QMessageBox.warning(self, '提示', '数据库连接失败!!!')

