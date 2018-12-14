# -*- coding:utf-8 -*-
import json
import builtins
from functools import wraps
from lib.public import logger
from lib.public import http_keywords
from lib.utils.use_mysql import ExecuteSQL
from lib.public.Recursion import GetJsonParams
from lib.public.case_manager import TestContainer

ES = ExecuteSQL()

# FIXME: 生成的每个测试用例集中的每个case都将最终配置4-5个装饰器, \
#  现完成sql操作/用例运行/断言分析等装饰器, 缺少运行locust性能接口测试装饰器  \
#  locust模板已经构思完成


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
    def wrap(*args):

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

    return wrap


# FIXME:还要加入自动对比的逻辑
def result_assert(func):

    @wraps(func)
    def wrap(*args, **kwargs):

        response = kwargs.get('response')
        kwassert = kwargs.get('kwassert')
        tmp = tuple(kwassert.keys())
        result = GetJsonParams.for_keys_to_dict(*tmp, my_dict=response)
        for key, value in kwassert.items():
            if isinstance(value, list):
                tp, _value = value
                if tp == "type" and key == "responseType":
                    result[key] = [tp, repr(getattr(builtins, tp)(response)).split("'")[1]]
                elif tp == "type":
                    result[key] = [tp, repr(getattr(builtins, tp)(result.get(key))).split("'")[1]]
                else:
                    result[key] = [tp, getattr(builtins, tp)(result.get(key))]

        expect_assert_value = json.dumps(
            result,
            sort_keys=True,
            ensure_ascii=False
        )
        kwassert_value = json.dumps(
            kwassert,
            sort_keys=True,
            ensure_ascii=False
        )
        return func(*args, response=result, expect_assert_value=expect_assert_value, kwassert_value=kwassert_value)

    return wrap


if __name__ == '__main__':
    pass

