# -*- coding:utf-8 -*-
import os
import click
import unittest
from config import setting
from lib.utils import email
from lib.public.case_manager import TestContainer
from lib.public.BeautifulReport import BeautifulReport
from lib.utils.analyze_log import WeChatAlarm


@click.command()
@click.option('--cases', default=setting.TEST_CASES_PATH, help="case file path")
@click.option('--pattern', default='*.py', help="get cases file pattern")
@click.option(
    '--report',
    default=setting.REPORT_PATH,
    help="generator report in path")
def run(cases, pattern, report):
    test_suite = unittest.defaultTestLoader.discover(cases, pattern)
    result = BeautifulReport(test_suite)
    result.report(filename='关键字回复测试报告', description='关键字回复测试报告', log_path=report)

    # 测试用例回溯
    try:
        for files in os.listdir(cases):
            os.remove(cases + files)
    except PermissionError:
        pass

    # 临时变量文件回溯
    # for files in os.listdir(setting.PUBLIC_RES):
    #     os.remove(setting.PUBLIC_RES + files)

    # 发送邮件
    # send_mail = email.SendMail()
    # send_mail.send_mail()

    # 日志告警
    push_msg = WeChatAlarm()
    push_msg.send_message(push_msg.error_log_message())


if __name__ == '__main__':
    run()
