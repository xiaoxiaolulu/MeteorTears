# -*- coding:utf-8 -*-
import unittest
from lib.public import wraps


class KqaBotSearch(unittest.TestCase):

    """KqaBotSearch接口测试脚本"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @wraps.create_random_data
    @unittest.skipIf(True, '条件为True ，用例跳过')
    @wraps.cases_runner
    @wraps.result_assert
    def test_kqa_bot_search(self, *args, **kwargs):
        """关键字搜索- bot查询接口-成功"""
        response = kwargs.get('response')
        self.assertEqual(kwargs.get('expect_assert_value'), kwargs.get('kwassert_value'))
        self.assertEqual(kwargs.get('database_check'), kwargs.get('execute_res'))
