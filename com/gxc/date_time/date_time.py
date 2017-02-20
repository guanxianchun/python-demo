#-*- encoding:utf-8 -*-
'''
Created on 2016年7月20日

@author: admin
'''
import datetime
month_table_name_data={"t_task_exc_stat_2016":{1:5,2:5,4:5,5:5,7:5,8:5,9:5,10:5,11:5,12:5},
                       "t_task_exc_stat_2015":{1:5,2:5,3:5,4:5,5:5,6:5,7:5,8:5,9:5,10:5,11:5,12:5}}
def get_task_history_count(table_name,task_id,_start_date,_end_date):
    result = {"total":0}
    if table_name in month_table_name_data:
        if _start_date.month in month_table_name_data[table_name]:
            result = {"total":month_table_name_data[table_name][_start_date.month]}
    return result
def  get_tables_datas(task_id,start,count):
    table_start_count={}
    total = 0
    _end_date = datetime.datetime.now()
    _start_date = _end_date.replace(day=1)
    all_table_names = ["t_task_exc_stat_2016","t_task_exc_stat_2015"]
    avail_count=0
    for table_name in all_table_names:
        _year = _start_date.year
        #大于当前年份，取下一个小的年份表
        if int(table_name.split("_")[-1])>_year:
            continue
        #得到相应的查询时间（与表对应的年）
        while True:
            tmp_year = int(table_name.split("_")[-1])
            if tmp_year==_year:
                break
            else:
                _end_date = _start_date-datetime.timedelta(days=1)
                _start_date = _end_date.replace(day=1)
                _year = _start_date.year
        _tmp_year = _year
        month_table_name="t_task_history_%s_%s"
        while _tmp_year==_year:
            result = get_task_history_count(table_name,task_id,_start_date,_end_date)
            _tmp_total = total
            #当前月没有数据，则找下一个月
            if result is None or not result["total"]:
                _end_date = _start_date-datetime.timedelta(days=1)
                _start_date = _end_date.replace(day=1)
                _year = _start_date.year
                continue
            total +=result["total"]
            if total>start:
                    _key=_start_date.strftime("%Y-%m")
                    _name = month_table_name%(_year,_start_date.month)
                    if _tmp_total<=start:
                        table_start_count[_key]={"start":start-_tmp_total, "table_name":_name}
                    else:
                        #前一张表的数据不够的情况
                        table_start_count[_key]={"start":_tmp_total-start-avail_count, "table_name":_name}
                    if total>=start+count:
                        table_start_count[_key]["count"]=count-avail_count
                        #已经取完了，则直接返回
                        return table_start_count
                    else:
                        table_start_count[_key]["count"]=total-_tmp_total-table_start_count[_key]["start"]
                        avail_count +=table_start_count[_key]["count"]
            
            _end_date = _start_date-datetime.timedelta(days=1)
            _start_date = _end_date.replace(day=1)
            _year = _start_date.year
if __name__ == '__main__':
    date_time = datetime.datetime.now()
    date_time = date_time+datetime.timedelta(days=30)
    print date_time.strftime("%Y_%m-%d"),date_time.year,date_time.month
    _new_date = date_time.replace(day=1)
    print _new_date.strftime("%Y_%m-%d")
    print (_new_date-datetime.timedelta(days=1)).strftime("%Y_%m-%d")
    result = get_tables_datas(1, 2, 4)
    sort_table_names = sorted(result,reverse=True)
    for table_name in sort_table_names:
        print table_name,result[table_name]
    data = []
    data.extend([{"id":1,"name":"gxc"},{"id":2,"name":"gxc"},{"id":3,"name":"gxc"}])
    print data
    data.extend([{"id":5,"name":"gxc"},{"id":6,"name":"gxc"},{"id":7,"name":"gxc"}])
    print data
    _result = u"0"
    if int(_result):
        print "*"*78