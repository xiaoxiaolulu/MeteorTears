# -*- coding:utf-8 -*-
import unittest
from lib.public import wraps


class Demo(unittest.TestCase):

    """Demo接口测试脚本"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @wraps.create_random_data
    @unittest.skipIf(True, '条件为True ，用例跳过')
    @wraps.cases_runner
    @wraps.result_assert
    def test_get_public_key(self, *args, **kwargs):
        """测试httpbin的ip接口返回正常"""
        response = kwargs.get('response')
        self.assertEqual(kwargs.get('expect_assert_value'), kwargs.get('kwassert_value'))
        self.assertEqual(kwargs.get('database_check'), kwargs.get('execute_res'))
