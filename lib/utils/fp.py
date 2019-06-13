# -*- coding:utf-8 -*-
import os


def iter_files(path: str, otype='path') -> list:
    r"""返回文件目录路径中所有文件路径，以列表的形式返回.

    :Args:
     - param path: 文件路径, str object.
     - param otype: 输出返回的数据类型、默认文件路径, str object default path.

    :Usage:
        iter_files('./cases/')
    """

    filename = []

    def iterate_files(path):

        path_rest = path if not isinstance(path, bytes) else path.decode()
        abspath = os.path.abspath(path_rest)

        try:
            all_files = os.listdir(abspath)
            for items in all_files:
                files = os.path.join(path, items)
                if os.path.isfile(files):
                    filename.append(files) if otype == 'path' else filename.append(items)
                else:
                    iterate_files(files)
        except (FileNotFoundError, AttributeError, BytesWarning, IOError, FileExistsError):
            pass

    iterate_files(path)

    return filename
