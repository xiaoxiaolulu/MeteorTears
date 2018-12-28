# -*- coding:utf-8 -*-
import os
import click
import unittest
from config import setting
from lib.utils import email
from lib.public.case_manager import TestContainer
from lib.public.BeautifulReport import BeautifulReport


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
    result.report(filename='Marketing测试报告', description='Marketing测试报告', log_path=report)

    # 发送邮件
    send_mail = email.SendMail()
    send_mail.send_mail()

    # 测试用例回溯
    try:
        for files in os.listdir(cases):
            if os.path.isfile(files):
                os.remove(cases + files)
    except PermissionError:
        pass


if __name__ == '__main__':
    run()
