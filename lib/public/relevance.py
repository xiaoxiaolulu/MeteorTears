# -*- coding: utf-8 -*-
import re
import ast


def custom_manage(custom: str, relevance: dict) -> dict:
    r"""上下游接口文件管理配置

    :Args:
     - custom: 需要关联的接口用例数据, str object.
     - relevance:  以${key}$的形式进行匹配内容替换, dict object.

     FIXME：替换参数为INT类型时不支持，若该INT类型的参数为中间位置替换时，\n
            会影响后面参数的正常替换
    """
    if isinstance(custom, str):
        _re_custom = {}

        try:

            relevance_list = re.findall("\${(.*?)}\$", custom)
            for n in relevance_list:
                if isinstance(relevance[n], str):
                    pattern = re.compile('\${' + n + '}\$')
                    custom = re.sub(pattern, relevance[n], custom, count=1)
                    _re_custom.update(ast.literal_eval(custom))
                if isinstance(relevance[n], dict):
                    _custom = ast.literal_eval(custom)
                    for _custom_key, _custom_value in _custom.items():
                        if _custom[_custom_key] == '${' + n + '}$':
                            _custom[_custom_key] = relevance[n]
                        else:
                            _custom[_custom_key] = _custom_value
                    _re_custom.update(_custom)
        except TypeError:
            pass
        return _re_custom


def extend_cases_manage(custom: str, relevance: dict) -> dict:
    r"""testsuite中入参变量替换数据

    :Args:
     - custom: 用例数据中存在需要入参的数据, str object.
     - relevance: 以${key}$的形式进行匹配内容替换, dict object.

    FIXME：替换变量不要添加int类型字符
    """
    if isinstance(custom, str):
        _re_custom = {}

        try:

            relevance_list = re.findall("\$<(.*?)>\$", custom)
            for n in relevance_list:
                if isinstance(relevance[n], str):
                    pattern = re.compile('\$<' + n + '>\$')
                    custom = re.sub(pattern, relevance[n], custom, count=1)
                    _re_custom.update(ast.literal_eval(custom))
                if isinstance(relevance[n], dict):
                    _custom = ast.literal_eval(custom)
                    for _custom_key, _custom_value in _custom.items():
                        if _custom[_custom_key] == '$<' + n + '>$':
                            _custom[_custom_key] = relevance[n]
                        else:
                            _custom[_custom_key] = _custom_value
                    _re_custom.update(_custom)
        except TypeError:
            pass
        return _re_custom
d = {'func_params': ['username'], 'method': 'post', 'url': '${Host}$/v31/mem/action/login', 'json': {'AppChannelId': 'testmarket', 'username': '$<username>$'}, 'headers': {'Content-Type': 'application/json; charset=utf-8'}}
c = {'username': '123213'}
print(extend_cases_manage(str(c), d))