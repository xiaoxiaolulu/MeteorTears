# -*- coding:utf-8 -*-
import re
import yaml
import types
from lib.utils import fp
from yaml import scanner


class LoadFiddlerFiles(object):

    def __init__(self, path: str = None):
        self.path = path

    @property
    def get_file_list(self) -> list:
        """
        获取WorkFlow目录下所有文件
        :return:
        """
        return fp.iter_files(self.path)

    @staticmethod
    def __match_files(re_pattern, request_url):
        """
        匹配有效接口文件, 匹配不成功返回None

        :Args:
         - request_url:  匹配的路由, STR TYPE.

        :Usage:
            match_files('/admin/ConfigInfo')
        """
        http_url_regexp = re.compile(re_pattern, re.I)
        return http_url_regexp.match(request_url)

    def loads_fiddler_request(self) ->types.GeneratorType:
        """
        加载录制的接口文件,并生成新的可迭代对象, 自动过滤错误的yaml文件对象

        :Usage:
            loads_fiddler_request()
        """

        for files in fp.iter_files(self.path):
            try:
                with open(files, 'r', encoding='utf-8') as file:
                    if 'Content-Type' not in file.read():
                        with open(files, 'a', encoding='utf-8') as wf:
                            wf.write(
                                'Content-Type: application/json;charset=UTF-8')

                with open(files, 'r', encoding='utf-8') as file:
                    content = yaml.load(file)
                    request_url = content['Request url']
                    request_type = content['Request header'][:4]
                    request_api = content['Request header'][4:].replace('HTTP/1.1', '')
                    class_name = (request_api.split('/')[-2] + '_' + request_api.split('/')[-1]).strip().title()
                    content_type = content['Content-Type']
                    request_body = content['Request body']
                    authorization = content['Authorization']
                    yield {
                        'class_name': class_name,
                        'request_url': request_url,
                        'request_type': request_type,
                        'content_type': content_type,
                        'request_body': request_body,
                        'authorization': authorization
                    }
            except scanner.ScannerError:
                continue


if __name__ == '__main__':
    pass
