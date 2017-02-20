#--*-- encoding:utf-8 --*--
'''
Created on 2016年7月4日

@author: admin
'''

from instance import TEST_VALUR
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
def wrap_str(str_value,split_num):
    """
        按指定的字符数换行 中文算1.5个字符宽度数
    @param str_value: 要wrap的字符串
    @param split_num: 每行的字符数
    @return: 返回处理后的字符串
    """
    if not isinstance(str_value, str):
        str_value = str(str_value)
    long_str=convert_unicode(str_value)
    ret_str = ''
    index =1 
    splits = 1
    for uchar in long_str:
        if index>=split_num*splits:
            splits+=1
            ret_str+="\n"
        ret_str+=uchar
        if uchar >= u'\u4e00' and uchar<=u'\u9fa5':
            index+=1.5
        elif uchar.isdigit():
            index+=0.91
        else:
            index+=1
    return ret_str.encode("utf-8")
if __name__=="__main__":
    test = {}
    
    test["ddd"] = {"id":3}
    test["ddd"]["list"]=[2,3]
    print test,test["ddd"]["id"]