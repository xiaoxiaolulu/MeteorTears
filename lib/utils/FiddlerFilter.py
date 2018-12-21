# -*- coding:utf-8 -*-
import os
import types
from config import setting
from lib.public import logger


class FiddlerFilter(object):

    def __init__(self):
        self.request = None
        self.response = None

    def __enter__(self):
        self.request = open(setting.FIDDLER_REQUEST, encoding='utf-8')
        self.request.read()
        self.response = open(setting.FIDDLER_RESPONSE, encoding='utf-8')
        self.response.read()

    def __filter_request(self):
        pass

    def __distinct_request(self):
        pass

    def __diff_request_api(self):
        pass

    def make_request_template(self):
        pass

    def init_fiddler_files(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.request.close()
        del self.request
        self.response.close()
        del self.response


class ApiWorkFlowPool:

    pass
