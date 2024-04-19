# -*- coding: utf-8 -*-
# 用户注册界面
from PyQt5 import uic
from PyQt5.QtWidgets import *
from mysql import *
from user.User_interface import *
import re


class RegistrationInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi('./ui_user/Registration_interface.ui')
        self.ui.register_2.clicked.connect(self.registerSuccess)
        self.ui.clean.clicked.connect(self.resetFields)
        # 连接文本框的 textChanged 信号到槽函数
        self.ui.id.textChanged.connect(self.UpdateId)
        self.ui.password_1.textChanged.connect(self.UpdatePassword1)
        self.ui.password_2.textChanged.connect(self.UpdatePassword2)
        self.ui.email_1.textChanged.connect(self.UpdateEmail)

    # 定义按钮点击事件
    def registerSuccess(self):
        # 连接到 MySQL 数据库
        self.db = OpenMySql.open_connection()
        if self.db:
            try:
                # 创建游标对象
                cursor = self.db.cursor()

                # 创建查询语句
                # 检查要插入的 ID 是否已存在
                id_to_check = self.ui.id.text().strip()
                cursor.execute("SELECT id FROM student_account WHERE id = %s", (id_to_check,))
                result = cursor.fetchone()
                cursor.close()

                if result:
                    # 如果 ID 已存在，则显示提示对话框并返回
                    QMessageBox.warning(self, '提示', '账号已存在，请重新输入！')
                    return

                # 创建新的游标对象
                cursor = self.db.cursor()

                # 创建查询语句
                # 检查要插入的 ID 是否在学校人员表中存在
                id_to_check = self.ui.id.text().strip()
                cursor.execute("SELECT id FROM student_information WHERE id = %s", (id_to_check,))
                result = cursor.fetchone()
                if result is not None:
                    try:
                        if (self.ui.password_1.text().strip() == self.ui.password_2.text().strip() is not None):
                            if (len(self.ui.id.text().strip()) == 11):
                                if ((re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', self.ui.email_1.text().strip())) and (self.ui.email_1.text().strip())is not None):
                                    # 执行 SQL 查询命令
                                    sql = "INSERT INTO student_account (id, password, email) VALUES (%s, %s, %s)"
                                    value1 = self.ui.id.text().strip()
                                    value2 = self.ui.password_1.text().strip()
                                    value3 = self.ui.email_1.text().strip()
                                    value = (value1,value2,value3)
                                    cursor.execute(sql, value)

                                    # 提交数据库执行
                                    self.db.commit()

                                    # 关闭游标和数据库连接
                                    cursor.close()
                                    self.db.close()
                                    from user.User_interface import UserLoginWindows  # 因为循环打入的问题使用函数导入模块
                                    registration_dialog = QMessageBox(self)
                                    registration_dialog.setWindowTitle('提示...')
                                    registration_dialog.setText('注册成功!!!')
                                    registration_dialog.addButton('去登录...', QMessageBox.AcceptRole)
                                    registration_dialog.accepted.connect(self.goToLogin)  # 连接accepted信号到goToLogin槽函数
                                    registration_dialog.exec_()
                                    self.UserLogin = UserLoginWindows()
                                    self.UserLogin.ui.show()
                                    self.ui.close()
                                else:
                                    QMessageBox.warning(self, '提示', '邮箱为空或格式不正确')
                            else:
                                QMessageBox.warning(self, '提示', '账号为空或格式不正确')
                        else:
                            QMessageBox.warning(self, '提示', '密码为空或两次输入不同')
                    except Exception as e1:
                        print("An error occurred:", e1)
                else:
                    QMessageBox.warning(self, '提示', '不是本校人员,禁止注册账号!!!')
            except Exception as e2:
                print("An error occurred:", e2)

    def goToLogin(self):
        self.close()  # 关闭当前的注册界面

    def resetFields(self):
        # 清除所有文本框内容
        self.ui.id.clear()
        self.ui.password_1.clear()
        self.ui.password_2.clear()
        self.ui.email_1.clear()
        self.ui.user_number_yesorno.setText('')
        self.ui.password_yesorno.setText('')
        self.ui.password_confirm_yesorno.setText('')
        self.ui.email_2.setText('')

    # 在QLadel显示信息
    def UpdateId(self, text):
        if text.strip():  # 检查文本框是否有内容
            if len(text.strip()) == 11:
                self.ui.user_number_yesorno.setText("账号可用!!")
            else:
                self.ui.user_number_yesorno.setText('账号长度错误')

    def UpdatePassword1(self, text):
        if text.strip():  # 检查文本框是否有内容
            if len(text.strip()) < 3:
                self.ui.password_yesorno.setText('格式错误!!')
            elif len(text.strip()) < 5:
                self.ui.password_yesorno.setText('弱!!!')
            elif 5 <= len(text.strip()) < 8:
                self.ui.password_yesorno.setText('中!!!')
            else:
                self.ui.password_yesorno.setText('强!!!')

    def UpdatePassword2(self, text):
        if text.strip():  # 检查文本框是否有内容
            password_1 = self.ui.password_1.text()
            password_2 = self.ui.password_2.text()
            if password_1.rstrip() == password_2.rstrip():
                self.ui.password_confirm_yesorno.setText("密码正确!!!")
            else:
                self.ui.password_confirm_yesorno.setText("两次密码不同")

    def UpdateEmail(self, text):
        if text.strip():  # 检查文本框是否有内容
            self.email = text.strip()
            # 正则表达式模式匹配电子邮件格式
            pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if re.match(pattern, self.email):
                self.ui.email_2.setText('邮箱正确!!!')
            else:
                self.ui.email_2.setText('邮箱格式错误')


