# -*- coding:utf-8 -*-
import time


def timestamp(format_key: str) -> str:
    r"""格式化时间

    :Args:
     - format_key: 转化格式方式, str object.

    :Usage:
        timestamp('format_day')
    """
    format_time = {
        'default':
            {
                'format_day': '%Y-%m-%d',
                'format_now': '%Y-%m-%d-%H_%M_%S',
                'unix_now': '%Y-%m-%d %H:%M:%S',
            }
    }
    return time.strftime(format_time['default'][format_key], time.localtime(time.time()))


def time_unix() -> int:
    r"""转化为时间蹉

    :Usage:
        time_unix()
    """
    return int(time.mktime(time.strptime(timestamp('unix_now'), "%Y-%m-%d %H:%M:%S")))
