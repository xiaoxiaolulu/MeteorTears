# -*- coding:utf-8 -*-
import os
import xlrd
import xlwt
from config import setting


def read_excel(file: str) -> list:
    """
    读取excel
    :Args:
     - file: 文件路径, STR TYPE.

    :Usage:
        read_excel(../data/test.json.xlsx)
    """
    workbook = xlrd.open_workbook(file)
    table = workbook.sheet_by_index(0)
    rows, cols_name, list__ = table.nrows, table.row_values(0), []

    for row in range(1, rows):
        data = table.row_values(row)

        if data:
            content = {}
            for index in range(len(cols_name)):
                content[cols_name[index]] = data[index]
            list__.append(content)

    return list__


def analyze_excel(file: str, data_index: int, excel_key: str) -> list:
    """
    分析表格中的事件, 并使用eval方法执行py代码

    :Args:
     - file: 文件路径, STR TYPE.
     - data_index: 指定数据的索引, INT TYPE.
     - excel_key: python代码数据对应的键, STR TYPE

    :Usage:
        analyze_excel('..data/test.json.xlsx', 1, 'landing_page')
    """

    data = read_excel(file)[data_index]
    function_obj = eval(data[excel_key])

    dic = {}
    for key, value in dict(data).items():
        dic[key] = value
        if key == excel_key:
            dic[key] = function_obj
    return [dic]


def save_excel(
        file: str,
        data_index: int,
        excel_key: str,
        excel_name: str = 'copy_excel'):
    """
    分析表格后得到新的数据,并写入一份副本文件

    :Args:
     - file: 文件路径, STR TYPE.
     - data_index: 指定数据的索引, INT TYPE.
     - excel_key: python代码数据对应的键, STR TYPE
     - excel_name: 复制的文件名, 默认为copy_excel, STR TYPE.

    :Usage:
        save_excel('../data/test.json.xlsx', 2, 'landing_page', 'test.json-副本.xlsx')
    """
    excel_copy = os.path.join(setting.DATA, 'copy_excel')
    workbook = xlwt.Workbook(encoding='utf-8')
    table, data = workbook.add_sheet(u"sheet1", cell_overwrite_ok=True), analyze_excel(file, data_index, excel_key)

    copy_data, k_data, v_data = [], [], []
    for index, value in enumerate(data):
        for k, v in value.items():
            k_data.append(k), v_data.append(v)
    copy_data.append(k_data)
    copy_data.append(v_data)

    for i, j in enumerate(copy_data):
        for q, p in enumerate(j):
            table.write(i, q, str(p))
    workbook.save(os.path.join(excel_copy, excel_name))


if __name__ == '__main__':
    pass
