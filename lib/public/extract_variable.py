# -*- coding:utf-8 -*-
import os
import types
from config import setting
from lib.public import logger
from lib.public import load_cases
from lib.public.Recursion import GetJsonParams

LD = load_cases.LoadCase(setting.EXTRACT_VARIABLE)


class CreateExtractVariable(GetJsonParams):

    def __init__(self):
        self.content = None

    def __enter__(self):
        self.content = open(setting.EXTRACT_VARIABLE_TEMPLATE, encoding='utf-8')
        self.cont = self.content.read()
        return self

    def make_headers_and_contents(
            self,
            class_name: str,
            func_name: str,
            description: str) -> None:
        """
        创建临时变量文件

        :Args:
         - classname: 类名&文件名, STR TYPE.
         - func_name: 函数方法名, STR TYPE.
         - description: 用例描述, STR TYPE.

        :Usage:
            make_headers_and_contents('Channel', 'add_channel', '新增渠道')
        """
        filename = setting.EXTRACT + class_name + '.py'
        if not os.path.exists(filename):
            with open(filename, 'a', encoding='utf-8') as file:
                file.write(self.cont.format(func_name, description))

    def create_template(self) -> types.GeneratorType:
        """
        通过文件管理器创建并关闭文件

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
        self.content.close()
        del self.cont


class ExtractContainer:

    extract = []
    with CreateExtractVariable() as file:
        for items in file.create_template():
            obj, func = items
            func(
                obj.crop['class_name'],
                obj.crop['func_name'],
                obj.crop['description']
            )
            extract.append(obj.crop)
            logger.log_debug(
                "临时变量文件已自动生成完毕, 文件: {}.py -> 具体变量文件:{}".format(
                    obj.crop['class_name'],
                    obj.crop['func_name']))

    def __iter__(self):
        return iter(self.extract)

    def __next__(self):
        return next(self.extract)

    def __repr__(self):
        return self.extract
