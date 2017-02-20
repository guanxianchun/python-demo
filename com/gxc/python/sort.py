#!/usr/bin/env python
#--*-- encoding:utf-8 --*--
'''
Created on 2016年5月26日

@author: admin
'''
import time
def singleton(cls, *args, **kw):  
    instances = {}  
    print 'args=',args
    def _singleton():  
        if cls not in instances:  
            instances[cls] = cls(*args, **kw)  
        return instances[cls]  
    return _singleton

@singleton  
class MyClass4(object):  
    def __init__(self, x=0):  
        self.x = x  
        
def list_dict_sort():
    _list = [{"Id":1,"client":"sdsdf","Num":2},{"Id":2,"client":"sdsddf","Num":5},{"Id":3,"client":"sdsdddf","Num":3}]
    print sorted(_list,key=lambda x:x["Num"],reverse=True)
SQL_KEY_PATTERN = "(?:%)|(?:')|(?:--)|(/\\*(?:.|[\\n\\r])*?\\*/)|(\\b(select|update|and|or|where|join|union|delete|insert|trancate|char|into|substr|ascii|order|declare|exec|count|master|into|drop|execute|load_file)\\b)"
if __name__ == '__main__':
    print '--->', '1.2.2.90' in '1.2.2.90_sadfdsf'
    list_dict_sort()
    result = None
    if not result:
        print "OOO"
    _str = str(int(time.time()*10))
    print _str,int(_str[-7:])
    time.sleep(1)
    _str = str(int(time.time()*10))
    print _str,int(_str[-7:])
    a = MyClass4(x=2)
    b = MyClass4()
    print a==b
    a.x=4
    print a.x,b.x
    pattern = "(?:')|(?:\")"
    _str = ' "-- delete '
    import  re
    if re.search( "(?:')|(?:\")", _str) and  re.search(SQL_KEY_PATTERN,_str ):
        print _str
        
        
    