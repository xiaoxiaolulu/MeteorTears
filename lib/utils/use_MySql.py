# # -*- coding:utf-8 -*-
import yaml
import types
import pymysql
from config import setting
from lib.public.Recursion import GetJsonParams


class ExecuteSQL(GetJsonParams):

    def __init__(self, connect_setting: dict = None):
        self.connect_setting = connect_setting
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = pymysql.connect(**self.connect_setting)
        self.cursor = self.conn.cursor()
        return self

    def execute(self, *args, **kwargs) -> dict:
        r"""执行SQL语句

        :Args:
         - query: 查询执行语句 str object.
         - args: 用于执行的查询参数, tuple/list/dict object.

        :Usage:
            execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='test_results'")
        """
        self.conn = pymysql.connect(**self.connect_setting)
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
        self.cursor.execute(*args, **kwargs)
        return self.cursor.fetchall()

    @classmethod
    def loads_sql_data(cls, filename) -> types.GeneratorType:
        r"""加载SQL数据，并以字典的形式返回

        :Usage:
            loads_sql_data()
        """
        with open(setting.CASE_DATA + filename, encoding='utf-8') as file:
            for class_name, body in yaml.safe_load(file).items():
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

    def specify_file_execution_data(self, filename: str):
        for sql_content in iter(self.loads_sql_data(filename)):
            class_name = sql_content['class_name']
            action = sql_content['action']
            table = sql_content['sql']
            columns = sql_content['columns']
            params = sql_content['params']
            desc = sql_content['desc']

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not exc_tb:
            self.conn.commit()
            self.cursor.close()
            del self.cursor
            self.conn.close()
            del self.conn
        else:
            self.conn.rollback()
