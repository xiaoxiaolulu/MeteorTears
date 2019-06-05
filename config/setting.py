# -*- coding:utf-8 -*-
import os
import yaml
from config import xml_handler


__all__ = [
    'CONTENT',
    'HEADER',
    'EMAIL',
    'WORK_FLOW',
    'XML_CONFIG',
    'TEST_CASES',
    'TEST_SUITE',
    'Recording',
    'WECHAT',
    'CASES',
    'LOG',
    'REPORT',
    'CASES_API',
    'CASE_DATA',
    'ENV_DATA',
    'RES'
]


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRO_PATH = {}
with open(BASE_DIR + '/config/path.yaml', 'r', encoding='utf-8') as file:
    PRO_PATH.update(yaml.safe_load(file))


# 项目各项目路径
CONTENT = PRO_PATH['CONTENT']
HEADER = PRO_PATH['HEADER']
EMAIL = PRO_PATH['EMAIL']
WORK_FLOW = PRO_PATH['WORK_FLOW']
XML_CONFIG = PRO_PATH['XML_CONFIG']
TEST_CASES = PRO_PATH['TEST_CASES']
Recording = PRO_PATH['Recording']
WECHAT = PRO_PATH['WECHAT']
LOG = PRO_PATH['LOG']
REPORT = PRO_PATH['REPORT']
CASES_API = PRO_PATH['CASES_API']
TEST_SUITE = PRO_PATH['TEST_SUITE']
CASE_DATA = PRO_PATH['CASE_DATA']
ENV_DATA = PRO_PATH['ENV_DATA']
RES = PRO_PATH['RES']
CASES = PRO_PATH['CASES']


# READ_CONF
BASE_CONF = xml_handler.XmlHandler(XML_CONFIG)
BASE_EMAIL_CONF = BASE_CONF.get_child('emailSender')['EmailSender']


# EMAIL SETTING
EMAIL_CONF = dict({
    'sendaddr_name': BASE_EMAIL_CONF[0]['sendaddr_name'],
    'sendaddr_pswd': BASE_EMAIL_CONF[1]['sendaddr_pswd']
}, **{'receivers': BASE_CONF.get_all_receivers})
