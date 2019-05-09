# -*- coding:utf-8 -*-
import os
import yaml
from config import xml_handler


__all__ = [
    'CONTENT_TEMPLATE_PATH',
    'HEADER_TEMPLATE_PATH',
    'EMAIL_TEMPLATE_PATH',
    'WORK_FLOW_CASE_PATH',
    'XML_CONFIG_PATH',
    'TEST_CASES_PATH',
    'FIDDLER_CASES_PATH',
    'WECHAT',
    'LOG_PATH',
    'REPORT_PATH',
    'CASES_PATH',
    'DATA_PATH',
    'PUBLIC_RES',
    'EXTRACT',
]


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRO_PATH = {}
with open(BASE_DIR + '/config/path.yaml', 'r', encoding='utf-8') as file:
    PRO_PATH.update(yaml.load(file, Loader=yaml.FullLoader))


# 项目各项目路径
CONTENT_TEMPLATE_PATH = PRO_PATH['CONTENT_TEMPLATE_PATH']
HEADER_TEMPLATE_PATH = PRO_PATH['HEADER_TEMPLATE_PATH']
EMAIL_TEMPLATE_PATH = PRO_PATH['EMAIL_TEMPLATE_PATH']
WORK_FLOW_CASE_PATH = PRO_PATH['WORK_FLOW_CASE_PATH']
XML_CONFIG_PATH = PRO_PATH['XML_CONFIG_PATH']
TEST_CASES_PATH = PRO_PATH['TEST_CASES_PATH']
FIDDLER_CASES_PATH = PRO_PATH['FIDDLER_CASES_PATH']
WECHAT = PRO_PATH['WECHAT']
LOG_PATH = PRO_PATH['LOG_PATH']
REPORT_PATH = PRO_PATH['REPORT_PATH']
CASES_PATH = PRO_PATH['CASES_PATH']
DATA_PATH = PRO_PATH['DATA_PATH']
PUBLIC_RES = PRO_PATH['PUBLIC_RES']
EXTRACT = PRO_PATH['EXTRACT']


# READ_CONF
BASE_CONF = xml_handler.XmlHandler(XML_CONFIG_PATH)
BASE_EMAIL_CONF = BASE_CONF.get_child('emailSender')['EmailSender']


# EMAIL SETTING
EMAIL_CONF = dict({
    'sendaddr_name': BASE_EMAIL_CONF[0]['sendaddr_name'],
    'sendaddr_pswd': BASE_EMAIL_CONF[1]['sendaddr_pswd']
}, **{'receivers': BASE_CONF.get_all_receivers})
