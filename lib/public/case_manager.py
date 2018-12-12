# -*- coding:utf-8 -*-
import json
import types
from config import setting
from lib.public import logger
from lib.public import Recursion
from lib.public import load_cases


class CreateCase(object):

    def __init__(self):
        self.headers = None
        self.content = None

    def __enter__(self):
        self.headers = open(setting.HEADER, encoding='utf-8')
        self.header = self.headers.read()
        self.content = open(setting.CONTENT, encoding='utf-8')
        self.cont = self.content.read()
        return self

    def make_headers_and_contents(self, class_name, func_name, description) -> None:
        """老子回头在写比较恶心"""
        pass

    def create_template(self) -> types.GeneratorType:
        """老子回头在写比较恶心"""
        yield load_cases.Containers({
        }), self.make_headers_and_contents

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.headers.close()
        del self.header
        self.content.close()
        del self.cont


class TestContainer:

    cases = []
    with CreateCase() as file:
        for items in file.create_template():
            obj, func = items
            func(
                obj.crop['class_name'],
                obj.crop['func_name'],
                obj.crop['description']
            )
            cases.append(obj)

    def __iter__(self):
        return iter(self.cases)

    def __next__(self):
        return next(self.cases)

    def __repr__(self):
        return self.cases
