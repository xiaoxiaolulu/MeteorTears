# -*- coding: utf-8 -*-
import re


def custom_manage(custom: str, relevance: dict) -> str:
    r"""自定义关联配置

    :Args:
     - custom: 需要关联的数据对象, str object.
     - relevance:  替换关联数据对象的数据, dict object.
    """
    if isinstance(custom, str):
        try:
            relevance_list = re.findall("\${(.*?)}\$", custom)
            for n in relevance_list:
                pattern = re.compile('\${' + n + '}\$')
                custom = re.sub(pattern, relevance[n], custom, count=1)
        except TypeError:
            pass
        return custom
