# -*- coding: utf-8 -*-
# 设置
from PyQt5 import uic
from PyQt5.QtWidgets import *

from mysql import OpenMySql


class Setting(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi('./ui_administrator/setting.ui')
        self.db = OpenMySql.open_connection()
        self.cursor = self.db.cursor()
        self.ui.borrow.clicked.connect(self.OpenBorrow)
        self.ui.Return.clicked.connect(self.OpenReturn)
        self.ui.book_information.clicked.connect(self.OpenBookInformation)
        self.ui.reserve.clicked.connect(self.OpenReserve)
        self.ui.user_info.clicked.connect(self.OpenUserInfo)
        self.ui.push.clicked.connect(self.GongGao)
        self.ui.xiugai.clicked.connect(self.XiuGaiPassword)

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

    def OpenUserInfo(self):
        from administration.user_info import UserInfo
        self.UserInfo = UserInfo()
        self.UserInfo.ui.show()
        self.ui.close()

    def GongGao(self):
        gonggao = self.ui.textEdit.toPlainText().strip()
        sql = "UPDATE gonggao SET neirong = %s"
        self.cursor.execute(sql, (gonggao,))
        try:
            self.db.commit()
            QMessageBox.warning(self, "提示", "发布成功!!!")
            self.ui.textEdit.clear()
        except Exception as e:
            print("提交失败:", e)

    def XiuGaiPassword(self):
        password = self.ui.old_password.text().strip()
        sql = "SELECT password FROM administrator"
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        print(result)
        if result[0] == password:
            new_password = self.ui.new_password.text().strip()
            new_password2 = self.ui.new_password2.text().strip()
            if len(new_password) > 3 and new_password == new_password2:
                sql = "UPDATE administrator SET password = %s"
                self.cursor.execute(sql, (new_password,))
                try:
                    self.db.commit()
                    QMessageBox.warning(self, "提示", "修改成功!!!")
                except Exception as e:
                    QMessageBox.warning(self, "提示", "修改失败!!!")
                    print(e)
            else:
                QMessageBox.warning(self, "提示", "新密码为空或不匹配!!!")
        else:
            QMessageBox.warning(self, "提示", "原密码不正确!!!")

    def closeEvent(self, event):
        if self.db:
            self.db.close()
