# -*- coding:utf-8 -*-
import os
from lib.utils import time_util
from config import xml_handler
from lib.utils import security


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def make_directory(root_directory: str, extension_pattern: int, flag: 'Default False' = False) -> str:
    """
    创建目录结构

    :Args:
     - root_directory: 根目录， STR TYPE.
     - extension_pattern: 匹配子目录的索引, INT TYPE.
     - flag: 创建文件标识符, 一般默认为False, BOOLEAN TYPE.

    :Usage:
        make_directory('case', 0)
    """
    extension_root = os.path.abspath(os.path.join(BASE_DIR, root_directory))
    file_directory = [
        extension_root,
        extension_root + '/log/' + time_util.timestamp('format_day'),
        extension_root + '/report/' + time_util.timestamp('format_day'),
        extension_root + '/log/',
        extension_root + '/report/',
    ]

    if not os.path.exists(extension_root):
        os.mkdir(extension_root)

    for filename in file_directory:
        if not os.path.exists(filename) and flag is True:
            os.makedirs(os.path.abspath(filename))

    return file_directory[extension_pattern]


def document_name(extension_filename: str, filename: 'default Null' = '', flag: bool = True) -> str:
    """
    指定创建当前时间的日志文件或测试报告文件

    :Args:
     - extension_filename: 预期匹配类型文件名, STR TYPE.
     - filename: 文件名, 默认为空, STR TYPE.
     - flag: 创建文件标识符, 一般默认为True, BOOLEAN TYPE.

    :Usage:
        document_name('log')
    """
    document_index = {'log': 1, 'html': 2}
    extension_document = make_directory('report', int(document_index[extension_filename]), flag)
    filename = os.path.abspath(os.path.join(extension_document, '{0}{1}.{2}'
                                            .format(time_util.timestamp('format_now'), filename, extension_filename)))
    return filename


BASE_DATA_BASE_CONF = xml_handler.XmlHandler(make_directory('config/config.xml', 0)).get_child('mysqlTest')['mysqlTest']


DATABASE = dict(security.batch_decryption({
    'host': BASE_DATA_BASE_CONF[0]['host'],
    'port': BASE_DATA_BASE_CONF[1]['port'],
    'user': BASE_DATA_BASE_CONF[2]['user'],
    'psw': BASE_DATA_BASE_CONF[3]['password'],
    'db': BASE_DATA_BASE_CONF[4]['db'],
}), **{'charset': "utf8"})
