# -*- coding:utf-8 -*-
import pymysql
from config import setting


class MetaSingleton(type):

    __instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls.__instances:
            cls.__instances[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)
            return cls.__instances[cls]


class ExecuteSQL(metaclass=MetaSingleton):

    def __init__(self):
        # Database connection pool
        self.mysql_connect = setting.DATABASE
        self.conn = pymysql.connect(**self.mysql_connect)
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    def execute(self, *args, **kwargs):
        """
        Execute a query

        :Args:
         - query: Query to execute, STR TYPE.
         - args: parameters used with query, TUPLE, LIST OR DICT TYPE.

        :Usage:
            execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='test_results'")
        """
        return self.cursor.execute(*args, **kwargs)

    def close(self):
        """
        Closing a cursor just exhausts all remaining data.
        """
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

if __name__ == '__main__':
    pass
