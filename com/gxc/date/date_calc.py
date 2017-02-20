#!/usr/bin/env python
#-*- encoding:utf-8 -*-
'''

时间: 2017年2月6日 下午3:18:13
@author: guan.xianchun
'''

import calendar,datetime,time,re
import decimal
from math import ceil
STR_TIME_FORMAT_ONE = '(^\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2}$)'
STR_TIME_FORMAT_TWO = '(^\d{4}/\d{1,2}/\d{1,2} \d{1,2}:\d{1,2}:\d{1,2}$)'
STR_TIME_FORMAT_THREE = '(^/\d{1,2}/\d{1,2}/\d{4} \d{1,2}:\d{1,2}:\d{1,2}$)'
STR_TIME_FORMAT_FOUR = '(^\d{4}\d{2}\d{2}$)'
STR_TIME_FORMAT_FIVR = '(^\d{4}-\d{1,2}-\d{1,2}$)'
STR_TIME_FORMAT_SIX = '(^\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2}.\d+S$)'
STR_TIME_FORMAT_SEVEN = '(^\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d+Z$)'
STR_TIME_FORMAT_MAP ={STR_TIME_FORMAT_ONE:'%Y-%m-%d %H:%M:%S',
                      STR_TIME_FORMAT_TWO:'%Y/%m/%d %H:%M:%S',
                      STR_TIME_FORMAT_THREE:'%d/%m/%Y %H:%M:%S',
                      STR_TIME_FORMAT_FOUR:'%Y%m%d',
                      STR_TIME_FORMAT_FIVR:'%Y-%m-%d',
                      STR_TIME_FORMAT_SIX:'%Y-%m-%d %H:%M:%S.%fS',
                      STR_TIME_FORMAT_SEVEN:'%Y-%m-%d %H:%M:%SZ',
                      } 

def months_to_days(startDate, months):
    """
    将月数转换成天数
    @:param startDate 开始时间
    @:param months 月数（多少个月）
    """
    month = startDate.month - 1 + months
    year = startDate.year + month / 12
    month = month % 12 + 1
    day = min(startDate.day, calendar.monthrange(year, month)[1])
    days = (datetime.datetime(year, month, day) - startDate).days
    return days + 1

def days_to_date(startDate, days):
    """
    将相差的天数转成时间
    @:param startDate 开始时间
    @:param days 相差的天数
    @:return 返回相差的时间对象
    """
    date_time = startDate + datetime.timedelta(days)
    return date_time

def string_to_datetime(time_str):
    """
    将时间字符串转换成datetime
    @:param time_str 时间字符串 支持的格式如下：
                    '年-月-日 时:分:秒',
                    '年/月/日 时:分:秒',
                    '日/月/年 时:分:秒',
                    '年月日',
                    '年-月-日',
    @:return datetime时间对象 如何是不支持的格式则返回空
    """
    _time = None
    if re.match(STR_TIME_FORMAT_ONE, time_str):
        _time = datetime.datetime.strptime(time_str,STR_TIME_FORMAT_MAP[STR_TIME_FORMAT_ONE])
    elif re.match(STR_TIME_FORMAT_TWO, time_str):
        _time = datetime.datetime.strptime(time_str,STR_TIME_FORMAT_MAP[STR_TIME_FORMAT_TWO])
    elif re.match(STR_TIME_FORMAT_THREE, time_str):
        _time = datetime.datetime.strptime(time_str,STR_TIME_FORMAT_MAP[STR_TIME_FORMAT_THREE])
    elif re.match(STR_TIME_FORMAT_FOUR, time_str):
        _time = datetime.datetime.strptime(time_str,STR_TIME_FORMAT_MAP[STR_TIME_FORMAT_FOUR])
    elif re.match(STR_TIME_FORMAT_FIVR, time_str):
        _time = datetime.datetime.strptime(time_str,STR_TIME_FORMAT_MAP[STR_TIME_FORMAT_FIVR])
    elif re.match(STR_TIME_FORMAT_SIX, time_str):
        _time = datetime.datetime.strptime(time_str,STR_TIME_FORMAT_MAP[STR_TIME_FORMAT_SIX])
    elif re.match(STR_TIME_FORMAT_SEVEN, time_str):
        _time = datetime.datetime.strptime(time_str,STR_TIME_FORMAT_MAP[STR_TIME_FORMAT_SEVEN])
    return _time

def time_to_str(source_time,format=STR_TIME_FORMAT_MAP[STR_TIME_FORMAT_ONE]):
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
    
def timestamp_to_datetime(source_time):
    """
    将时间戳转换成datetime对象
    @:param source_time 
    @:return datetime对象
    """
    return datetime.datetime.fromtimestamp(source_time)

def datetime_to_timestamp(source_time):
    """
    获取datetime的时间戳
    如果不是datetime对象，则返回None
    @:param source_time  datetime对象
    @:return 时间戳
    """
    if isinstance(source_time, (datetime.datetime,datetime.date)):
        return time.mktime(source_time.timetuple())
    return None

def calc_datatime_interval_months(source_data,dest_date):
    def check_leap_year(year):
        if (year%4 == 0 and year%100 != 0) or (year%400 == 0 and year%100 == 0):
            return True
        else:
            return  False
    def get_max_day_in_month(year, month):
        dic_month_max_day = {1: 31, 2: 29 if check_leap_year(year) is True else 28, 3: 31, 4: 30, 5:31, 6: 30,
                             7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
        return dic_month_max_day[month]
    def get_next_month_date(year,month):
        months = month + 1
        if months % 12 != 0:
            return year+months / 12,months % 12
        else:
            return year+months / 12-1,12
        
    year_org = int(source_data.year)
    month_org = int(source_data.month)
    day_org = int(source_data.day)
    hour_org = int(source_data.hour)
    minute_org = int(source_data.minute)
    second_org = int(source_data.second)
    month=1
    while True:
        _year,_month = get_next_month_date(year_org,month_org)
        check_date = datetime.datetime(_year, _month, day_org if get_max_day_in_month(_year, _month) > day_org else get_max_day_in_month(_year, _month),
                            hour_org, minute_org, second_org)
        if check_date>dest_date:
            check_date = datetime.datetime(year_org, month_org, day_org if get_max_day_in_month(year_org, month_org) > day_org else get_max_day_in_month(year_org, month_org),
                            hour_org, minute_org, second_org)
            return month-1,(dest_date-check_date).days,get_max_day_in_month(year_org, month_org)
        if check_date==dest_date:
            return month,0,0
        else:
            year_org,month_org=_year,_month
            month+=1
            
if __name__ == '__main__':
    source_date = "2017-2-1 00:00:00"
    dest_date = "2018-2-28 00:00:00"
    _value = calc_datatime_interval_months(string_to_datetime(source_date),string_to_datetime(dest_date))
    print '%s-%s相差的月份：%s'%(source_date,dest_date,str(_value))
    print 10*_value[0]+ceil(10.0*_value[1]/_value[2])
