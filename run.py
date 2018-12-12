# -*- coding:utf-8 -*-
import unittest

from config import setting
from lib.public.BeautifulReport import BeautifulReport


def run():
    test_suite = unittest.defaultTestLoader.discover(setting.make_directory('tests', 0), pattern='test*.py')
    result = BeautifulReport(test_suite)
    result.report(
        filename='report',
        description='IDEF测试报告',
        log_path='report/')


if __name__ == '__main__':
    run()
