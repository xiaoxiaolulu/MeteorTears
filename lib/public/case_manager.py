# -*- coding:utf-8 -*-
import os
import types
from config import setting
from lib.public import logger
from lib.public import load_cases
from lib.public.Recursion import GetJsonParams

LD = load_cases.LoadCase(setting.CASES)


class CreateCase(GetJsonParams):

    def __init__(self):
        self.headers = None
        self.content = None

    def __enter__(self):
        self.headers = open(setting.HEADER, encoding='utf-8')
        self.header = self.headers.read()
        self.content = open(setting.CONTENT, encoding='utf-8')
        self.cont = self.content.read()
        return self

    def make_headers_and_contents(
            self,
            class_name: str,
            setup: str,
            teardown: str,
            skip: str,
            func_name: str,
            description: str) -> None:
        r"""创建用例文件

        :Args:
         - classname: 测试用例文件名、等同于转化成py文件的类名(test suite), str object.
         - setup: 测试用例前置条件, str object.
         - teardown: 测试用例后置条件, str object.
         - func_name: 具体的测试用例、等同于转化成py文件的函数名(test case), str object.
         - skip: 测试用例是否跳过, str object.
         - description: 测试用例的用例描述, str object.

        :Usage:
            make_headers_and_contents('Channel', 'add_channel', '新增渠道')
        """
        filename = setting.TEST_CASES + class_name + '.py'
        if not os.path.exists(filename):
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(self.header.format(class_name, class_name, setup, teardown))

        with open(filename, 'a', encoding='utf-8') as file:
            file.write(self.cont.format(skip, func_name,  description))

    def create_template(self) -> types.GeneratorType:
        r"""通过上下文管理器读取yaml测试用例加载测试模板，自动生成unittest .py形式的case

        :Usage:
            create_template()
        """
        # tags = LD.sub_case_func_params()
        tags = LD.load_files()
        for items in tags:
            for class_name, body in items.items():
                if len(body):
                    for key, value in body.items():
                        func_name = key
                        description = self.get_value(value, 'description')
                        skip = self.get_value(value, 'skip')
                        setup = self.get_value(value, 'setUp')
                        teardown = self.get_value(value, 'tearDown')
                        body = value
                        yield load_cases.Containers({
                            'class_name': class_name,
                            'func_name': func_name,
                            'description': description,
                            'skip': bool(skip),
                            'setup': setup,
                            'teardown': teardown,
                            'body': body
                        }), self.make_headers_and_contents
                else:
                    for func, _body in body.items:
                        yield load_cases.Containers({
                            'class_name': class_name,
                            'func_name': func,
                            'description': self.get_value(_body, 'description'),
                            'skip': bool(self.get_value(_body, 'skip')),
                            'setup': self.get_value(_body, 'setUp'),
                            'teardown': self.get_value(_body, 'tearDown'),
                            'body': _body
                        })

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
                obj.crop['setup'],
                obj.crop['teardown'],
                obj.crop['skip'],
                obj.crop['func_name'],
                obj.crop['description']
            )
            cases.append(obj.crop)
            logger.log_info(
                "测试用例已自动生成完毕, 文件: {}.py -> 具体测试用例:{}".format(
                    obj.crop['class_name'],
                    obj.crop['func_name']))

    def __iter__(self):
        return iter(self.cases)

    def __next__(self):
        return next(self.cases)

    def __repr__(self):
        return self.cases
