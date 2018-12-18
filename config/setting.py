# -*- coding:utf-8 -*-
from config import xml_handler
from lib.utils import security
from lib.utils import time_util


__all__ = [
    'CONTENT_TEMPLATE_PATH',
    'HEADER_TEMPLATE_PATH',
    'EMAIL_TEMPLATE_PATH',
    'XML_CONFIG_PATH',
    'TEST_CASES_PATH',
    'LOG_FILE_NAME',
    'REPORT_PATH',
    'CASES_PATH',
    'DATA_PATH'
]


# ALL PATHS
LOG_FILE_NAME = 'report/log/Mar-{}.log'.format(time_util.timestamp('format_now'))
CONTENT_TEMPLATE_PATH = 'lib/template/content_template'
HEADER_TEMPLATE_PATH = 'lib/template/header_template'
EMAIL_TEMPLATE_PATH = 'lib/template/email_template'
XML_CONFIG_PATH = 'config/config.xml'
TEST_CASES_PATH = 'lib/test_cases/'
LOG_PATH = 'report/log/'
REPORT_PATH = 'report/'
CASES_PATH = 'cases/'
DATA_PATH = 'data/'


# READ_CONF
BASE_CONF = xml_handler.XmlHandler(XML_CONFIG_PATH)
BASE_DATA_CONF = BASE_CONF.get_child('mysqlTest')['mysqlTest']
BASE_EMAIL_CONF = BASE_CONF.get_child('emailSender')['EmailSender']


# MYSQL SETTING
DATABASE = dict(security.batch_decryption({
    'host': BASE_DATA_CONF[0]['host'],
    'port': BASE_DATA_CONF[1]['port'],
    'user': BASE_DATA_CONF[2]['user'],
    'psw': BASE_DATA_CONF[3]['password'],
    'db': BASE_DATA_CONF[4]['db'],
}), **{'charset': "utf8"})


# EMAIL SETTING
EMAIL_CONF = dict(security.batch_decryption({
    'sendaddr_name': BASE_EMAIL_CONF[0]['sendaddr_name'],
    'sendaddr_pswd': BASE_EMAIL_CONF[1]['sendaddr_pswd']
}), **{'receivers': security.batch_decryption(BASE_CONF.get_all_receivers)})
