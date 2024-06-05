# -*- coding: utf-8 -*-
# 用户界面
from PyQt5 import uic
from PyQt5.QtWidgets import *

from mysql import OpenMySql
# 自建模块
from user.Recommended_books import RecommendedBooks
from user.Registration_interface import RegistrationInterface

class UserLoginWindows(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi('./ui_user/user_interface.ui')
        self.ui.register_2.clicked.connect(self.OpenRegistrationInterface)
        self.ui.user_button.clicked.connect(self.OpenRecommended_books)

    # 定义按钮点击事件
    def OpenRegistrationInterface(self):
        # 打开注册界面
        self.RegistrationInterface = RegistrationInterface()
        self.RegistrationInterface.ui.show()
        self.ui.close()

    def OpenRecommended_books(self):
        if len(self.ui.user_number_text.text()) == 11:
            # 连接到 MySQL 数据库
            self.db = OpenMySql.open_connection()
            if self.db:
                try:
                    # 创建游标对象
                    cursor = self.db.cursor()

                    # 创建查询语句
                    # 检查要登录的 ID 是否存在
                    id_to_check = self.ui.user_number_text.text().strip()
                    cursor.execute("SELECT id FROM student_account WHERE id = %s", (id_to_check,))
                    result = cursor.fetchone()
                    cursor.close()

                    if result:
                        password = self.ui.password_2.text().strip()

                        # 创建一个新的游标
                        cursor = self.db.cursor()

                        # 创建查询语句
                        # 检查要登录的 ID 对应的密码是否与输入密码相同
                        id_to_check = self.ui.user_number_text.text().strip()
                        cursor.execute("SELECT password FROM student_account WHERE id = %s", (id_to_check,))
                        sqlpassword = cursor.fetchone()  # 获取的是元组不是字符串

                        if sqlpassword[0] == password:
                            sql = "INSERT INTO dl_user (id) VALUES (%s)"
                            value = self.ui.user_number_text.text().strip()
                            cursor.execute(sql, value)
                            try:
                                self.db.commit()
                            except Exception as e:
                                print("提交失败:", e)

                            try:
                                self.RecommendedBooks = RecommendedBooks()
                                self.RecommendedBooks.ui.show()
                                self.ui.close()
                                sql = "SELECT neirong FROM gonggao"
                                cursor.execute(sql)
                                result = cursor.fetchone()
                                QMessageBox.warning(self, '公告', result[0])
                                # 关闭数据库和游标连接
                                cursor.close()
                                self.db.close()
                            except Exception as e2:
                                print(e2)
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
                QMessageBox.warning(self, '提示', '数据库未连接!!!')
        else:
            QMessageBox.warning(self, '提示', '不是11位账号!!!')
            self.ui.user_number_text.clear()
            self.ui.password_2.clear()



