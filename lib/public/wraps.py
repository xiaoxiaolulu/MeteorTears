# -*- coding:utf-8 -*-
import ast
import yaml
import json
import builtins
from os import path
from functools import wraps
from config import setting
from lib.public import logger, relevance
from lib.public import http_keywords
from lib.utils.use_SqlServer import ExecuteSQL
from lib.public.Recursion import GetJsonParams
from lib.public.case_manager import TestContainer


DataBaseSetting = {
    'server': "192.168.1.171:21433", 'user': "testuser", 'password': "testuser@123", 'database': 'ChatbotAdmin-TEST'
}


def cases_runner(func):

    @wraps(func)
    def wrap(*args):

        for items in iter(TestContainer()):

            for key, value in dict(items).items():
                if value == func.__name__:

                    body = {}

                    # 用例场景集合继承单组用例, 个组API表达一个测试动作
                    # relevant_case_api = items.get('body').get('relevant_case_api')
                    # if relevant_case_api:
                    #
                    #     if isinstance(relevant_case_api, list):
                    #         _relevance = {}
                    #         for case_api in relevant_case_api:
                    #
                    #             relevant_files = case_api + '.yaml'
                    #             with open(path.join(setting.CASES_API, relevant_files), 'rb') as file:
                    #                 _relevance.update(yaml.safe_load(file))
                    #
                    #         relevance_body = relevance.custom_manage(str(items['body']), _relevance)
                    #         body.update(ast.literal_eval(relevance_body))

                    # 用例文件与临时变量文件相互关联
                    relevant_params = items.get('body').get('relevant_parameter')

                    if relevant_params:

                        if isinstance(relevant_params, list):
                            _relevance = {}
                            for relevant_param in relevant_params:

                                relevant_files = relevant_param + '.yaml'
                                with open(setting.RES + relevant_files, 'rb') as file:
                                    _relevance.update(yaml.safe_load(file))

                            relevance_body = relevance.custom_manage(str(items['body']), _relevance)
                            body.update(ast.literal_eval(relevance_body))

                        # 运行用例，暂支持Post与Get请求接口
                        handler = http_keywords.BaseKeyWords(body)
                        result = handler.make_test_templates()

                        logger.log_info("本次用例执行的测试结果为{}".format(
                            json.dumps(result, indent=4, ensure_ascii=False))
                        )

                        # 将临时变量写入yaml文件
                        res_index = items.get('body').get('res_index')
                        if res_index:
                            if isinstance(res_index, list):
                                for res_key in res_index:
                                    return_res = GetJsonParams.get_value(result, res_key)
                                    file_name = setting.RES + res_key
                                    logger.log_debug('保存的变量值为 => {} '.format(return_res))

                                    with open(file_name + '.yaml', 'w', encoding='utf-8') as file:
                                        file.write('{}: {}'.format(res_key, return_res))

                            if isinstance(res_index, str):
                                return_res = GetJsonParams.get_value(result, res_index)
                                file_name = setting.RES + res_index
                                logger.log_debug('保存的变量值为 {}'.format(return_res))

                                with open(file_name, 'w', encoding='utf-8') as file:
                                    file.write('{}: {}'.format(res_index, return_res))

                        # 场景测试用例继承单组api集合
                        relevant_api = items.get('body').get('relevant_case_api')
                        if relevant_api:
                            if isinstance(relevant_params, list):
                                _relevance = {}
                                for relevant_param in relevant_params:
                                    relevant_files = relevant_param + '.yaml'
                                    with open(setting.RES + relevant_files, 'rb') as file:
                                        _relevance.update(yaml.safe_load(file))

                                relevance_body = relevance.custom_manage(str(items['body']), _relevance)
                                body.update(ast.literal_eval(relevance_body))

                            # 运行用例，暂支持Post与Get请求接口
                            handler = http_keywords.BaseKeyWords(body)
                            result = handler.make_test_templates()

                            logger.log_info("本次用例执行的测试结果为{}".format(
                                json.dumps(result, indent=4, ensure_ascii=False))
                            )

                            # 将临时变量写入yaml文件
                            res_index = items.get('body').get('res_index')
                            if res_index:
                                if isinstance(res_index, list):
                                    for res_key in res_index:
                                        return_res = GetJsonParams.get_value(result, res_key)
                                        file_name = setting.RES + res_key
                                        logger.log_debug('保存的变量值为 => {} '.format(return_res))

                                        with open(file_name + '.yaml', 'w', encoding='utf-8') as file:
                                            file.write('{}: {}'.format(res_key, return_res))

                                if isinstance(res_index, str):
                                    return_res = GetJsonParams.get_value(result, res_index)
                                    file_name = setting.RES + res_index
                                    logger.log_debug('保存的变量值为 {}'.format(return_res))

                                    with open(file_name, 'w', encoding='utf-8') as file:
                                        file.write('{}: {}'.format(res_index, return_res))

                        # 验证接口请求数据是否落库
                        excep_columns, res_sql = {}, {}
                        relevant_database = items.get('body').get('relevant_sql')
                        if relevant_database:

                            if isinstance(relevant_database, list):
                                for relevant_db in relevant_database:
                                    filename = relevant_db + '.yaml'

                                    relevant_sql = {}
                                    with open(setting.CASE_DATA + filename, 'rb') as file:
                                        relevant_sql.update(yaml.safe_load(file))

                                    action = relevant_sql[relevant_db]['action']
                                    columns = relevant_sql[relevant_db]['execSQL']['columns']
                                    table = relevant_sql[relevant_db]['execSQL']['table']
                                    params = relevant_sql[relevant_db]['execSQL']['params']
                                    desc = relevant_sql[relevant_db]['execSQL']['desc']
                                    execute_sql = '{} {} FROM {} {} {}'.format(action, columns, table, params, desc)
                                    execute_res = ExecuteSQL(DataBaseSetting).execute(execute_sql)[0][0]

                                    res_sql.update({columns: execute_res})
                                    logger.log_debug('执行sql结果为{}'.format(execute_res))

                        return func(
                            *args,
                            response=result,
                            kwassert=items.get('body').get('assert'),
                            execute_res=res_sql,
                            db_check=items.get('body').get('check_db')
                        )

    return wrap


def result_assert(func):

    @wraps(func)
    def wrap(*args, **kwargs):

        response = kwargs.get('response')
        kwassert = kwargs.get('kwassert')
        database_check = kwargs.get('db_check') if kwargs.get('db_check') else {}
        execute_res = kwargs.get('execute_res')

        tmp = tuple(kwassert.keys())
        result = GetJsonParams.for_keys_to_dict(*tmp, my_dict=response)

        for key, value in kwassert.items():

            if isinstance(value, list):
                tp, _value = value
                if tp == "type" and key == "ResponseType":
                    result[key] = [tp, repr(getattr(builtins, tp)(response)).split("'")[1]]
                elif tp == "type":
                    result[key] = [tp, repr(getattr(builtins, tp)(result.get(key))).split("'")[1]]
                elif tp == "len":
                    result[key] = [tp, repr(getattr(builtins, tp)(result.get(key)))]
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
        return func(
            *args,
            response=result,
            expect_assert_value=expect_assert_value,
            kwassert_value=kwassert_value,
            database_check=database_check,
            execute_res=execute_res
        )

    return wrap
