# -*- coding:utf-8 -*-
import unittest
from lib.public import wraps


class KqaAdd(unittest.TestCase):

    """KqaAdd接口测试脚本"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @wraps.create_random_data
    @unittest.skipIf(True, '条件为True ，用例跳过')
    @wraps.cases_runner
    @wraps.result_assert
    def test_kqa_bot_add(self, *args, **kwargs):
        """关键字搜索- 添加关键字-成功"""
        response = kwargs.get('response')
        self.assertEqual(kwargs.get('expect_assert_value'), kwargs.get('kwassert_value'))
        self.assertEqual(kwargs.get('database_check'), kwargs.get('execute_res'))

    @wraps.create_random_data
    @unittest.skipIf(True, '条件为True ，用例跳过')
    @wraps.cases_runner
    @wraps.result_assert
    def test_kqa_bot_add_required_verify_answer(self, *args, **kwargs):
        """关键字搜索-添加关键字-answer为空"""
        response = kwargs.get('response')
        self.assertEqual(kwargs.get('expect_assert_value'), kwargs.get('kwassert_value'))
        self.assertEqual(kwargs.get('database_check'), kwargs.get('execute_res'))

    @wraps.create_random_data
    @unittest.skipIf(True, '条件为True ，用例跳过')
    @wraps.cases_runner
    @wraps.result_assert
    def test_kqa_bot_add_required_verify_CreateUserName(self, *args, **kwargs):
        """关键字搜索- 添加关键字-CreateUserName为空"""
        response = kwargs.get('response')
        self.assertEqual(kwargs.get('expect_assert_value'), kwargs.get('kwassert_value'))
        self.assertEqual(kwargs.get('database_check'), kwargs.get('execute_res'))

    @wraps.create_random_data
    @unittest.skipIf(True, '条件为True ，用例跳过')
    @wraps.cases_runner
    @wraps.result_assert
    def test_kqa_bot_add_required_verify_TenantDomain(self, *args, **kwargs):
        """关键字搜索- 添加关键字-TenantDomain为空"""
        response = kwargs.get('response')
        self.assertEqual(kwargs.get('expect_assert_value'), kwargs.get('kwassert_value'))
        self.assertEqual(kwargs.get('database_check'), kwargs.get('execute_res'))

    @wraps.create_random_data
    @unittest.skipIf(True, '条件为True ，用例跳过')
    @wraps.cases_runner
    @wraps.result_assert
    def test_kqa_bot_add_keyword_number(self, *args, **kwargs):
        """关键字搜索- 添加关键字-keyword不超过三个"""
        response = kwargs.get('response')
        self.assertEqual(kwargs.get('expect_assert_value'), kwargs.get('kwassert_value'))
        self.assertEqual(kwargs.get('database_check'), kwargs.get('execute_res'))

    @wraps.create_random_data
    @unittest.skipIf(True, '条件为True ，用例跳过')
    @wraps.cases_runner
    @wraps.result_assert
    def test_kqa_bot_add_keyword_splite(self, *args, **kwargs):
        """关键字搜索- 添加关键字-keyword分隔符"""
        response = kwargs.get('response')
        self.assertEqual(kwargs.get('expect_assert_value'), kwargs.get('kwassert_value'))
        self.assertEqual(kwargs.get('database_check'), kwargs.get('execute_res'))
