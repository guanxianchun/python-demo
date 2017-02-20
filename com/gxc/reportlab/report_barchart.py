#!/usr/bin/env pythonget_host_gather_categories
#-*- coding:utf-8 -*-
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.colors import purple, PCMYKColor, red, Color, CMYKColor, yellow
from reportlab.graphics.charts.legends import Legend
from reportlab.graphics.shapes import Drawing, _DrawingEditorMixin, String
from reportlab.lib.validators import Auto
from reportlab.pdfbase.pdfmetrics import stringWidth, EmbeddedType1Face, registerTypeFace, Font, registerFont
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.textlabels import Label
from esreports.report_pdf_define import task_type_color
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
from reportlab.pdfbase.ttfonts import TTFont
from esutils.convert_utils import convert_unicode
pdfmetrics.registerFont(TTFont('msyh', 'msyh.ttf'))

class ReportBarChart(_DrawingEditorMixin,Drawing):
   
    def __init__(self,width,height,x,y,categoryXlables,datas,categoryYlables,*args,**kw):
        Drawing.__init__(self,width,height,*args,**kw)
        # font
        fontName = 'msyh'
        # chart
#         self._add(self,VerticalBarChart(),name='chart',validate=None,desc=None)
#         self.chart.width = width-x
#         self.chart.height = height-15
#         # chart bars
#         self.chart.bars.strokeColor = None
#         self.chart.bars.strokeWidth = 0
#         self.chart.barSpacing = 4
#         self.chart.barLabels.fontName        = fontName
#         self.chart.barLabels.fontSize        = 5
#         self.chart.data = datas
#         self.chart.categoryAxis.categoryNames=categoryXlables
#         # categoy axis
# #         self.chart.categoryAxis.labelAxisMode='low'
#         self.chart.categoryAxis.labels.boxAnchor = 'ne'
#         self.chart.categoryAxis.labels.dy = 5
#         self.chart.categoryAxis.labels.fillColor = PCMYKColor(0,0,0,100)
#         self.chart.categoryAxis.labels.fontName = fontName
#         self.chart.categoryAxis.labels.fontSize = 5
# 
#         self.chart.categoryAxis.labels.angle=25
#         self.chart.categoryAxis.labels.textAnchor='start'
#         self.chart.categoryAxis.strokeWidth     = 0
#         self.chart.categoryAxis.style = 'stacked'
#         # value axis
#         self.chart.valueAxis.labels.fontName    = fontName
#         self.chart.valueAxis.labels.fontSize    = 8
#         self.chart.valueAxis.strokeWidth        = 0
#         self.chart.valueAxis.visibleGrid        = True
#         self.chart.valueAxis.visibleTicks       = True
#         self.chart.valueAxis.visibleAxis        = True
        # legend
        self._add(self,Legend(),name='legend',validate=None,desc=None)
        self.legend.alignment = 'right'
        self.legend.boxAnchor = 'sw'
        self.legend.fontSize = 5
        self.legend.fontName = fontName
        self.legend.strokeColor = None
        self.legend.strokeWidth = 0
        self.legend.subCols.minWidth = 55
        self.legend.columnMaximum =1
        self.legend.deltay = 1
        self.legend.colorNamePairs = zip(task_type_color[0:len(categoryYlables)],categoryYlables)
#         self.legend.colorNamePairs   =  Auto(obj=self.chart)
        
#         for i in range(len(categoryYlables)): 
#             self.chart.bars[i].name = categoryYlables[i]
#             self.chart.bars[i].fillColor = task_type_color[i]
#         self.chart.x = x
#         self.chart.y = y
        self.legend.x = x
#         self.legend.y = 0
    
if __name__=="__main__":
    x_category_lables=[u'2016-08-30', u'2016-08-31', u'2016-09-01', u'2016-09-02', u'2016-09-03', u'2016-09-04', u'2016-09-05']
    barchart_datas=[[1, 20, 1, 1, 1, 1, 2], [0, 20, 0, 30, 0, 10, 10], [0, 0, 31, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]
    barLabels = ['定时备份','实时备份','远程复制','存储快照','数据归档','云备份']
    ReportBarChart(495, 150, 40, 40, x_category_lables, barchart_datas, barLabels).save(formats=['pdf'],outDir='.',fnRoot=None)