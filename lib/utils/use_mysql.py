# -*- coding:utf-8 -*-
import yaml
import pymysql
import types
from config import setting
from lib.utils import fp
from lib.public.Recursion import GetJsonParams


class ExecuteSQL(GetJsonParams):

    def __init__(self):
        """数据库链接池"""
        self.mysql_connect = {
            'host': setting.DATABASE['host'],
            'port': int(setting.DATABASE['port']),
            'user': setting.DATABASE['user'],
            'passwd': setting.DATABASE['psw'],
            'db': setting.DATABASE['db'],
            'charset': setting.DATABASE['charset']
        }
        self.sql = None
        self.conn = pymysql.connect(**self.mysql_connect)
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    def __enter__(self):
        self.file = open(self.sql, encoding='utf-8')
        return self.file

    def execute(self, *args, **kwargs) -> dict:
        """
        执行SQL语句

        :Args:
         - query: 查询执行语句 STR TYPE.
         - args: 用于执行的查询参数, TUPLE, LIST OR DICT TYPE.

        :Usage:
            execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='test_results'")
        """
        return self.cursor.execute(*args, **kwargs)

    def close(self) -> None:
        """
        关闭游标只会耗尽所有剩余数据.

        :Usage:
            close()
        """
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    @classmethod
    def loads_sql_data(cls) -> types.GeneratorType:
        """
        加载SQL数据，并以字典的形式返回

        :Usage:
            loads_sql_data()
        """

        sql_files = fp.iter_files(setting.make_directory('data', 0))
        for sql in sql_files:
            with open(sql, encoding='utf-8') as file:
                for dic in yaml.load(file):
                    for class_name, body in dic.items():
                        if len(body) > 1:
                            query_action = body['action']
                            table = cls.get_value(body['execSQL'], 'table')
                            columns = cls.get_value(body['execSQL'], 'columns')
                            params = cls.get_value(body['execSQL'], 'params')
                            desc = cls.get_value(body['execSQL'], 'desc')
                            yield {
                                'classname': class_name,
                                'action': query_action,
                                'table': table,
                                'columns': columns,
                                'params': params,
                                'desc': desc
                            }

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()
        del self.file


if __name__ == '__main__':
    pass
