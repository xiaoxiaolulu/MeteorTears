# -*- coding:utf-8 -*-
import unittest
from lib.public import wraps


class ChannelGetlist(unittest.TestCase):

    """ChannelGetlist接口测试脚本"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @wraps.cases_runner
    @wraps.result_assert
    def test_channel_getlist(self, *args, **kwargs):
        """获取渠道列表数据"""
        response = kwargs.get('response')
        self.assertEqual(kwargs.get('expect_assert_value'), kwargs.get('kwassert_value'))

    @wraps.cases_runner
    @wraps.result_assert
    def test_channel_getlist(self, *args, **kwargs):
        """获取渠道列表数据"""
        response = kwargs.get('response')
        self.assertEqual(kwargs.get('expect_assert_value'), kwargs.get('kwassert_value'))

    @wraps.cases_runner
    @wraps.result_assert
    def test_channel_getlist(self, *args, **kwargs):
        """获取渠道列表数据"""
        response = kwargs.get('response')
        self.assertEqual(kwargs.get('expect_assert_value'), kwargs.get('kwassert_value'))