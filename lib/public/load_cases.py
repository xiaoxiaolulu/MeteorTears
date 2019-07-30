# -*- coding:utf-8 -*-
import yaml
from os import path
from lib.utils import fp
from lib.public import logger
from lib.utils import exceptions
from config import setting
from collections import Iterable
from lib.public.Recursion import GetJsonParams
from lib.public import relevance


TestMap = {
    "api": [],
    "cases": [],
    'PWD': setting.BASE_DIR
}

ExtendCaseMap = {}

get_value = lambda seq, key: GetJsonParams.get_value(seq, key)


class LoadCase(object):

    def __init__(self, path: str = None):
        self.path = path

    def get_all_files(self) -> list:
        r"""返回文件目录路径下全部文件列表

        :Usage:
            get_all_files()
        """
        return fp.iter_files(self.path)

    @property
    def __get_files_name(self) -> list:
        r"""返回文件目录下的文件名

        :Usage:
            __get_files_name
        """
        return fp.iter_files(self.path, otype='name')

    @staticmethod
    def load_yaml_file(filepath) -> dict:
        r"""加载并读取.yaml格式文件

        :Args:
         - filepath: yaml文件路径, str object.
        """
        with open(filepath, encoding='utf-8') as stream:
            file_content = yaml.safe_load(stream)
            return file_content

    def load_file(self, file_path: str) -> dict:
        r"""加载单个.yaml测试用例文件

        :Args:
         - file_path: yaml文件路径, str object.
        """
        if not path.isfile(file_path):
            raise exceptions.CaseYamlFileNotFound("{} does not exist.".format(file_path))

        file_suffix = path.splitext(file_path)[1].lower()
        if file_suffix in ['.yaml', '.yml']:
            return self.load_yaml_file(file_path)
        else:
            err_msg = u"Unsupported file format: {}".format(file_path)
            logger.log_error(err_msg)
            return {}

    def load_files(self) -> list:
        r"""加载cases目录下的用例文件

        :Usage:
            load_files()
        """
        files_list = []
        for index, file in enumerate(self.get_all_files()):
            class_name = self.__get_files_name[index].split('.')[0].title().replace('_', '')
            try:
                with open(file, encoding='utf-8') as f:
                    files_list.append({class_name: yaml.safe_load(f)})
            except exceptions.JsonLoadingError as err:
                logger.log_error(
                    "Json file parsing error, error file: {0}, error message: {1}".format(
                        file, err))
        return files_list

    def classification_cases(self) -> tuple:
        r"""加载cases文件夹下的用例数据,并对数据进行分类
        """

        for yaml_content in self.load_files():
            _extend_cases_path = get_value(yaml_content, 'testcases')
            _extend_api_path = get_value(yaml_content, 'apipath')

            # if _extend_cases_path:
            #     TestMap['suites'].append(yaml_content)
            #     testcase_path = path.join(
            #         TestMap['PWD'],
            #         *_extend_cases_path.split('/')
            #     )
            #     test_dict = self.load_file(testcase_path)
            #     ExtendCaseMap[_extend_cases_path] = test_dict

            if _extend_api_path:
                TestMap['cases'].append(yaml_content)
                testapi_path = path.join(
                    TestMap['PWD'],
                    *_extend_api_path.split('/')
                )
                test_dict = self.load_file(testapi_path)
                ExtendCaseMap[_extend_api_path] = test_dict
            if not _extend_cases_path and not _extend_api_path:
                TestMap['api'].append(yaml_content)

        return TestMap, ExtendCaseMap

    def _case_loads_inherit_case(self) -> tuple:
        r"""对于测试用例中调用或有继承关系的yaml文件，将testapi字段的文件路径替换成具体的用例数据.
        """
        cases = {}
        cases_set, extend_cases = self.classification_cases()
        for tags in cases_set['cases']:

            for class_name, content in tags.items():
                for case_name, value in content.items():
                    extend_case_flag = get_value(tags, 'extend_api')
                    if extend_case_flag:

                        _relevance = {}
                        for extend_case in extend_case_flag:
                            extend_case_path = setting.API_PATH + extend_case + '.yaml'
                            with open(extend_case_path, encoding='utf-8') as file:
                                _relevance.update(yaml.safe_load(file))
                        relevance_body = relevance.custom_manage(str(value), _relevance, '2')
                        cases.update({class_name: {case_name: relevance_body}})
        return cases, extend_cases
        # return cases, extend_cases
        # inks, ouks, sub_key, sub_dict = [], [], [], {}
        # for case in dict(cases_set)['cases']:
        #     if isinstance(case, Iterable):
        #         for keys in dict(case).keys():
        #             ouks.append(keys)+++
        #             for cases_keys in dict(case)[keys]:
        #                 inks.append(cases_keys)
        #
        # for ink in inks:
        #     sub_key.append(dict(GetJsonParams.get_value(cases_set, ink))['testapi'])
        #
        # for key, value in dict(extend_cases).items():
        #     if key in sub_key:
        #         sub_dict.update(value)
        #
        # try:
        #     for sui_index in range(len(cases_set['cases'])):
        #         for index, ink in enumerate(inks):
        #             cases_set['cases'][sui_index][ouks[index]][ink]['testapi'] = sub_dict
        # except (KeyError, ValueError):
        #     pass

        # return cases_set, extend_cases

    def sub_case_func_params(self):
        r""" 将继承case中需要入参的参数替换params_keys中的各个值
        入参：
            params_kwargs:
                - username: tracy.liu
                - password: 12345678
        传参:
            func_params:  [username, password]
            json:
                ${username}$
                ${password}$
        """
        ncases = {
            'cases': [
            ]
        }
        api_case_set, extend_cases = self._case_loads_inherit_case()
        func_params = GetJsonParams.get_value(extend_cases, 'func_params')
        params_kwargs = GetJsonParams.get_value(api_case_set['cases'], 'params_kwargs')
        if isinstance(func_params, Iterable) and isinstance(params_kwargs, Iterable):

            for case in api_case_set['cases']:
                _relevance = {}
                for func_param in func_params:
                    _relevance.update({func_param: dict(params_kwargs)[func_param]})

                relevance_body = relevance.custom_manage(str(case), _relevance, '1')
                ncases['cases'].append(relevance_body)

            return ncases['cases']


class Containers(object):

    def __init__(self, crop: dict):
        self.crop = crop

    def __repr__(self):
        return "Containers <{}->{}>".format(
            self.crop.get('class_name'),
            self.crop.get('func_name')
        )
