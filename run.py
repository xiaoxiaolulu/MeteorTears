# -*- coding:utf-8 -*-
import click
import shutil
import unittest
from config import setting
from lib.public.case_manager import TestContainer
from lib.public.BeautifulReport import BeautifulReport


@click.command()
@click.option('--cases', default=setting.TEST_CASES, help="case file path")
@click.option('--pattern', default='*.py', help="get cases file pattern")
@click.option(
    '--report',
    default=setting.REPORT,
    help="generator report in path")
def run(cases, pattern, report):
    test_suite = unittest.defaultTestLoader.discover(cases, pattern)
    result = BeautifulReport(test_suite)
    result.report(filename='Marketing测试报告', description='Marketing测试报告', log_path=report)

    shutil.rmtree(setting.TEST_CASES)


if __name__ == '__main__':
    run()
