# -*- coding:utf-8 -*-
from functools import wraps
from lib.public import logger
from lib.public import http_keywords
from lib.utils.use_mysql import ExecuteSQL
from lib.public.case_manager import TestContainer

ES = ExecuteSQL()


def test_data_runner(func):

    @wraps(func)
    def wrap(*args, **kwargs):

        for item in iter(ExecuteSQL.loads_sql_data()):

            func_name = func.__name__.title().replace('_', '')
            if item['classname'] == func_name:
                logger.log_debug("操作的数据库表为 ====> {}".format(item['classname']))
                columns = ','.join(item['columns']) if len(item['columns']) else '*'
                table = item['table']
                params = item['params']
                desc = item['desc']
                if item['action'] == 'SELECT':
                    sql = 'SELECT {} FROM {} WHERE {} {}'.format(columns, table, params, desc)
                    result = ES.execute(sql)
                    logger.log_debug("执行的SQL语句为 ===> {}".format(sql))
                    logger.log_debug("执行结果为 ===> {}".format(result))
                if item['action'] == 'DELETE':
                    sql = 'DELETE FROM {} WHERE {}'.format(table, params)
                    result = ES.execute(sql)
                    logger.log_debug("执行的SQL语句为 ===> {}".format(sql))
                    logger.log_debug("执行结果为 ===> {}".format(result))
        return func(*args, **kwargs)

    return wrap


def cases_runner(func):

    @wraps(func)
    def wrap(*args, **kwargs):

        for items in iter(TestContainer()):
            for key, value in dict(items).items():
                if value == func.__name__:
                    handler = http_keywords.BaseKeyWords(items['body'])
                    result = handler.make_test_templates()
                    logger.log_debug("The test result is {}".format(result))
                    return func(
                        *args,
                        response=result,
                        kwassert=items.get('body').get('assert')
                    )

        return func(*args, **kwargs)

    return wrap


if __name__ == '__main__':
    @cases_runner
    def add_channel(*args, **kwargs):
        print(kwargs.get('response'))
        print(kwargs.get('kwassert'))

    add_channel()
