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
    'Recording',
    'EMAIL_CONF',
    'DATA_BASE_CONF',
    'WECHAT',
    'LOG',
    'REPORT',
    'CASES',
    'CASE_DATA',
    'ENV_DATA',
    'RES'
]


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRO_PATH = {}
with open(BASE_DIR + '/config/path.yaml', 'r', encoding='utf-8') as file:
    PRO_PATH.update(yaml.safe_load(file))


# project PATH
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
CASES = PRO_PATH['CASES']
CASE_DATA = PRO_PATH['CASE_DATA']
ENV_DATA = PRO_PATH['ENV_DATA']
RES = PRO_PATH['RES']


# READ CONF
BASE_CONF = xml_handler.XmlHandler(XML_CONFIG)
BASE_EMAIL_CONF = BASE_CONF.get_child('emailSender')['EmailSender']
BASE_DATA_BASE_CONF = BASE_CONF.get_child('MySqlSetting')['MySQLTest9']


# EMAIL SETTING
EMAIL_CONF = dict({
    'sendaddr_name': BASE_EMAIL_CONF[0]['sendaddr_name'],
    'sendaddr_pswd': BASE_EMAIL_CONF[1]['sendaddr_pswd']
}, **{'receivers': BASE_CONF.get_all_receivers})


# DATA SETTING
DATA_BASE_CONF = {
    'host': BASE_DATA_BASE_CONF[0]['host'],
    'port': int(BASE_DATA_BASE_CONF[1]['port']),
    'user': BASE_DATA_BASE_CONF[2]['user'],
    'passwd': BASE_DATA_BASE_CONF[3]['passwd'],
    'db': BASE_DATA_BASE_CONF[4]['db'],
    'charset': BASE_DATA_BASE_CONF[5]['charset']
}