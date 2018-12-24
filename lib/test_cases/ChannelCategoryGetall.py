# -*- coding:utf-8 -*-
import unittest
from lib.public import wraps


class ChannelCategoryGetall(unittest.TestCase):

    """ChannelCategoryGetall接口测试脚本"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @wraps.cases_runner
    @wraps.result_assert
    def test_channel_category_getall(self, *args, **kwargs):
        """获取渠道分类"""
        response = kwargs.get('response')
        self.assertEqual(kwargs.get('expect_assert_value'), kwargs.get('kwassert_value'))

    @wraps.cases_runner
    @wraps.result_assert
    def test_channel_category_getall(self, *args, **kwargs):
        """获取渠道分类"""
        response = kwargs.get('response')
        self.assertEqual(kwargs.get('expect_assert_value'), kwargs.get('kwassert_value'))