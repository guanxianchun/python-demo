#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2016年7月25日

@author: admin
'''
import random, decimal, uuid, string,socket
from urllib import urlencode

def random_string(start,end):
    return "ssssssssss"

def random_strname(randstr,start,end):
    randnum = str(random.randint(start,end))
    print randnum,len(randstr)
    print random.sample(randstr, randnum)
    teststrname = string.join(random.sample(randstr, randnum))
    return teststrname    
    
def save_data_2(dict_data):
    print dict_data
def get_mac_from_hex_value(hexvalue):
        """
        将十六进制的MAC地址转换成MAC地址
        @param hexvalue: 十六进制的MAC地址  如：0xd8490bc7713f
        """
        mac_result = ''
        if hexvalue is None or not hexvalue:
            return mac_result
        if re.match(pattern, hexvalue) is not None:
            index = 1
            for char in hexvalue[2:]:
                mac_result+=char.upper()
                if index%2 ==0:
                    mac_result+=":"
                index+=1
        if len(mac_result)>0:
            return mac_result[:-1]
        return mac_result
if __name__ == '__main__':
    random.seed(1)
    print random.random()
    print random.random()
    print random.random()
    print random.random()
    data=1024
    print data >> 8
    data_size = decimal.Decimal("2.3698514524521")
    size = data_size.quantize(decimal.Decimal("0.%s"%("0"*4)))
    print size
    dict_data = {"userId":"dsfds","userName":"gxc"}
    func_str = 'save_data_%s(dict_data)' % (2)
    print func_str
    eval(func_str)
    print 35+60+45+40+40+45+35+35+35+35+35+35+30
    print 30+70+55+45+45+45+30+30+30+30+30+30+30
    {}
    encode_str = urlencode({"file":"睦"})
    print  encode_str.split("=")[1]
    import re
    
    pattern = r'^0x(\w)*'
    mac_src = '0xd8490bc77140'
    print get_mac_from_hex_value(mac_src)
    
    print unicode(uuid.uuid1().hex)
    tenant_type=0
    if not(tenant_type == (1,0) or tenant_type == (2,'H3C',1)):
        print "*********dddddd*****"
    random_strname("ssssssss",2,3)