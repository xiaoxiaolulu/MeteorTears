import yaml
from os import path
from config import setting
from lib.utils import fp
from lib.public import logger
from lib.utils import exceptions
from collections import Iterable
from lib.public import relevance
from lib.public.Recursion import GetJsonParams


class Loader(object):

    def __init__(self, filepath: str = None):
        self.filepath = filepath

    @staticmethod
    def get_filename(pwd: str) -> list:
        r"""以列表的形式获取文件路径

        :Args:
         - pwd: 文件根目录, str object.
        :return: 以list的数据类型返回文件路径
        :rtype: list object.
        """
        try:
            filename = fp.iter_files(pwd)
            return filename
        except exceptions.CaseYamlFileNotFound:
            logger.log_warn('目录文件不存在.')

    @staticmethod
    def get_yaml_content(filepath: str) -> list:
        r"""读取yaml文件中的内容，以列表的形式返回

        :Args:
         - filepath: yaml 文件路径, str object.
        :return: 以list的数据类型返回yaml文件中的数据
        :rtype: list object.
        """
        try:
            with open(filepath, encoding='utf-8') as stream:
                yaml_content = yaml.safe_load(stream)
                return yaml_content
        except exceptions.CaseYamlFileNotFound:
            logger.log_warn('读取的yaml用例文件 -> {} 不存在,请查看'.format(filepath))

    def classification_cases(self) -> dict:
        r"""对测试数据进行类别分类, 并对yaml文件中存在继承关系的文件路径\n
        替换成实际的数据。

        :return: 返回处理完成的测试用例集
        :rtype: dict object.
        """

        def get_case_content(filepath: str) -> tuple:
            r"""获取遍历文件内容，以tuple类型数据返回.

            :Args:
             - filepath: 遍历文件路径
            """
            collection = {}
            path = self.get_filename(filepath)
            if isinstance(path, Iterable):
                for yaml_path in path:
                    classname = yaml_path.split('/')[-1].split('.')[0]
                    yaml_content = self.get_yaml_content(yaml_path)
                    collection.update({classname: yaml_content})
            return classname, collection

        """加载api文件数据"""
        api_name, api_content = get_case_content(setting.API_PATH)

        """加载case文件数据"""
        case_name, case_content = get_case_content(setting.TEST_CASE)

        # 对case中存在依赖关系的文件路径,替换成实际用例数据.
        for case_filename, cases in case_content.items():
            for index, case in enumerate(cases):
                for func_name, func_value in case.items():
                    for body_key, body_value in func_value.items():
                        if body_key == 'testapi':
                            be_related = body_value.split('/')[-1].split('.')[0]
                            func_value[body_key] = api_content[be_related]
                        else:
                            func_value[body_key] = body_value
        return case_content

    def sub_case_func_params(self):
        cases = self.classification_cases()
        for classname, case_content in cases.items():
            for func in case_content:
                for func_name, func_content in func.items():

                    request_body = GetJsonParams.get_value(func_content['testapi'][0], 'request_body')
                    func_params = dict(request_body).get('func_params')

                    if func_params:
                        if isinstance(func_params, list):

                            _relevance = {}
                            for func_param in func_params:
                                _relevance.update({func_param: GetJsonParams.get_value(func, 'params_kwargs')})

                            relevance_body = relevance.extend_cases_manage(str(request_body), _relevance)
                            print(request_body)


if __name__ == '__main__':
    l = Loader()
    l.sub_case_func_params()
