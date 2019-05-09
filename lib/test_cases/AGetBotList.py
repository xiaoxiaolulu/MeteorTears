# -*- coding:utf-8 -*-
import unittest
from lib.public import wraps


class AGetBotList(unittest.TestCase):

    """AGetBotList接口测试脚本"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @wraps.cases_runner
    @wraps.result_assert
    def test_bot_list(self, *args, **kwargs):
        """获取机器人列表"""
        response = kwargs.get('response')
        self.assertEqual(kwargs.get('expect_assert_value'), kwargs.get('kwassert_value'))

    @wraps.cases_runner
    @wraps.result_assert
    def test_bot_list_required_verify_TenantId(self, *args, **kwargs):
        """获取机器人列表-TenantId为空"""
        response = kwargs.get('response')
        self.assertEqual(kwargs.get('expect_assert_value'), kwargs.get('kwassert_value'))

    @wraps.cases_runner
    @wraps.result_assert
    def test_bot_list(self, *args, **kwargs):
        """获取机器人列表"""
        response = kwargs.get('response')
        self.assertEqual(kwargs.get('expect_assert_value'), kwargs.get('kwassert_value'))

    @wraps.cases_runner
    @wraps.result_assert
    def test_bot_list_required_verify_TenantId(self, *args, **kwargs):
        """获取机器人列表-TenantId为空"""
        response = kwargs.get('response')
        self.assertEqual(kwargs.get('expect_assert_value'), kwargs.get('kwassert_value'))