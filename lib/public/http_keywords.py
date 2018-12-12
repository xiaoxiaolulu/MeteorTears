# -*- coding:utf-8 -*-
import json
from requests import Session
from lib.public import logger
from lib.public.Recursion import GetJsonParams


class BaseKeyWords(GetJsonParams):

    def __init__(self, request_body: dict):
        self.session = Session()
        self.request_boy = request_body

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

        logger.log_debug(self.request_boy)
        logger.log_info("接受的请求方式 {}, 请求参数为{}".format(
            self.request_boy.get('method'), json.dumps(self.request_boy, indent=4, sort_keys=True, ensure_ascii=False))
        )


if __name__ == '__main__':
    pass
