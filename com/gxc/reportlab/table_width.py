# -*- coding: utf-8 -*-
from _collections import defaultdict
import time, os, base64, StringIO

from reportlab.lib import colors
from reportlab.lib import pdfencrypt
from reportlab.lib.pagesizes import A4, landscape, inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import BaseDocTemplate, SimpleDocTemplate, Paragraph, Spacer, Image, Table, LongTable, \
    TableStyle


pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
# from esutils.convert_utils import convert_unicode
pdfmetrics.registerFont(TTFont('msyh', 'msyh.ttf'))

class BaseTableStyle:
    @classmethod
    def get_no_title_default_style(cls):
        return TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'msyh'),  # 字体
            ('FONTSIZE', (0, 0), (-1, 0), 6),  # 列表头字体大小
            ('FONTSIZE', (0, 1), (-1, -1), 5),  # 列表内容字体大小
            ('BACKGROUND', (0, 0), (-1, 0),colors.HexColor("#F6F6F6")),  #列表头背景颜色
            ('ALIGN', (0, 0), (-1, 0), 'LEFT'),  # 列表头对齐方式
            ("LEFTPADDING",(0,0),(-1,-1),1),   #表格左边内部边距为1
            ("RIGHTPADDING",(0,0),(-1,-1),1),  #表格右边内部边距为1
            ("BOTTOMPADDING",(0,0),(-1,-1),1),
            ('ALIGN', (0, 1), (-1, -1), 'LEFT'),  # 对齐
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),  # 设置表格内文字颜色
            ('GRID', (0, 0), (-1, -1),0.8, colors.HexColor("#C9C9C9")),  # 设置表格框线为灰色，线宽为0.5
        ])
    @classmethod
    def get_default_style(cls):
        return TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'msyh'),  # 字体
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor("#0449A6")),  #标题文本颜色(报表名称)
            ('FONTSIZE', (0, 0), (-1, 1), 7),  # 标题文本字体大小 (报表名称)
            ('TEXTCOLOR', (0, 1), (-1, 1), colors.black),  #标题文本颜色(报表名称)
            ('SPAN',(0,0),(-1,0)), #合并第一行所有列
            ('BACKGROUND', (0, 0), (-1, 0),colors.HexColor('#E6F3FF')),  #标题背景颜色
            ('FONTSIZE', (0, 1), (-1, -1), 5),  # 列表头字体大小
            ('BACKGROUND', (0, 1), (-1, 1),colors.HexColor("#F6F6F6")),  #列表头背景颜色
            ('ALIGN', (0, 1), (-1, 1), 'LEFT'),  # 列表头对齐方式
            ("LEFTPADDING",(0,0),(-1,-1),1),   #表格左边内部边距为1
            ("RIGHTPADDING",(0,0),(-1,-1),1),  #表格右边内部边距为1
            ("BOTTOMPADDING",(0,0),(-1,-1),1),
            ('ALIGN', (0, 2), (-1, -1), 'LEFT'),  # 对齐
            ('TEXTCOLOR', (0, 2), (-1, -1), colors.black),  # 设置表格内文字颜色
            ('GRID', (0, 0), (-1, -1),0.8, colors.HexColor("#C9C9C9")),  # 设置表格框线为灰色，线宽为0.5
        ])
    @classmethod
    def get_empty_table_style(cls):
        return TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'msyh'),  # 字体
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor("#0449A6")),  #标题文本颜色(报表名称)
            ('FONTSIZE', (0, 0), (-1, 1), 7),  # 标题文本字体大小 (报表名称)
            ('TEXTCOLOR', (0, 1), (-1, 1), colors.black),  #标题文本颜色(报表名称)
            ('SPAN',(0,0),(-1,0)), #合并第一行所有列
            ('FONTSIZE', (0, 1), (-1, -1), 5),  # 列表头字体大小
            ('BACKGROUND', (0, 1), (-1, 1),colors.toColor('rgb(0,131,165)')),  #列表头背景颜色
            ('ALIGN', (0, 1), (-1, 1), 'LEFT'),  # 列表头对齐方式
            ("LEFTPADDING",(0,0),(-1,-1),1),   #表格左边内部边距为1
            ("RIGHTPADDING",(0,0),(-1,-1),1),  #表格右边内部边距为1
            ("BOTTOMPADDING",(0,0),(-1,-1),1),
            ('SPAN',(0,2),(-1,2)), #
            ('ALIGN', (0, 2), (-1, 2), 'LEFT'),  # 对齐
    #         ('LINEBEFORE', (0, 0), (0, -1), 0.1, colors.lightskyblue),  # 设置表格左边线颜色为灰色，线宽为0.1
            ('TEXTCOLOR', (0, 2), (-2, -1), colors.black),  # 设置表格内文字颜色
            ('GRID', (0, 0), (-1, -1),0.8, colors.toColor('rgb(201,201,201)')),  # 设置表格框线为灰色，线宽为0.5
        ])

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

def wrap_str(str_value,split_num):
    """
        按指定的字符数换行 中文算1.5个字符宽度数
    @param str_value: 要wrap的字符串
    @param split_num: 每行的字符数
    @return: 返回处理后的字符串
    """
    if not isinstance(str_value, str):
        str_value = str(str_value)
    long_str=convert_unicode(str_value)
    ret_str = ''
    index =0
    for uchar in long_str:
        if index>=(split_num-2):
            ret_str+="\n"
            index =0
        ret_str+=uchar
        if uchar >= u'\u4e00' and uchar<=u'\u9fa5':
            index+=1.55
        elif uchar.isupper():
            index+=1.1
        elif uchar.islower():
            index+=0.85
        elif uchar.isdigit():
            index+=0.9
        elif uchar in [u'#']:
            index+=1
        elif uchar in [u'@',u'－',u'￥']:
            index+=1.62
        elif uchar in [u'&',u'%']:
            index+=1.4
        else:
            index+=0.9
    return ret_str.encode("utf-8")

if __name__ == '__main__':
    headers =['任务类型','名称']
    table_datas = [['定时任务','奇功村厅大师傅大师傅厅防盗锁无可奈何花落去士大夫大师傅枯地要地厅村傅厅防盗锁无可奈何花落去 士大夫大师傅枯地要地厅村'],
                   ['定时任务','奇FDSFDSFDS功村厅FDSFDS大师－－－－246789FDSFSAF044162.2132.·#￥%4士大夫大FDSFDSFDSF师@#@#傅枯地SAFSDAFDS_要__地厅村DSFSF傅SDF厅DSFDSF防盗锁无DSFDSF可奈何花落去'],
                   ['定时任务','172.172.172.172'],
                   ['定时任务','11111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111']
                   ,['定时任务','ASDADSAFDSGFDHGKJHLJKPEWQREWRIEWIROWEROEWIROWEQIROEWIROEWIROEWORIEWDKFGJLDSKFOEWEWIROEWRIEW']
                   ,['定时任务','@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@']
                   ,['定时任务','##############################################################################']
                   ,['定时任务','&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&']
                   ,['定时任务','246789044444444444447777777777777777777777777777777777777777777777777777777444444444444444444444444444444444444444444444444444444444444444']
                   ,['定时任务','奇功村厅大师－－－－246789044162.2132.·#￥%4士大夫大师傅枯地_要__地厅村傅厅防盗锁无可奈何花落去']
                   ,['定时任务','$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$']
                   ,['定时任务','￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥']
                   ,['定时任务','%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%']
                   ,['定时任务','%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%']
                   ,['定时任务','%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%']
                ]
    colWidths = [40,42]
    split_nums =[12,13]
    data_list = []
    for _item in table_datas:
        for i in range(len(_item)):
            _item[i] = wrap_str(_item[i], split_nums[i])
    table_datas.insert(0,headers)
    tab = Table(table_datas,colWidths)
    tab.setStyle(BaseTableStyle.get_no_title_default_style())
    data_list.append(tab)
    full_file_name = "./test_table.pdf"
    f = open(full_file_name, "wb")
    doc = SimpleDocTemplate(f, title=convert_unicode("dsfds"),leftMargin=30,rightMargin=30)
    doc.build(data_list)
    f.close()