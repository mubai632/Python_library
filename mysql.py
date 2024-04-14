# -*- coding: utf-8 -*_
import pymysql


class OpenMySql():
    @staticmethod
    def open_connection():
        db = pymysql.connect(
            host="localhost",
            user="root",
            password="000000",
            database="book_library"
        )
        return db
