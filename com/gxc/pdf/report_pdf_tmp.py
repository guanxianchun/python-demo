# !/usr/bin/python
# coding:utf-8
from esdefine.types import ReportTypeCode
from reportlab.lib.styles import getSampleStyleSheet

ReportTitleTemplet = '<para autoLeading="off" fontSize=15 align=center><b><font face="msyh">%s</font></b><br/></para>'
NormalParaGraphStype = getSampleStyleSheet()['Normal']
TaskReportInfoTemplet = '''<para autoLeading="off" fontSize=10>
        <font face="msyh" fontsize=10>{0}: %s        {1}: %s--%s</font><br/>
        <font face="msyh" fontsize=10>{2}: %s</font><br/>
        </para>'''
TableTitleTemplet = """<para autoLeading="off" fontSize=9><br/><br/><b><font face="msyh">%s</font></b><br/></para>"""

class ReportCode2Tmplet:
    code_2_templet={
        ReportTypeCode.TaskStatReports: TaskStatReportsTemplet,

    }
class TaskStatReportsTemplet:
    title_str_cn = ReportTitleTemplet %('任务统计报告')
    title_str_us = ReportTitleTemplet %('任务统计报告')

    title_style_cn = NormalParaGraphStype
    title_style_us = NormalParaGraphStype
    # 报表基础信息
    info_cn = TaskReportInfoTemplet.format('报告生成于', '报告时间段', '报告对象')
    info_us = TaskReportInfoTemplet.format('报告生成于', '报告时间段', '报告对象')
    para_style = NormalParaGraphStype
    table_task_cn ={
        1:{"title":'按类型统计任务',"first_line":, "col_width_list":[2,3,4,5,6]},
    }
    table_task_us ={
        1: {"title":'按类型统计任务',"first_line": ['', '', '', ''], "col_width_list": [2, 3, 4, 5, 6]},
    }
    table_bar_chart_cn = {"title":'任务摘要' ,"first_line":['','',''], "col_width_list":[2,3,4,5,6]}
    table_bar_chart_us = {"title":'任务摘要' ,"first_line":['','',''], "col_width_list":[2,3,4,5,6]}

    table_pie_chart_cn = {"title":'任务摘要' ,"first_line":['','',''], "col_width_list":[2,3,4,5,6]}
    table_bar_chart_us = {"title":'任务摘要' ,"first_line":['','',''], "col_width_list":[2,3,4,5,6]}
