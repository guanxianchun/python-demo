#!/usr/bin/env python
#-*- encoding:utf-8 -*-
import os
def convert_unicode(value):
    """
    将字符转换为Unicode格式（中文字符处理）
    @param value
    @:return 返回转换的字符串  转换失败返回None
    """
    if not isinstance(value, unicode):
        try:
            value = value.decode("utf8")
        except UnicodeDecodeError:
            try:
                value = value.decode("gbk")
            except UnicodeDecodeError:
                return None
    return value
from reportlab.platypus import doctemplate

def get_random_str(resource_str,start,end):
    import random 
    _length = random.Random().randint(start, end)
    str_leng = len(resource_str)
    ret_result = []
    for i in range(_length+1):
        ret_result.append(resource_str[random.Random().randint(0, str_leng-1)])
    return "".join(ret_result)
if __name__ == '__main__':
    s = "qwertyuioplkjhgfdsavxzmmvcx"
    print get_random_str(s, 3, 50)
    