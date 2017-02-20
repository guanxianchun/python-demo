#-*- encoding:utf-8 -*-
'''
Created on 2016年7月14日

@author: admin
'''
from hashlib import md5
import datetime,memcache
import time

class MemcacheDB(object):
    def __init__(self):
        self.mc = memcache.Client(['172.17.111.167:11211'],debug=0)
        
    def get(self,key):
        return self.mc.get(key)
    def set(self,key,value,time=0,min_compress_len=0):
        self.mc.set(key, value, time, min_compress_len)

memcachedb = MemcacheDB()
def get_index_site_id(args_name):
    return args_name.index("site_id")
    
def esdeco_gen_key(func):
    def wrapper(self, *args, **kwargs):
        #memcachedb = MemcacheDB()
        arg_names = list(func.func_code.co_varnames)[1:func.func_code.co_argcount]
        print arg_names,arg_names.index("site_id" )
        print "d----",func.__doc__
        print 'site_id=',args[arg_names.index("site_id" )]
        key="%s.%s"%(self.__class__.__name__,func.__name__)
        for arg in args:
            key += str(arg)
        _key = md5(key).hexdigest()
        result = memcachedb.get(_key)
        if result is None or not result:
            result = func(self,*args,**kwargs)
            memcachedb.set(_key,result,60*30,8)
        print  "(%s,%s)"%(_key,result)
        return result
    return wrapper

class TestDecorator(object):
    @esdeco_gen_key
    def test_decorator(self,report_id,start_time,end_time,site_id,server_id):
        print "call test_decorator..................."
        data = {"report_id":report_id,"start_time":start_time,"end_time":end_time,"site_ids":site_id,"server_ids":server_id}
        return data
    
    
import random
if __name__ == '__main__':
    count =1
    while count:
        _start_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        server_ids = random.Random().choice([1,2,3,4,5,6,7])
        _time = time.time()
        result = TestDecorator().test_decorator(1, _start_time, '2016-7-15', None,[1,2,3])
        print "main:",type(result),result
        print "time:",time.time()-_time
        result = TestDecorator().test_decorator(1, time.time(), '2016-7-15', 2, server_ids)
        print "main:",type(result),result
        count-=1
#         time.sleep(1)
    
    
