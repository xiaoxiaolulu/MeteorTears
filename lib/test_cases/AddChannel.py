# -*- coding:utf-8 -*-
import unittest
from lib.public import wraps


class AddChannel(unittest.TestCase):

    """AddChannel接口测试脚本"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @wraps.cases_runner
    @wraps.result_assert
    def test_channel_getchildren(self, *args, **kwargs):
        """获得子渠道"""
        response = kwargs.get('response')
        self.assertEqual(kwargs.get('expect_assert_value'), kwargs.get('kwassert_value'))

    @wraps.cases_runner
    @wraps.result_assert
    def test_channel_getchildren(self, *args, **kwargs):
        """获得子渠道"""
        response = kwargs.get('response')
        self.assertEqual(kwargs.get('expect_assert_value'), kwargs.get('kwassert_value'))

    @wraps.cases_runner
    @wraps.result_assert
    def test_channel_getchildren(self, *args, **kwargs):
        """获得子渠道"""
        response = kwargs.get('response')
        self.assertEqual(kwargs.get('expect_assert_value'), kwargs.get('kwassert_value'))