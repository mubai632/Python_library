# -*- coding:utf-8 -*-
# 推荐书籍
from PyQt5 import uic
from PyQt5.QtWidgets import *


#自建模块

class RecommendedBooks(QMainWindow):
    # def __init__(self):
    #     super().__init__()
    #     self.ui = uic.loadUi('./ui_user/Recommended_books.ui')

    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi('./ui_user/Recommended_books_Null.ui')
