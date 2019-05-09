# # -*- coding:utf-8 -*-
import yaml
import types
import pymssql
from lib.utils import fp
# from config import setting
from lib.public.Recursion import GetJsonParams


class ExecuteSQL(GetJsonParams):

    def __init__(self, connect_setting: dict = None):
        self.connect_setting = connect_setting
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = pymssql.connect(**self.connect_setting)
        self.cursor = self.conn.cursor()
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
        self.conn = pymssql.connect(**self.connect_setting)
        self.cursor = self.conn.cursor()
        self.cursor.execute(*args, **kwargs)
        return self.cursor.fetchall()

    # @classmethod
    # def loads_sql_data(cls) -> types.GeneratorType:
    #     """
    #     加载SQL数据，并以字典的形式返回
    #
    #     :Usage:
    #         loads_sql_data()
    #     """
    #
    #     sql_files = fp.iter_files(setting.DATA_PATH)
    #     for sql in sql_files:
    #         with open(sql, encoding='utf-8') as file:
    #             for dic in yaml.load(file):
    #                 for class_name, body in dic.items():
    #                     if len(body) > 1:
    #                         query_action = body['action']
    #                         table = cls.get_value(body['execSQL'], 'table')
    #                         columns = cls.get_value(body['execSQL'], 'columns')
    #                         params = cls.get_value(body['execSQL'], 'params')
    #                         desc = cls.get_value(body['execSQL'], 'desc')
    #                         yield {
    #                             'classname': class_name,
    #                             'action': query_action,
    #                             'table': table,
    #                             'columns': columns,
    #                             'params': params,
    #                             'desc': desc
    #                         }

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not exc_tb:
            self.conn.commit()
            self.cursor.close()
            del self.cursor
            self.conn.close()
            del self.conn
        else:
            self.conn.rollback()


if __name__ == '__main__':
    pass

    server="192.168.1.171:21433"
    user="testuser"
    password="testuser@123"
    EX = ExecuteSQL({'server': server, 'user': user, 'password': password, 'database': 'ChatbotTenant-TEST'})
    print(EX.execute("""SELECT * FROM [dbo].[Tenant_Info]"""))

# conn=pymssql.connect(server,user,password,database="ChatbotTenant-TEST")
# cursor=conn.cursor()
# cursor.execute("""SELECT * FROM [dbo].[Tenant_Info]""")
# row=cursor.fetchone()
# while row:
#     row=cursor.fetchone()
#     print(row)
#
# conn.close()