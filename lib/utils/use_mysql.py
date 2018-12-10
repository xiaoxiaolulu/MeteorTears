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
            'password': setting.DATABASE['psw'],
            'db': setting.DATABASE['db'],
            'charset': setting.DATABASE['charset']
        }
        self.conn = pymysql.connect(**self.mysql_connect)
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    def __enter__(self):
        self.file = open(fp.iter_files(setting.make_directory('data', 0))[0], encoding='utf-8')
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

    def loads_sql_data(self) -> types.GeneratorType:
        """
        加载SQL数据，并以列表的形式返回

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
                            table = self.get_value(body['execSQL'], 'table')
                            columns = self.get_value(body['execSQL'], 'columns')
                            params = self.get_value(body['execSQL'], 'params')
                            desc = self.get_value(body['execSQL'], 'desc')
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


class CreateSqlObj:

    sql_data = []

    with ExecuteSQL() as file:
        for items in file.loads_sql_data():
            print(items)

if __name__ == '__main__':
    print(CreateSqlObj)