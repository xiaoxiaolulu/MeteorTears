# -*- coding:utf-8 -*-
import unittest
from lib.public import wraps


class Setupteardown(unittest.TestCase):

    """Setupteardown接口测试脚本"""

    def setUp(self):
        print('前置条件')

    def tearDown(self):
        print('后置条件')

    @unittest.skipIf(False, '条件为True ，用例跳过')
    @wraps.cases_runner
    @wraps.result_assert
    def test_setupteardown(self, *args, **kwargs):
        """前置后置条件测试"""
        response = kwargs.get('response')
        self.assertEqual(kwargs.get('expect_assert_value'), kwargs.get('kwassert_value'))
        self.assertEqual(kwargs.get('database_check'), kwargs.get('execute_res'))
