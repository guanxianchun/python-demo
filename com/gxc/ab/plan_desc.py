#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2016年7月25日

@author: admin
'''
import time,datetime
WEEK_DESC={0x01:"星期天",0x02:"星期一",0x04:"星期二",0x08:"星期三",0x10:"星期四",0x20:"星期五",0x40:"星期六"}
WEEK={1}
DAYS_OF_MONTH = [0x00000000, 0x00000001, 0x00000002, 0x00000004,
                                0x00000008, 0x00000010, 0x00000020, 0x00000040,
                                0x00000080, 0x00000100, 0x00000200, 0x00000400,
                                0x00000800, 0x00001000, 0x00002000, 0x00004000,
                                0x00008000, 0x00010000, 0x00020000, 0x00040000,
                                0x00080000, 0x00100000, 0x00200000, 0x00400000,
                                0x00800000, 0x01000000, 0x02000000, 0x04000000,
                                0x08000000, 0x10000000, 0x20000000, 0x40000000];
MONTH_CODE=[0x00,0x01, 0x02, 0x04,
                                0x08, 0x10, 0x20, 0x40,
                                0x80, 0x100, 0x200, 0x400,
                                0x800,0x1000]
UNIT_CODE={1:"月",2:"周",3:"天",4:"时",5:"分"}

def time_to_str(source_time,format='%Y-%m-%d %H:%M:%S'):
    """
    将时间对象转换成字符串(包括timestamp时间戳)，默认格式为：年-月-日 时:分:秒
    @:param source_time 时间对象
    @:return 返回时间字符
    """
    if isinstance(source_time, float) or isinstance(source_time, long) or isinstance(source_time, int):
        return time.strftime(format,time.localtime(source_time))
    elif isinstance(source_time, (datetime.datetime,datetime.date)):
        return source_time.strftime(format)
    else:
        return str(source_time)
def get_week_days(value):
    values=""
    keys = sorted(WEEK_DESC.keys())
    for _item in keys:
        if _item & value:
            values+="%s , "%(WEEK_DESC[_item])
    return values[:-2]
    if value is None or not values:
        return ""
    week_days = ""
    for _value in values:
        week_days+="%s,"%(WEEK_DESC[int(_value)])
    return week_days[:-1]
    
def get_days_month(value):
    values = ""
    for _item in DAYS_OF_MONTH:
        if _item & value:
            values+="%s,"%(DAYS_OF_MONTH.index(_item))
    return values[:-1]
    
def get_months(value):
    values = ""
    _value=0
    for _item in MONTH_CODE:
        if _item & value:
            _value += value|_item
            values+="%s,"%(MONTH_CODE.index(_item))
    return values[:-1]

def get_plan_desc(plan_type,interval_unit,interval_value,value,start_time,backup_type,
                  senior_interval_unit=None,senior_interval_value=None,
                  duration_unit=None,duration_value=None):
    _desc =""
    if plan_type ==1:
        _desc+="一次性"
    elif plan_type ==2:
        if interval_unit==1:
            _desc="%s%s%s"%("每",get_months(interval_value),UNIT_CODE[interval_unit])
            if value:
                _desc+="%s%s%s"%("(",get_days_month(value),"日)")
        if interval_unit==2:    
            _desc="%s%s%s"%("每",interval_value,"周")
            _desc+="%s%s%s"%("(",get_week_days(value),")")
        if interval_unit ==3:
            _desc+="%s%s%s"%("每",interval_value,"天")
    elif plan_type==3:
        if interval_unit==2:    
            _desc="%s%s%s"%("每",interval_value,"周")
            _desc+="%s%s%s"%("(",get_week_days(value),")")
    _desc +=",%s：%s"%("开始时间",time_to_str(long(start_time)))
    if senior_interval_value:
        _desc+=",重复:每隔%s%s,持续%s%s "%(senior_interval_value,UNIT_CODE[senior_interval_unit],duration_value
                                     ,UNIT_CODE[duration_unit])
    if backup_type==1:
        _desc+="\t定时备份:完全备份"
    else:
        _desc+="\t定时备份:增量备份"
    return _desc

if __name__ == '__main__':
    print get_plan_desc(2, 3, 4, 0,1468252800000000/1000000,2,4,1,5,1)
    print get_plan_desc(2, 1, 31, 27,1469376000,1,5,2,5,3)
    print get_plan_desc(3, 2, 2, 15,1472054400000000/1000000,2,5,1,5,14)
    print get_plan_desc(2, 3, 2, 0,1469376000000000/1000000,1,5,2,5,5)
    print get_plan_desc(1, 0, 0, 0,1469419024000000/1000000,1,5,0,5,0)
    
    for _item in MONTH_CODE:
        print _item