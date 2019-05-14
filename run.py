# -*- coding:utf-8 -*-
import os
import click
import unittest
import pysnooper
from config import setting
from lib.utils import email
from lib.public.case_manager import TestContainer
from lib.public.HtmlReport import Report
from lib.utils.analyze_log import WeChatAlarm


@click.command()
@click.option('--cases', default=setting.TEST_CASES, help="case file path")
@click.option('--pattern', default='*.py', help="get cases file pattern")
@click.option(
    '--report',
    default=setting.REPORT,
    help="generator report in path")
@pysnooper.snoop()
def run(cases=setting.TEST_CASES, pattern='*.py', report=setting.REPORT):
    test_suite = unittest.defaultTestLoader.discover(cases, pattern)
    result = Report(test_suite)
    result.report(filename='HighTalkReport', description='HighTalkReport', log_path=report)

    # 测试用例回溯
    # try:
    #     for files in os.listdir(cases):
    #         filename = cases + files
    #         if os.path.isfile(filename):
    #             os.remove(filename)
    # except PermissionError:
    #     pass

    # 临时变量文件回溯
    # for files in os.listdir(setting.PUBLIC_RES):
    #     filename = setting.PUBLIC_RES + files
    #     if os.path.isfile(filename):
    #         os.remove(filename)

    # 发送邮件
    # send_mail = email.SendMail()
    # send_mail.send_mail()

    # 日志告警
    # push_msg = WeChatAlarm()
    # push_msg.send_message(push_msg.error_log_message())


if __name__ == '__main__':
    run()
