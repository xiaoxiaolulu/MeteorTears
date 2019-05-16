# -*- coding:utf-8 -*-
import unittest
from lib.public import wraps


class A001ValidateLogin(unittest.TestCase):

    """A001ValidateLogin接口测试脚本"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @wraps.create_random_data
    @unittest.skipIf(False, '条件为True ，用例跳过')
    @wraps.cases_runner
    @wraps.result_assert
    def test_validate_login(self, *args, **kwargs):
        """登录成功"""
        response = kwargs.get('response')
        self.assertEqual(kwargs.get('expect_assert_value'), kwargs.get('kwassert_value'))
        self.assertEqual(kwargs.get('database_check'), kwargs.get('execute_res'))
