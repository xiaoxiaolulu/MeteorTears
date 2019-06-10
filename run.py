# -*- coding:utf-8 -*-
import os
import click
import unittest
import pysnooper
from config import setting
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
def run(cases=setting.TEST_CASES, pattern='*.py', report=setting.REPORT):

    RandomData.create_random_test_data()

    test_suite = unittest.defaultTestLoader.discover(cases, pattern)
    result = Report(test_suite, retry=3)
    result.report(filename='Report', description='Report', log_path=report)

    # 临时文件回溯
    def files_backtrack(filepath: list) -> None:
        if isinstance(filepath, list):
            for path in filepath:
                try:
                    for files in os.listdir(path):
                        filename = path + files
                        if os.path.isfile(filename):
                            os.remove(filename)
                except PermissionError:
                    pass

    back_track_files_path = [cases, setting.Recording, setting.WORK_FLOW]
    files_backtrack(back_track_files_path)

    # 发送邮件
    # send_mail = email.SendMail()
    # send_mail.send_mail()

    # 日志告警
    # push_msg = WeChatAlarm()
    # push_msg.send_message(push_msg.error_log_message())


if __name__ == '__main__':
    run()
