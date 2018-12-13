# -*- coding:utf-8 -*-
import json
from urllib import parse
from requests import Session
from lib.public import logger
from lib.utils import exceptions
from lib.public.Recursion import GetJsonParams


class BaseKeyWords(GetJsonParams):

    def __init__(self, request_body: dict):
        self.session = Session()
        self.request_body = request_body

    def post(self, **kwargs: dict) -> dict:
        """
        发送POST请求。返回:class:`Response` object。

        :Args:
         - \*\*kwargs:: “session.post”接受的可选参数。

        :Usage:
            post(url='/admin/category/add', data={"name": "AUTO", "enabled": 1})
        """
        return self.session.post(**kwargs).json()

    def get(self, **kwargs: dict) -> dict:
        """
        发送GET请求。返回:class:`Response` object。

        :Args:
         - \*\*kwargs:: “session.get”接受的可选参数

        :Usage:
            get(url='/admin/category/getNames')
        """
        return self.session.get(**kwargs).json()

    def make_test_templates(self) -> dict:
        """
        创建测试用例的基础数据

        :Usage:
            make_test_templates()
        """

        logger.log_debug(self.request_body)
        method = self.request_body.get('method')

        if method in ['get', 'GET']:
            temp = ('url', 'params', 'headers')
            request_body = GetJsonParams.for_keys_to_dict(*temp, my_dict=self.request_body)
            if '=' in request_body.get('params') or '&' in request_body.get('params'):
                request_body['params'] = dict(parse.parse_qsl(request_body['params']))

            logger.log_debug("接受GET的请求参数为{}".format(
                json.dumps(request_body, indent=4, ensure_ascii=False))
            )
            return self.get(**request_body)

        if method in ['post', 'POST']:
            temp = ('url', 'headers', 'data', 'json')
            request_body = GetJsonParams.for_keys_to_dict(*temp, my_dict=self.request_body)

            logger.log_debug("接受POST的请求参数为{}".format(
                json.dumps(request_body, indent=4, ensure_ascii=False))
            )
            return self.post(**request_body)

        else:
            raise exceptions.TestApiMethodError("接口测试请求类型错误, 请检查相关用例!")


if __name__ == '__main__':
    pass
