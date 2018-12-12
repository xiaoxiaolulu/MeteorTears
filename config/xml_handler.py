# -*- coding:utf-8 -*-
import os
from xml.etree import ElementTree as ET


class MetaSingleton(type):

    __instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls.__instances:
            cls.__instances[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)
            return cls.__instances[cls]


class XmlHandler(metaclass=MetaSingleton):

    def __init__(self, filename: str):
        self.filename = os.fspath(filename)
        self.baseFilename = os.path.abspath(filename)

    @property
    def _getroot(self) -> str:
        """
        获取Xml节点

        :Usage:
            _getroot()
        """
        return ET.parse(self.filename).getroot()

    def get_child(self, tag: str) -> dict:
        """
        获取Xml节点属性

        :Args:
         - tag: 根据tag取一个tag下对应的子属性, STR TYPE.

        :Usage:
            get_child('emailReceivers')
        """
        elements = []
        try:
            for child in self._getroot:
                if child.tag == tag:
                    for grandchildren in child:
                        elements.append(dict(**{grandchildren.tag: grandchildren.text}))
            return {elements[0]['type']: elements[1:]}
        except (IndexError, KeyError):
            raise IndexError("The element child key is exist ")

    @property
    def get_all_receivers(self):
        """
        以列表的方式返回接收人列表

        :Usage:
            get_all_receivers()
        """
        receivers = []
        for value in self.get_child('emailReceivers')['EmailReceivers']:
            for child in value.values():
                receivers.append(child)
        return receivers


if __name__ == '__main__':
    pass
