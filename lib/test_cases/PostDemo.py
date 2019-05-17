# -*- coding:utf-8 -*-
import unittest
from lib.public import wraps


class PostDemo(unittest.TestCase):

    """PostDemo接口测试脚本"""

    def setUp(self):
        None

    def tearDown(self):
        None

    @unittest.skipIf(False, '条件为True ，用例跳过')
    @wraps.cases_runner
    @wraps.result_assert
    def test_post_demo(self, *args, **kwargs):
        """测试Post请求"""
        response = kwargs.get('response')
        self.assertEqual(kwargs.get('expect_assert_value'), kwargs.get('kwassert_value'))
        self.assertEqual(kwargs.get('database_check'), kwargs.get('execute_res'))
