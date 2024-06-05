# -*- coding: utf-8 -*_
import pymysql


class OpenMySql():
    @staticmethod
    def open_connection():
        try:
            db = pymysql.connect(
                host="localhost",
                user="root",
                password="000000",
                database="book_library",
                charset="utf8"
            )
            return db
        except pymysql.MySQLError as e:
            print(f"Error connecting to the database: {e}")
            return None

