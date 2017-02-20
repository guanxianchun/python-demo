#-*- encoding:utf-8 -*-
'''
Created on 2016年7月12日

@author: admin
'''
import memcache
from hashlib import md5

#!/usr/bin/env python

# 20140105,  conn_mysql.py

import MySQLdb
import hashlib,zlib,uuid,random,json

def zlib_compress(raw_data):
    """
        采用zlib压缩数据
    @param raw_data: 原始字符串数据
    @return: 返回压缩后的数据
    """
    try:
        return zlib.compress(raw_data)
    except:
        return raw_data

def zlib_decompress(zb_data):
    """
        采用zlib解压缩数据
    @param raw_data: 压缩数据
    @return: 返回解压缩后的数据
    """
    try:
        return zlib.decompress(zb_data)
    except:
        return zb_data
    
class MysqlConnection(object):
    def __init__(self):
        self.conn=MySQLdb.connect(host='172.17.111.167',user='anycloud',passwd='P@sswd4Eis00',db='anycloud',port=3306)
    
    def __del__(self):
        if self.conn:
            self.conn.close()
            
    def insert(self,report_id,report_uuid,json_data):
        data={
              "f_report_id":report_id,
              "f_report_uuid":report_uuid,
              "f_content":json_data,
            }
        self._insert("t_report_json_data",data)
        
    def _insert(self, table, columns):
        """
        插入一条数据
        Args:
            table: string，要插入的表名
            columns: dict or list，要插入值的列以及值
                     如果是字典，键为列名
                     如果是列表，元素为值
        Return:
            最后一个插入语句的自增ID，如果没有则为0
        Raise:
            TypeError: 参数类型错误时丢出异常
        Example:
            insert("test_table", {"id": 1, "name": "test"})
            => INSERT INTO `test_table` (`id`, `test`) VALUES ("1", "test")
            insert("test_table", [1, "test"])
            => INSERT INTO `test_table` VALUES ("1", "test")
        """
        values=""
        try:
            if not isinstance(table, basestring):
                raise TypeError("table only use string type")

            sql = ["INSERT INTO `{0}` ".format(table)]

            if isinstance(columns, dict):
                sql.append(self.__get_columns(columns.keys()))
                values = columns.values()
            elif isinstance(columns, list):
                values = columns
            else:
                raise TypeError("columns only use list or dict type")
            sql.append(" VALUES (%s) " % (", ".join(["%s"] * len(values))))
            cursor = self.conn.cursor()
            cursor.execute("".join(sql), values)
            last_id = cursor.lastrowid
            self.conn.commit()
            cursor.close()
            return last_id            
        except Exception:
            print "execute sql error,sql:%s. args:%s" %(sql,values)
    
    @classmethod      
    def __get_columns(cls, columns):
        """
        将列名列表转换为字符串
        Args:
            columns: list，列名
        Return:
            字符串，例如：
            __get_columns(["id", "name"])
            => (`id`, `name`)
        """
        stmt = ["`%s`" % c for c in columns]
        return " (%s) " % (", ".join(stmt))
class conn_mysql(object):
    def __init__(self):
        print "init mysql"

    def __del__(self):
        print "quit mysql"

    def connect_db(self):
        self.conn=MySQLdb.connect(host='172.17.111.167',user='anycloud',passwd='P@sswd4Eis00',db='anycloud',port=3306)
        self.cur=self.conn.cursor()
        self.conn.select_db('anycloud')

    def test_select(self):
        count=self.cur.execute('select f_user_id,f_login_name from t_user')
        print 'there has %s rows record' % count
 
        result=self.cur.fetchone()
        print result
        print 'ID: %s info %s' % result
 
        results=self.cur.fetchmany(5)
        for r in results:
            print r

        print '=='*10
        self.cur.scroll(0,mode='absolute')

        results=self.cur.fetchall()
        for r in results:
            print r[1]
 
        self.conn.commit()

    def test_count(self, str_sql):
        count=self.cur.execute(str_sql)
        # print 'there has %s rows record' % count

        result=self.cur.fetchone()
        # print 'id_info has %s rows' % result
        str_rows = '%s' % result
        return str_rows

    def connect_cache(self):
        self.mc = memcache.Client(['172.17.111.167:11211'],debug=0)

    def test_count_cached(self, str_sql):
        str_hash = hashlib.md5(str_sql).hexdigest()
        #str_hash = myhash(str_sql)
        print str_hash
        result = self.mc.get(str_hash)
        print result
        if result != None:
            return result
        print "*"*50
        count = self.cur.execute(str_sql)
        # print 'there has %s rows record' % count

        result = self.cur.fetchone()
        self.mc.set(str_hash, result,60*2)
        self.mc.set('SQL'+str_hash, str_sql)
        print(str_hash)
        # print 'id_info has %s rows' % result
        return result

    def disconnect_db(self):
        self.cur.close()
        self.conn.close()
        
if __name__ == '__main__':
    _db = MysqlConnection()
    for i in range(200000):
        dict_data = [{"Count": i%20000, "List": [{"AllTimes": i%20000, 
                        "DestServerType": 3, "BackupNodeName": "localhost111.188", "DestServerIP": "172.17.111.188", 
                        "DataSourceType": "1", "PartSuccess": 0, "SuccessAlarm": 0, "FailTimes": 0, "StoppedTimes": 0, 
                        "DestServerName": "172.17.111.188", "SourceServerName": "ADMIN-PC", "SuccessScale": "0.00%", 
                        "SourceServerIP": "172.17.111.155", "TaskID": 1, "TaskType": 1, "SuccessTimes": 0, "TaskName": "412123123123123", 
                        "DisasterServerName": None, "SourceServerType": 4, "MonitorTaskID": 1}]}]
        report_uuid = hashlib.md5("%s_%s_%s"%(i%20000,str(uuid.uuid1()),random.Random().randint(1, 1000))).hexdigest()
        _db.insert(i%20000, report_uuid, json.dumps(dict_data))
#     mc = memcache.Client(['172.17.111.167:11211'],debug=0)
#     print mc
#     sql = "select * from test.demo_test"
#     _key = md5(sql)
#     print _key
#     mc.set('name','luo',60)
#     mc.set('student','{name:gxc,age:31}',60)
#     import time
#     _start = time.time()
#     result = mc.get(key="student")
#     print time.time()-_start
#     print result
#     str_sql = 'select * from t_user where f_login_name="audit"'
# 
# 
#     db_connect = conn_mysql()
#     db_connect.connect_db()
#     db_connect.connect_cache()
#     str_rows = db_connect.test_count_cached(str_sql)
#     print "result is tuple:", isinstance(str_rows,tuple)
#     db_connect.disconnect_db()