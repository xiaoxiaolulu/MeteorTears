# -*- coding:utf-8 -*-
import yaml
import types
import pymysql
from lib.utils import fp
from config import setting
from lib.public import logger
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
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = pymysql.connect(**self.mysql_connect)
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
        return self

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
        if not exc_tb:
            self.conn.commit()
            self.cursor.close()
            del self.cursor
            self.conn.close()
            del self.conn
        else:
            self.conn.rollback()


class SqlContainer:

    data = []

    with ExecuteSQL() as file:

        for items in file.loads_sql_data():

            logger.log_debug("本次操作的数据库为{}".format(items['classname']))

            action = items['action']
            columns = ','.join(items['columns']) if len(items['columns']) else '*'
            table = items['table']
            params = items['params']
            desc = items['desc']

            if action == 'SELECT':
                sql = 'SELECT {} FROM {} WHERE {} {}'.format(columns, table, params, desc)
                result = file.execute(sql)
                logger.log_debug("执行的SQL语句为 ===> {}".format(sql))
                logger.log_debug("执行结果为 ===> {}".format(result))

            if action == 'DELETE':
                sql = 'DELETE FROM {} WHERE {}'.format(table, params)
                result = file.execute(sql)
                logger.log_debug("执行的SQL语句为 ===> {}".format(sql))
                logger.log_debug("执行结果为 ===> {}".format(result))

            data.append(items)

    def __iter__(self):
        return iter(self.data)

    def __next__(self):
        return next(self.data)

    def __repr__(self):
        return self.data
