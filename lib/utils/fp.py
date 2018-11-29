# -*- coding:utf-8 -*-
import os


def iter_files(path):
    """
    返回文件目录路径下全部文件列表

    :Args:
     - path: 文件路径, STR TYPE.

    :Usage:
        iter_files(’../case/')
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
                    filename.append(files)
                else:
                    iterate_files(files)
        except (FileNotFoundError, AttributeError, BytesWarning, IOError, FileExistsError):
            pass
    iterate_files(path)
    return filename
