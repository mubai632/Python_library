# -*- coding: utf-8 -*-
import sys
from PyQt5.QtCore import *
from Main_interface import *


class AppCleanup(QObject):
    # 创建一个信号，用于在应用程序退出时触发数据库清理操作
    cleanup_signal = pyqtSignal()

    def __init__(self):
        super().__init__()

    def cleanup(self):
        # 连接到数据库并删除表
        self.db = OpenMySql.open_connection()
        cursor = self.db.cursor()
        cursor.execute("DELETE FROM dl_user")
        self.db.commit()  # 提交事务才能显示删除的数据
        cursor.close()
        self.db.close()

    def start_cleanup(self):
        # 启动应用程序清理操作
        self.cleanup_signal.emit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.ui.show()

    # 创建应用程序清理对象
    cleanup = AppCleanup()

    # 连接应用程序退出信号到清理操作
    app.aboutToQuit.connect(cleanup.cleanup)

    sys.exit(app.exec_())
