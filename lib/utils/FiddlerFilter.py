# -*- coding:utf-8 -*-
import os
import types
from lib.utils import fp
from config import setting
from lib.public import logger


class FiddlerFilter(object):

    def __init__(self, path: str = None):
        self.path = path
