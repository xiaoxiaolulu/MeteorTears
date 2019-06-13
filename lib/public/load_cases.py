# -*- coding:utf-8 -*-
import yaml
from lib.utils import fp
from lib.public import logger
from lib.utils import exceptions


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


class Containers(object):

    def __init__(self, crop: dict):
        self.crop = crop

    def __repr__(self):
        return "Containers <{}->{}>".format(
            self.crop.get('class_name'),
            self.crop.get('func_name')
        )
