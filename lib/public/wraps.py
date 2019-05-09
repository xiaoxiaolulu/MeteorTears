# -*- coding:utf-8 -*-
import os
import yaml
import json
import builtins
from functools import wraps
from config import setting
from lib.utils import relevance
from lib.public import logger
from lib.public import http_keywords
from lib.utils.use_SqlServer import ExecuteSQL
from lib.public.Recursion import GetJsonParams
from lib.public.case_manager import TestContainer

ES = ExecuteSQL()


def test_data_runner(func):

    @wraps(func)
    def wrap(*args, **kwargs):

        global ExecuteResult

        for item in iter(ExecuteSQL.loads_sql_data()):

            func_name = func.__name__.title().replace('_', '')
            sql_pattern_obj = item['classname'].split('_')[0]
            if sql_pattern_obj in func_name:
                logger.log_debug("操作的数据库表为 ====> {}".format(item['classname']))
                columns = ','.join(item['columns']) if len(item['columns']) else '*'
                table = item['table']
                params = item['params']
                desc = item['desc']
                if item['action'] == 'SELECT':
                    sql = 'SELECT {} FROM {} WHERE {} {}'.format(columns, table, params, desc)
                    ExecuteResult = ES.execute(sql)[0]['id']
                    logger.log_debug("执行的SQL语句为 ===> {}".format(sql))
                    logger.log_debug("执行结果为 ===> {}".format(ExecuteResult))
                if item['action'] == 'DELETE':
                    sql = 'DELETE FROM {} WHERE {}'.format(table, params)
                    ExecuteResult = ES.execute(sql)
                    logger.log_debug("执行的SQL语句为 ===> {}".format(sql))
                    logger.log_debug("执行结果为 ===> {}".format(ExecuteResult))
        return func(*args, **kwargs, resql=ExecuteResult)

    return wrap


def cases_runner(func):

    @wraps(func)
    def wrap(*args):

        for items in iter(TestContainer()):

            for key, value in dict(items).items():
                if value == func.__name__:

                    body = {}
                    # 用例文件与临时变量文件相互关联
                    relevant_params = items.get('body').get('relevant_parameter')

                    if relevant_params:

                        if isinstance(relevant_params, str):
                            relevant_files = relevant_params + '.yaml'
                            _relevance = {}
                            with open(setting.PUBLIC_RES + relevant_files, 'rb') as file:
                                _relevance.update(yaml.load(file))

                            relevance_body = relevance.custom_manage(str(items['body']), _relevance)
                            body.update(eval(relevance_body))

                        if isinstance(relevant_params, list):

                            _relevance = {}
                            for relevant_param in relevant_params:

                                relevant_files = relevant_param + '.yaml'
                                with open(setting.PUBLIC_RES + relevant_files, 'rb') as file:
                                    _relevance.update(yaml.load(file))

                            relevance_body = relevance.custom_manage(str(items['body']), _relevance)
                            body.update(eval(relevance_body))

                        # 运行用例，暂支持Post与Get请求接口
                        handler = http_keywords.BaseKeyWords(body)
                        result = handler.make_test_templates()

                        logger.log_info("The test.json result is{}".format(
                            json.dumps(result, indent=4, ensure_ascii=False))
                        )

                        # 将临时变量写入yaml文件
                        res_index = items.get('body').get('res_index')
                        if res_index:
                            if isinstance(res_index, list):
                                for res_key in res_index:
                                    return_res = GetJsonParams.get_value(result, res_key)
                                    file_name = setting.PUBLIC_RES + res_key
                                    logger.log_debug('保存的变量值为 {} => '.format(return_res))

                                    with open(file_name + '.yaml', 'w', encoding='utf-8') as file:
                                        file.write('{}: {}'.format(res_key, return_res))

                            if isinstance(res_index, str):
                                return_res = GetJsonParams.get_value(result, res_index)
                                file_name = setting.PUBLIC_RES + res_index
                                logger.log_debug('保存的变量值为 {}'.format(return_res))

                                with open(file_name, 'w', encoding='utf-8') as file:
                                    file.write('{}: {}'.format(res_index, return_res))

                        return func(
                            *args,
                            response=result,
                            kwassert=items.get('body').get('assert'),
                            db_check=items.get('body').get('check_db')
                        )

    return wrap


def result_assert(func):

    @wraps(func)
    def wrap(*args, **kwargs):

        response = kwargs.get('response')
        kwassert = kwargs.get('kwassert')
        database_check = kwargs.get('db_check')

        tmp = tuple(kwassert.keys())
        result = GetJsonParams.for_keys_to_dict(*tmp, my_dict=response)
        for key, value in kwassert.items():
            if isinstance(value, list) and len(value) > 1:
                tp, _ = value
                if tp == "type" and key == "responseType":
                    result[key] = [tp, repr(getattr(builtins, tp)(response)).split("'")[1]]
                elif tp == "type":
                    result[key] = [tp, repr(getattr(builtins, tp)(result.get(key))).split("'")[1]]
                else:
                    result[key] = [tp, getattr(builtins, tp)(result.get(key))]
            else:
                result[key] = response[key]

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
        return func(
            *args,
            response=result,
            expect_assert_value=expect_assert_value,
            kwassert_value=kwassert_value
        )

    return wrap


if __name__ == '__main__':
    pass
