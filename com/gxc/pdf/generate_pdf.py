# -*- coding: utf-8 -*-
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont

pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
from reportlab.pdfbase.ttfonts import TTFont

# pdfmetrics.registerFont(TTFont('msyh', 'msyh.ttf'))
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.platypus import BaseDocTemplate, SimpleDocTemplate, Paragraph, Spacer, Image, Table, LongTable, \
    TableStyle
from reportlab.lib.pagesizes import A4, landscape, inch
from reportlab.lib import pdfencrypt
import time
import os
import base64
import StringIO

class PdfGenerater(object):
    def __init__(self, name, path, need_draw_frame, title, passwd=None):
        self.data_list = []
        self.name = name
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

    def generate_table(self, data_list, style,colWidths=None):
        tab = Table(data_list,colWidths=colWidths)
        # 另外需考虑表格整体大小。
        # 单元格定长 Table(data_list, colWidths=[20,50,50, 150, 90, 90])
        tab.setStyle(style)
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
        doc = SimpleDocTemplate(self.path + self.name, author='eisoo.com', title=self.title, encrypt=enc)
        if self.need_draw_frame:
            doc.build(self.data_list, onFirstPage=self.drawPageFrame, onLaterPages=self.drawPageFrame)
        else:
            doc.build(self.data_list)

# 过长字段切割。（备注：中文编码问题）
# def split_str(long_str,split_num = 10):
#     long_str=long_str.decode('utf-8')
#     length=len(long_str)
#     if split_num <= 0:
#         split_num=10
#     if length <= split_num:
#         return long_str.encode('utf-8')
#     import textwrap
#     ret = textwrap.wrap(long_str, split_num)
#     ret_str = ''
#     for i in range(len(ret)):
#         ret_str += ret[i]
#         if i <len(ret)-1:
#             ret_str += '\n'
#     return ret_str.encode('utf-8')

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
    <font face="msyh" color=black>报表时间范围:  %s--%s</font><br/>
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
    table_style = TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'msyh'),  # 字体
        ('FONTSIZE', (0, 0), (-1, -1), 5),  # 字体大小
        # ('SPAN',(0,0),(3,0)),#合并第一行前三列
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightskyblue),  # 设置第一行背景颜色
        # ('SPAN',(-1,0),(-2,0)), #合并第一行后两列
        ('ALIGN', (-1, 0), (-2, 0), 'RIGHT'),  # 对齐
        ('VALIGN', (-1, 0), (-2, 0), 'MIDDLE'),  # 对齐
        ('LINEBEFORE', (0, 0), (0, -1), 0.1, colors.grey),  # 设置表格左边线颜色为灰色，线宽为0.1
        ('TEXTCOLOR', (0, 1), (-2, -1), colors.black),  # 设置表格内文字颜色
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),  # 设置表格框线为灰色，线宽为0.5
    ])

    table1_data = [
        ['任务名称', '应用类型', '备份节点', '客户端', '执行次数', '成功次数', '成功率'],
        ['a', 'MYSQL数据库', '备份节点01', '客户端A', 10, '3', '33.33%'],
        ['定时备份02', '文件系统', '备份节点02', '客户端B', '5', '2', '25.00%'],
        ['实时备份01', 'MySQL数据库', '备份节点03', '客户端C', '1000', '800', '80.00%'],
        ['实时备份01', '文件系统', '备份节点03', '客户端D', '800', '400', '50.00%'],
    ]
    my_pdf.generate_table(table1_data, table_style,[80,60,60,60,40,40,40])
    # 空行
    my_pdf.generate_spacer(20)
    # 图片
#     my_pdf.generate_image('C:/Users/admin/Desktop/a.jpg')
    my_pdf.build()
