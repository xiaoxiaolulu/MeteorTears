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
                if isinstance(relevance[n], (dict, int)):
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
