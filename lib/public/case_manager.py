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
            func_name: str,
            description: str) -> None:
        """
        创建用例文件

        :Args:
         - classname: 类名&文件名, STR TYPE.
         - func_name: 函数方法名, STR TYPE.
         - description: 用例描述, STR TYPE.

        :Usage:
            make_headers_and_contents('Channel', 'add_channel', '新增渠道')
        """
        filename = setting.TEST_CASES + class_name + '.py'
        if not os.path.exists(filename):
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(self.header.format(class_name, class_name))

        with open(filename, 'a', encoding='utf-8') as file:
            file.write(self.cont.format(func_name, description))

    def create_template(self) -> types.GeneratorType:
        """
        通过文件管理器Contextor创建并关闭文件

        :Usage:
            create_template()
        """
        tags = LD.load_files()
        for items in tags:
            for class_name, body in items.items():
                if len(body):
                    for key, value in body.items():
                        func_name = key
                        description = self.get_value(value, 'description')
                        body = value
                        yield load_cases.Containers({
                            'class_name': class_name,
                            'func_name': func_name,
                            'description': description,
                            'body': body
                        }), self.make_headers_and_contents
                else:
                    for func, _body in body.items:
                        yield load_cases.Containers({
                            'class_name': class_name,
                            'func_name': func,
                            'description': self.get_value(_body, 'description'),
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
                obj.crop['func_name'],
                obj.crop['description']
            )
            cases.append(obj.crop)
            logger.log_debug(
                "测试用例已自动生成完毕, 文件: {}.py -> 具体测试用例:{}".format(
                    obj.crop['class_name'],
                    obj.crop['func_name']))

    def __iter__(self):
        return iter(self.cases)

    def __next__(self):
        return next(self.cases)

    def __repr__(self):
        return self.cases
