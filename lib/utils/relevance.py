# -*- coding: utf-8 -*-
import re


def custom_manage(custom: str, relevance: dict) -> str:
    """
    自定义关联配置

    :Args:
     - custom:  自定义错误说明, STR TYPE.
     - relevance:  关联对象, DICT TYPE.
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


if __name__ == "__main__":
    pass
