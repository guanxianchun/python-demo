#!/usr/bin/env python
#-*- encoding:utf-8 -*-
'''

时间: 2016年11月29日 下午3:12:19
@author: guan.xianchun
'''
import pymongo,json
from bson import json_util
pymongo.command_cursor.CommandCursor 
class DBMongodb(object):
    def __init__(self):
        client = pymongo.MongoClient("mongodb://anycloud:test@172.17.21.130:27017/student")
        client.student.authenticate("anycloud","test")
        self._db = client.get_database("student")
        self._collection = self._db.get_collection("students")
    def save_student(self,dict_student):
        self._collection.insert_one(dict_student)
        
    def find_student(self,dict_filter=None):
        return self._collection.find(dict_filter)
    
    def delete_student(self,dict_fiter):
        return self._collection.delete_many(dict_fiter).deleted_count
    
    def group(self):
        self._collection.group("name",{})
        
    
if __name__ == '__main__':
    mongodb = DBMongodb()
    dict_student = {"name":"guan.xianchun","age":32}
    mongodb.save_student(dict_student)
#     print mongodb.group()
    for item in mongodb.find_student():
        print json_util.dumps(item)
        print json.loads(json_util.dumps(item))
    print mongodb.delete_student({"name":"guan.xianchun"})