# -*- coding: utf-8 -*-
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from _collections import defaultdict

pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
from reportlab.pdfbase.ttfonts import TTFont
# from esutils.convert_utils import convert_unicode
pdfmetrics.registerFont(TTFont('msyh', '/usr/share/fonts/liberation/msyh.ttf'))
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.platypus import BaseDocTemplate, SimpleDocTemplate, Paragraph, Spacer, Image, Table, LongTable, \
    TableStyle
from reportlab.lib.pagesizes import A4, landscape, inch
from reportlab.lib import pdfencrypt
import time,os,base64,StringIO
# from esreports.report_pdf_define import ReportTaskStatsTable,ReportModuleType,BaseTableStyle
# from esdefine.types import TaskType
# from esutils.utils import wrap_str

# data={TaskType.SCHEDULE:[["2016-08-12","181-文件系统-定时备份-成功 ","文件系统文件系统 文件系统","111.186AB_Softwarefdsafdsaf","PENGXL-244asfdsfdsafds","172.172.112.122","221","1000","123","1222","2220","2220","100.00%"],
#                          ["2016-08-12","181-文件系统-定时 ","2016-08-122016-08-122016-08-12","111.186AB_Software","PENGXL-244","172.17.112.2","221","1000","123","1222","2220","2220","100.00%"],
#                          ["2016-08-12","181-文件系统-定时 ","111.186AB_Software ","111.186AB_Software","PENGXL-244","172.17.112.2","221","1000","123","1222","2220","2220","100.00%"]
#                          ,["2016-08-12","AB_SoftwareAB_SoftwareAB_SoftwareAB_Software ","文件111.186AB_Software系统 ","111.186AB_Software","PENGXL-244","172.17.112.2","221","1000","123","1222","2220","2220","100.00%"]
#                          ,["2016-08-12","181-文件系统-定时 ","文件系统 ","111.186AB_Software","PENGXL-244","172.17.112.2","221","1000","123","1222","2220","2220","100.00%"]
#                          ,["2016-08-12","181-文件系统-定时 ","文件系统 ","111.186AB_Software","PENGXL-244","172.17.112.2","221","1000","123","1222","2220","2220","100.00%"]
#                          ,["2016-08-12","PENGXLPENGXLPENGXLPENGXLPENGXLPENGXLPENGXL ","文件系统 ","111.186AB_Software","PENGXL-244","172.17.112.2","221","1000","123","1222","2220","2220","100.00%"]
#                          ,["2016-08-13","181-文件系统-定时 ","文件系统 ","111.186AB_Software","PENGXL-244","172.17.112.2","221","1000","123","1222","2220","2220","100.00%"]
#                          ,["2016-08-13","181-文件系统-定时 ","文件系统 ","111.186AB_Software","PENGXL-244","172.17.112.2","221","1000","123","1222","2220","2220","100.00%"]
#                          ,["2016-08-13","181-文件系统-定时 ","文件系统 ","111.186AB_Software","PENGXL-244","172.17.112.2","221","1000","123","1222","2220","2220","100.00%"]
#                          ,["2016-08-13","181-文件系统-定时 ","文件系统 ","111.186AB_Software","PENGXL-244","172.17.112.2","221","1000","123","1222","2220","2220","100.00%"]
#                          ,["2016-08-13","181-文件系统-定时 ","文件系统 ","111.186AB_Software","PENGXL-244","172.17.112.2","221","1000","123","1222","2220","2220","100.00%"]
#                          ,["2016-08-13","181-文件系统-定时 ","文件系统 ","111.186AB_Software","PENGXL-244","172.17.112.2","221","1000","123","1222","2220","2220","100.00%"]
#                          ,["2016-08-13","181-文件系统-定时 ","文件系统 ","111.186AB_Software","PENGXL-244","172.17.112.2","221","1000","123","1222","2220","2220","100.00%"]
#                          ,["2016-08-13","181-文件系统-定时 ","文件系统 ","111.186AB_Software","PENGXL-244","172.17.112.2","221","1000","123","1222","2220","2220","100.00%"]
#                          ,["2016-08-13","181-文件系统-定时 ","文件系统 ","111.186AB_Software","PENGXL-244","172.17.112.2","221","1000","123","1222","2220","2220","100.00%"]
#                          ,["2016-08-13","181-文件系统-定时 ","文件系统 ","111.186AB_Software","PENGXL-244","172.17.112.2","221","1000","123","1222","2220","2220","100.00%"]
#                          ,["2016-08-13","181-文件系统-定时 ","文件系统 ","111.186AB_Software","PENGXL-244","172.17.112.2","221","1000","123","1222","2220","2220","100.00%"]
#                          ,["2016-08-13","181-文件系统-定时 ","文件系统 ","111.186AB_Software","PENGXL-244","172.17.112.2","221","1000","123","1222","2220","2220","100.00%"]
#                          ,["2016-08-13","181-文件系统-定时 ","文件系统 ","111.186AB_Software","PENGXL-244","172.17.112.2","221","1000","123","1222","2220","2220","100.00%"]
#                          ,["2016-08-13","181-文件系统-定时 ","文件系统 ","111.186AB_Software","PENGXL-244","172.17.112.2","221","1000","123","1222","2220","2220","100.00%"]
#                          ,["2016-08-13","181-文件系统-定时 ","文件系统 ","111.186AB_Software","PENGXL-244","172.17.112.2","221","1000","123","1222","2220","2220","100.00%"]
#                          ,["2016-08-13","181-文件系统-定时 ","文件系统 ","111.186AB_Software","PENGXL-244","172.17.112.2","221","1000","123","1222","2220","2220","100.00%"]
#                          ,["2016-08-13","181-文件系统-定时 ","文件系统 ","111.186AB_Software","PENGXL-244","172.17.112.2","221","1000","123","1222","2220","2220","100.00%"]
#                          ,["2016-08-14","181-文件系统-定时 ","文件系统 ","111.186AB_Software","PENGXL-244","172.17.112.2","221","1000","123","1222","2220","2220","100.00%"]
#                          ,["2016-08-14","181-文件系统-定时 ","文件系统 ","111.186AB_Software","PENGXL-244","172.17.112.2","221","1000","123","1222","2220","2220","100.00%"]
#                          ,["2016-08-14","181-文件系统-定时 ","文件系统 ","111.186AB_Software","PENGXL-244","172.17.112.2","221","1000","123","1222","2220","2220","100.00%"]
#                          ,["2016-08-15","181-文件系统-定时 ","文件系统 ","111.186AB_Software","PENGXL-244","172.17.112.2","221","1000","123","1222","2220","2220","100.00%"]
#                          ,["2016-08-15","181-文件系统-定时 ","文件系统 ","111.186AB_Software","PENGXL-244","172.17.112.2","221","1000","123","1222","2220","2220","100.00%"]]}

class PdfGenerater(object):
    def __init__(self, name, path, need_draw_frame, title, passwd=None):
        self.data_list = []
        self.name = "管贤春.pdf"
        self.path = path
        self.need_draw_frame = need_draw_frame
        self.passwd = passwd
        self.title = title

    # 画背景图片
    @staticmethod
    def drawPageFrame(canvas, doc):
        h, w = landscape(A4)
        canvas.saveState()
        canvas.drawImage("eisoo.jpg", 400, 810, 200, 30)
        canvas.restoreState()

    def generate_table(self, data_list, style=None,colWidths=None):
        tab = Table(data_list,colWidths=colWidths)
        # 另外需考虑表格整体大小。
        # 单元格定长 Table(data_list, colWidths=[20,50,50, 150, 90, 90])
#         tab.setStyle(style)
        self.data_list.append(tab)

    def generate_paragraph(self, text, style):
        par = Paragraph(text, style)
        self.data_list.append(par)

    def generate_image(self, image, w=500, h=150):
        ima = Image(image, w, h)
        self.data_list.append(ima)

    def generate_spacer(self, num):
        spacer = Spacer(0, num)
        self.data_list.append(spacer)

    def build(self):
        if self.passwd:
            enc = pdfencrypt.StandardEncryption(self.passwd, canPrint=1)
        else:
            enc = None
        doc = SimpleDocTemplate(self.path + self.name, author='eisoo.com', title=self.title, encrypt=enc,leftMargin=40,rightMargin=40)
        if self.need_draw_frame:
            doc.build(self.data_list, onFirstPage=self.drawPageFrame, onLaterPages=self.drawPageFrame)
        else:
            doc.build(self.data_list)

if __name__ == '__main__':
    my_pdf = PdfGenerater('我的报表.pdf', './', 0, '我的报表标题')
    report_creator = '系统管理员'
    report_start_time = '2016-01-01'
    report_end_time = '2016-0-07'
    report_obj = '全部站点'
    report_type = '任务统计报告'
    text = '''<para autoLeading="off" fontSize=10>
    <br/><br/>
    <font face="msyh" >创建者：%s</font><br/>
    <font face="msyh" color=black>报表时间范围: dsafsdsaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaasfdsafffffffffffffffffffffffffffffffffffffffffffffff %s--%s</font><br/>
    <font face="msyh" fontsize=10>报表对象：  %s</font><br/>
    <font face="msyh" fontsize=10>报表类型：  %s</font><br/>
    </para>''' % (report_creator, report_start_time, report_end_time, report_obj, report_type)

    stylesheet = getSampleStyleSheet()
    normalStyle = stylesheet['Normal']
    # 标题
    rpt_title = '<para autoLeading="off" fontSize=15 align=center><b><font face="msyh">%s</font></b><br/></para>' % (
    '资源报告')
    my_pdf.generate_paragraph(rpt_title, normalStyle)
    # 段落
    my_pdf.generate_paragraph(text, normalStyle)
    # 表格
#     table_style = BaseTableStyle.get_default_style()

    table1_data = [
        ['任务名称', '应用类型', '备份节点', '客户端', '执行次数', '成功次数', '成功率'],
        ['a', 'MYSQL数据库', '备份节点01', '客户端A', 10, '3', '33.33%'],
        ['定时备份02', '文件系统', '备份节点02', '客户端B', '5', '2', '25.00%'],
        ['实时备份01', 'MySQL数据库', '备份节点03', '客户端C', '1000', '800', '80.00%'],
        ['实时备份01', '文件系统', '备份节点03', '客户端D', '800', '400', '50.00%'],
    ]
#     table1_data.insert(0, ['任务统计报表', '', '', '', '', '', ''])
#     for item in data[TaskType.SCHEDULE]:
#         table1_data.append(item)
#     colwdiths = ReportTaskStatsTable.get_colum_widths(ReportModuleType.TASK_STATS, TaskType.SCHEDULE)
#     splitNums = ReportTaskStatsTable.get_colum_width_split_nums(ReportModuleType.TASK_STATS, TaskType.SCHEDULE)
#     span_row_info = {}
#     index = 0
#     count = 0
#     for datas in table1_data:
#         if count==0:
#             count +=1
#             continue
#         if index not in span_row_info:
#                 span_row_info[index]={"date":datas[0],"count":1,"start":count}
#         else:
#             if span_row_info[index]["date"]==datas[0]:
#                 span_row_info[index]["count"]+=1
#             else:
#                 index+=1
#                 span_row_info[index]={"date":datas[0],"count":1,"start":count}
#         count +=1
#         for i in range(len(datas)):
#             datas[i]=wrap_str(datas[i],splitNums[i])
#             
#     print span_row_info
#     for _index in span_row_info:
#         start_row = span_row_info[_index]["start"]
#         end_row = span_row_info[_index]["start"]+span_row_info[_index]["count"]-1
#         table_style.add('SPAN',(0,start_row),(0,end_row))
#     print table_style
#     table_style.add('SPAN',(0,0),(-1,0))
    my_pdf.generate_table(table1_data)
    # 空行
    my_pdf.generate_spacer(20)
    # 图片
#     my_pdf.generate_image('C:/Users/admin/Desktop/a.jpg')
    my_pdf.build()
