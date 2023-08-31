#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File    :   CommonTools.py    
@Contact :   lking@lking.icu
@Author :    Jason
@Date :      2022/4/29 15:57
@Description  Python version-3.10
常用工具类
"""


def is_empty_or_none(s):
    """
    判断字符串是否有效
    True - 无效值
    False - 有效值
    @param s: 字符串
    @return: bool
    """
    return s is None or len(s.strip()) == 0


def write_error(path, mode, text_list):
    """
    记录错误信息
    @param path:
    @param mode:
    @param text_list:
    @return:
    """
    with open(path, mode, encoding="utf-8") as f:
        f.writelines(text_list)



