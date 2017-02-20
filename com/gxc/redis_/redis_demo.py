# /usr/bin/env python
# -*- encoding:utf-8 -*-
'''
Created on 2016年7月18日

@author: admin
'''
import redis, uuid, json, zlib
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

def get_all_datas(_redis_conn):
    keys = _redis_conn.keys()
    for key in keys:
        print key,' = ',zlib_decompress(_redis_conn.get(key))
        
def set_data(_redis_conn,key,raw_data):
    _redis_conn.set(key,zlib_compress(raw_data))
    
if __name__ == '__main__':
    import gzip, cPickle, StringIO
    host = "172.17.112.242"
    #host = "172.17.111.167"
    pool = redis.ConnectionPool(host=host, port=6379, db=0, password="P@sswd4Eis00")

    r = redis.Redis(connection_pool=pool)
    for _del_item in r.keys("8:*"):
        r.delete(_del_item)
        
    get_all_datas(r)
    for i in range(400):
        dict_data = [{"Count": 3, "List": [{"AllTimes": 1, "DestServerType": 3, "BackupNodeName": "localhost111.188", "DestServerIP": "172.17.111.188", "DataSourceType": "1", "PartSuccess": 0, "SuccessAlarm": 0, "FailTimes": 0, "StoppedTimes": 0, "DestServerName": "172.17.111.188", "SourceServerName": "ADMIN-PC", "SuccessScale": "0.00%", "SourceServerIP": "172.17.111.155", "TaskID": 1, "TaskType": 1, "SuccessTimes": 0, "TaskName": "412123123123123", "DisasterServerName": None, "SourceServerType": 4, "MonitorTaskID": 1}]}]
        set_data(r, "2:0b3d75ead0dd1bbd3bf916e156cec983c18%s"%(i), json.dumps(dict_data))
