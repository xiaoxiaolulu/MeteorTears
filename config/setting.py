# -*- coding:utf-8 -*-
import os
import yaml
from config import xml_handler


__all__ = [
    'EXTRACT_VARIABLE_TEMPLATE',
    'CONTENT_TEMPLATE_PATH',
    'HEADER_TEMPLATE_PATH',
    'EMAIL_TEMPLATE_PATH',
    'WORK_FLOW_CASE_PATH',
    'XML_CONFIG_PATH',
    'TEST_CASES_PATH',
    'FIDDLER_CASES_PATH',
    'WECHAT',
    'EXTRACT_VARIABLE',
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
    PRO_PATH.update(yaml.load(file))


# 项目各项目路径
EXTRACT_VARIABLE_TEMPLATE = PRO_PATH['EXTRACT_VARIABLE_TEMPLATE']
CONTENT_TEMPLATE_PATH = PRO_PATH['CONTENT_TEMPLATE_PATH']
HEADER_TEMPLATE_PATH = PRO_PATH['HEADER_TEMPLATE_PATH']
EMAIL_TEMPLATE_PATH = PRO_PATH['EMAIL_TEMPLATE_PATH']
WORK_FLOW_CASE_PATH = PRO_PATH['WORK_FLOW_CASE_PATH']
XML_CONFIG_PATH = PRO_PATH['XML_CONFIG_PATH']
TEST_CASES_PATH = PRO_PATH['TEST_CASES_PATH']
FIDDLER_CASES_PATH = PRO_PATH['FIDDLER_CASES_PATH']
WECHAT = PRO_PATH['WECHAT']
EXTRACT_VARIABLE = PRO_PATH['EXTRACT_VARIABLE']
LOG_PATH = PRO_PATH['LOG_PATH']
REPORT_PATH = PRO_PATH['REPORT_PATH']
CASES_PATH = PRO_PATH['CASES_PATH']
DATA_PATH = PRO_PATH['DATA_PATH']
PUBLIC_RES = PRO_PATH['PUBLIC_RES']
EXTRACT = PRO_PATH['EXTRACT']


# READ_CONF
BASE_CONF = xml_handler.XmlHandler(XML_CONFIG_PATH)
BASE_DATA_CONF = BASE_CONF.get_child('sqlTest')['sqlTest']
BASE_EMAIL_CONF = BASE_CONF.get_child('emailSender')['EmailSender']


# MYSQL SETTING
DATABASE = dict({
    'host': BASE_DATA_CONF[0]['host'],
    'user': BASE_DATA_CONF[1]['user'],
    'psw': BASE_DATA_CONF[2]['password'],
    'db': BASE_DATA_CONF[3]['db'],
}, **{'charset': "utf8"})


# EMAIL SETTING
EMAIL_CONF = dict({
    'sendaddr_name': BASE_EMAIL_CONF[0]['sendaddr_name'],
    'sendaddr_pswd': BASE_EMAIL_CONF[1]['sendaddr_pswd']
}, **{'receivers': BASE_CONF.get_all_receivers})
