# -*- coding:utf-8 -*-
import unittest
from lib.public import wraps


class Ksqa(unittest.TestCase):

    """Ksqa接口测试脚本"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @wraps.cases_runner
    @wraps.result_assert
    def test_ks_qa(self, *args, **kwargs):
        """快速问答某接口"""
        response = kwargs.get('response')
        print(response)
        self.assertEqual(kwargs.get('expect_assert_value'), kwargs.get('kwassert_value'))