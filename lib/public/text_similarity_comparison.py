# -*- coding:utf-8 -*-
import jieba
from collections import Counter
import numpy as np
import math
from lib.public import logger
from config import setting
from os import path


def stopwords(seg_list: list) -> list:
    r"""过滤掉文本中的停用词, 停用词路径：/data/env_data/stopKeywords/

    :Args:
     - seg_list: 使用JieBa分词后对待测试文本进行分词后得到的一个列表对象, list object.
    """
    stayed_word = []

    filter_keywords = open(path.join(setting.ENV_DATA, 'stopKeywords'), 'r', encoding='utf-8')
    stop_key = [line.strip() for line in filter_keywords.readlines()]
    for word in seg_list:
        if word not in stop_key:
            stayed_word.append(word)
    return stayed_word


def count(res: str):
    r"""待测试文本进行分词后，统计得出词频。

    :Args:
     - res: 待测试文本关键字, str object.
    """
    seg_list = list(jieba.cut(res))
    seg_list = stopwords(seg_list)
    dic = Counter(seg_list)

    return (dic)


def merge_word(expect: dict, res: dict) -> list:
    r"""关键词合并单词.

    :Args:
     - expect: 预期待测文本值, dict object.
     - res: Response返回预对比值, dict object.
    """
    return list(set(list(expect.keys())).union(set(list(res.keys()))))


def cal_vector(expect: dict, merge_word: list) -> list:
    r"""获取文本向量值

    :Args:
     - expect: 预期待测文本值,, dict object.
     - merge_word: 关键词合并单词., list object.
    """
    vector = []
    for ch in merge_word:
        if ch in expect:
            vector.append(expect[ch])
        else:
            vector.append(0)
    return vector


def cal_con_dis(v1: list, v2: list, length_vector):
    r"""计算余弦距离.

    :Args:
     - v1: 预期的向量, list object.
     - v2: 实际的向量, list object.
     - length_vector: 向量的长度, list object.
    """
    a1 = np.asarray(v1)
    a2 = np.asarray(v2)
    A = math.sqrt(np.sum(a1**2)) * math.sqrt(np.sum(a1**2))
    B = np.sum(a1 * a2)

    try:
        return format(float(B) / A, ".3f")
    except ZeroDivisionError:
        return 0


def contrast_num(expected_knowledge, actual_knowledge) -> float:
    r"""得出计算对比度

    :Args:
     - expected_knowledge: 预期的待测试文本, str object.
     - actual_knowledge: 实际Response返回文本, str object.
    """
    expect, res = count(expected_knowledge), count(actual_knowledge)
    merge = merge_word(expect, res)
    v1, v2 = cal_vector(expect, merge), cal_vector(res, merge)
    diff = round(float(cal_con_dis(v2, v1, len(merge))), 4)
    logger.log_info('{}{}{}'.format(expect, res, diff))
    return diff
