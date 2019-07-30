# -*- coding:utf-8 -*-
import os
import click
import unittest
import pysnooper
from config import setting
from lib.utils import time_util
from lib.utils import email
from lib.public.case_manager import TestContainer
from lib.utils.analyze_log import WeChatAlarm
from lib.utils.random_data import RandomData
from lib.public.HtmlReport import Report


@click.command()
@click.option('--cases', default=setting.TEST_CASES, help="case file path")
@click.option('--pattern', default='*.py', help="get cases file pattern")
@click.option(
    '--report',
    default=setting.REPORT,
    help="generator report in path")
@pysnooper.snoop()
def run(cases=setting.TEST_CASES, pattern='*.py', report=setting.REPORT) -> None:
    r"""运行测试用例主入口

    :param cases: 运行的测试用例文件路径, str object.
    :param pattern: 匹配运行的测试用例文件, str object.
    :param report: 生成的测试报告路径, str object.
    """

    # 生成随机测试数据
    RandomData.create_random_test_data()

    # 加载&运行测试用例
    test_suite = unittest.defaultTestLoader.discover(cases, pattern)
    result = Report(test_suite)
    result.report(filename='Report', description='Report', log_path=report)

    # 临时文件回溯
    def files_backtrack(filepath: list) -> None:
        if isinstance(filepath, list):
            for path in filepath:
                try:
                    for files in os.listdir(path):
                        filename, pattern_back_date = path + files, time_util.timestamp('format_day')
                        if os.path.isfile(filename) and pattern_back_date not in files.split('.'):
                            os.remove(filename)
                except PermissionError:
                    pass

    back_track_files_path = [cases, setting.LOG]
    files_backtrack(back_track_files_path)

    # 发送邮件
    # send_mail = email.SendMail()
    # send_mail.send_mail()

    # 日志告警
    # push_msg = WeChatAlarm()
    # push_msg.send_message(push_msg.error_log_message())


if __name__ == '__main__':
    run()
