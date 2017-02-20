#-*- encoding:utf-8 -*-
from reportlab.lib.colors import Color, blue, red
from reportlab.graphics.charts.legends import Legend, TotalAnnotator
from reportlab.graphics.shapes import Drawing, _DrawingEditorMixin
from reportlab.lib.validators import Auto
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.pdfbase import pdfmetrics
"Comparison chart"
from reportlab.lib.colors import purple, PCMYKColor, red, Color, CMYKColor, yellow
from reportlab.graphics.charts.legends import Legend
from reportlab.graphics.shapes import Drawing, _DrawingEditorMixin, String
from reportlab.lib.validators import Auto
from reportlab.pdfbase.pdfmetrics import stringWidth, EmbeddedType1Face, registerTypeFace, Font, registerFont
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.textlabels import Label

from reportlab.pdfbase.cidfonts import UnicodeCIDFont
pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont('msyh', 'msyh.ttf'))

class BarChart02(_DrawingEditorMixin,Drawing):
    '''
        Chart Features
        --------------

        This is a Bar Chart that contains a Legend Widget to compare several companies performance
        for a period of last 10 years. Features include:

        - A Legend that can wrap: **legend.columnMaximum=3**

        - Labels for the positive bars are above bars, while labels for negative bars are below bars.
        You can control this through the property **chart.barLabels.boxTarget** which can take
        one of ('normal','anti','lo','hi')

        - Simple category axis - dates are not necessary here.

        This chart was built with our [Diagra](http://www.reportlab.com/software/diagra/) solution.

        Not the kind of chart you looking for? Go [up](..) for more charts, or to see different types of charts click on [ReportLab Charts Gallery](/chartsgallery/).
    '''
    def __init__(self,width=298,height=164,*args,**kw):
        Drawing.__init__(self,width,height,*args,**kw)
        # font
        fontName = 'msyh'
        # chart
        self._add(self,VerticalBarChart(),name='chart',validate=None,desc=None)
        self.chart.width = width
        self.chart.height = height
        # chart bars
        self.chart.bars.strokeColor = None
        self.chart.bars.strokeWidth = 0
        self.chart.barSpacing = 4
        self.chart.barWidth = 14
        self.chart.barLabelFormat   = '%s'
        self.chart.barLabels.nudge           = 5
        self.chart.barLabels.fontName        = fontName
        self.chart.barLabels.fontSize        = 5
        # categoy axis
        self.chart.categoryAxis.labelAxisMode='low'
        self.chart.categoryAxis.labels.angle = 0
        self.chart.categoryAxis.labels.boxAnchor = 'n'
        self.chart.categoryAxis.labels.dy = -6
        self.chart.categoryAxis.labels.fillColor = PCMYKColor(0,0,0,100)
        self.chart.categoryAxis.labels.fontName = fontName
        self.chart.categoryAxis.labels.fontSize = 8
        self.chart.categoryAxis.labels.textAnchor='middle'
        self.chart.categoryAxis.tickShift=1
        self.chart.categoryAxis.visibleTicks = 0
        self.chart.categoryAxis.strokeWidth     = 0
        self.chart.categoryAxis.strokeColor         = None
        self.chart.groupSpacing = 15
        # value axis
        self.chart.valueAxis.avoidBoundFrac     = None
        self.chart.valueAxis.labels.fontName    = fontName
        self.chart.valueAxis.labels.fontSize    = 8
        self.chart.valueAxis.rangeRound         = 'both'
        self.chart.valueAxis.strokeWidth        = 0
        self.chart.valueAxis.visibleGrid        = 1
        self.chart.valueAxis.visibleTicks       = 0
        self.chart.valueAxis.visibleAxis        = 0
        self.chart.valueAxis.gridStrokeColor    = PCMYKColor(100,0,46,46)
        self.chart.valueAxis.gridStrokeWidth    = 0.25
        self.chart.valueAxis.valueStep          = None#3
        self.chart.valueAxis.labels.dx          = -3
        # legend
        self._add(self,Legend(),name='legend',validate=None,desc=None)
        self.legend.alignment = 'right'
        self.legend.boxAnchor = 'sw'
        self.legend.columnMaximum = 3
        self.legend.dx = 8
        self.legend.dxTextSpace = 4
        self.legend.dy = 6
        self.legend.fontSize = 8
        self.legend.fontName = fontName
        self.legend.strokeColor = None
        self.legend.strokeWidth = 0
        self.legend.subCols.minWidth = 55
        self.legend.variColumn = 1
        self.legend.y = 1
        self.legend.deltay = 10
        self.legend.colorNamePairs   =  Auto(obj=self.chart)
        self.legend.autoXPadding     = 65
        # x label
        self._add(self,Label(),name ='XLabel',validate=None,desc="The label on the horizontal axis")
        self.XLabel._text = ""
        self.XLabel.fontSize = 6
        self.XLabel.height = 0
        self.XLabel.maxWidth = 100
        self.XLabel.textAnchor ='middle'
        self.XLabel.x = 0
        self.XLabel.y = 10
        # y label
#         self._add(self,Label(),name='YLabel',validate=None,desc="The label on the vertical axis")
#         self.YLabel._text = ""
#         self.YLabel.angle = 90
#         self.YLabel.fontSize = 6
#         self.YLabel.height = 0
#         self.YLabel.maxWidth = 100
#         self.YLabel.textAnchor ='middle'
#         self.YLabel.x = 12
#         self.YLabel.y = 0
        #sample data
        self.chart.data = [[-2.6000000000000001, -0.80000000000000004, 9.8000000000000007, None, None, None, None], [-1.8999999999999999, 1.3999999999999999, 13.1, None, None, None, None], [-1.8999999999999999, 1.3, 12.199999999999999, 4.9000000000000004, 2.2000000000000002, 5.4000000000000004, 10.6], [-1.7, 2.0, 13.300000000000001, 5.9000000000000004, 3.2000000000000002, 6.4000000000000004, 11.6], [-1.8999999999999999, 1.5, 13.9, 4.0999999999999996, -1.3, 3.8999999999999999, 11.1]]
        self.chart.categoryAxis.categoryNames=['Q3', 'YTD', '1 Year', '3 Year', '5 Year', '7 Year', '10 Year']
        for i in range(len(self.chart.data)): self.chart.bars[i].name = ('BP妈', 'Shell Transport & Trading', 'Liberty International', 'Persimmon', 'Royal Bank of Scotland',)[i]
        self.width       = 400
        self.height      = 200
        self.chart.x               = 30
        self.chart.y               = 65
        self.legend.x              = 30
        self.chart.bars[0].fillColor   = PCMYKColor(0,100,100,40,alpha=85)
        self.chart.bars[1].fillColor   = PCMYKColor(23,51,0,4,alpha=85)
        self.chart.bars[2].fillColor   = PCMYKColor(100,60,0,50,alpha=85)
        self.chart.bars[3].fillColor   = PCMYKColor(66,13,0,22,alpha=85)
        self.chart.bars.fillColor       = PCMYKColor(100,0,90,50,alpha=85)

class BarChart06(_DrawingEditorMixin,Drawing):
    '''
        Chart Features
        --------------
        We have added an experimental table legend to our open source library. This table legend
        can align its column values with another widget's columns (or bars, etc ...):

        - The bars are filled with one color and stroked with black color.

        - Bar labels are not displayed, you could achieve that through either setting the
        **barLabels.visible** to False, or not providing a formatting function (or any python callable)
        to the barLabelFormat attribute.

        - Simple category axis - dates are not necessary here.

        This chart was built with our [Diagra](http://www.reportlab.com/software/diagra/) solution.

        Not the kind of chart you looking for? Go [up](..) for more charts, or to see different types of charts click on [ReportLab Charts Gallery](/chartsgallery/).
    '''
    def __init__(self,width=403,height=163,*args,**kw):
        Drawing.__init__(self,width,height,*args,**kw)
        fontName = 'msyh'
        fontSize = 5
        bFontName = 'Times-Bold'
        bFontSize = 7
        colorsList = [PCMYKColor(0, 73, 69, 56), PCMYKColor(0, 3, 7, 6),PCMYKColor(41, 25, 0, 21)]
        self._add(self,VerticalBarChart(),name='chart',validate=None,desc=None)
        self.chart.height                  = 73
        self.chart.fillColor               = None
        self.chart.data                    = [[7.7199999999999998, 7.9400000000000004, 9.1699999999999999, 7.04, 7.7199999999999998, 8.1699999999999999], [4.46, 1.97, 13.220000000000001, 10.49, 8.5800000000000001, 10.74], [5.1399999999999997, 9.5999999999999996, 5.3099999999999996, 4.4699999999999998, 3.5099999999999998, 4.8399999999999999]]
        #self.chart.bars.fillColor         = color
        self.chart.bars.strokeWidth        = 0.5
        self.chart.bars.strokeColor        = PCMYKColor(0,0,0,100)
        #self.chart.barLabels.angle         = 90
        #self.chart.barLabelFormat          = DecimalFormatter(2)
        #self.chart.barLabels.boxAnchor     ='w'
        #self.chart.barLabels.boxFillColor  = None
        #self.chart.barLabels.boxStrokeColor= None
        #self.chart.barLabels.fontName      = fontName
        #self.chart.barLabels.fontSize      = fontSize
        #self.chart.barLabels.dy            = 3
        #self.chart.barLabels.boxTarget     = 'hi'
        #self.chart.annotations=[lambda c,cA,vA: Line(c.x,c.y,c.x+c.width,c.y,strokeColor=black,strokeWidth=0.5)]
        for i, color in enumerate(colorsList): self.chart.bars[i].fillColor = color
        self.chart.valueAxis.labels.fontName       = fontName
        self.chart.valueAxis.labels.fontSize       = fontSize
        self.chart.valueAxis.strokeDashArray       = (5,0)
        self.chart.valueAxis.visibleGrid           = True
        self.chart.valueAxis.visibleTicks          = False
        self.chart.valueAxis.tickLeft              = 0
        self.chart.valueAxis.tickRight             = 11
        #self.chart.valueAxis.gridStrokeDashArray   = (0,1,0)
        #self.chart.valueAxis.valueStep             = 200
        self.chart.valueAxis.strokeWidth           = 0.25
        #self.chart.valueAxis.gridStrokeWidth       = 0.25
        #self.chart.valueAxis.gridStrokeDashArray   = (1,1,1)
        self.chart.valueAxis.avoidBoundFrac        = 0#1#0.5
        self.chart.valueAxis.rangeRound            ='both'
        self.chart.valueAxis.gridStart             = 13
        self.chart.valueAxis.gridEnd               = 342
        self.chart.valueAxis.labelTextFormat        = None #DecimalFormatter(1, suffix=None, prefix=None)
        self.chart.valueAxis.forceZero              = True
        self.chart.valueAxis.labels.boxAnchor       = 'e'
        self.chart.valueAxis.labels.dx              = -1
        self.chart.categoryAxis.strokeDashArray        = (5,0)
        #self.chart.categoryAxis.gridStrokeDashArray = (1,1,1)
        self.chart.categoryAxis.visibleGrid         = False
        self.chart.categoryAxis.visibleTicks        = False
        self.chart.categoryAxis.strokeWidth         = 0.25
        self.chart.categoryAxis.tickUp              = 5
        self.chart.categoryAxis.tickDown            = 0
        self.chart.categoryAxis.labelAxisMode       ='low'
        self.chart.categoryAxis.labels.textAnchor   ='end'
        self.chart.categoryAxis.labels.angle        = 0
        self.chart.categoryAxis.labels.fontName     = bFontName
        self.chart.categoryAxis.labels.fontSize     = bFontSize
        #self.chart.categoryAxis.tickShift          = 1
        #self.chart.categoryAxis.strokeDashArray     = (0,1,0)
        # self.chart.categoryAxis.labels.boxAnchor    = 'autox'
        self.chart.categoryAxis.labels.boxAnchor    = 'e'
        self.chart.categoryAxis.labels.dx           = 7#-10
        self.chart.categoryAxis.labels.dy           = -5
        self._add(self,Legend(),name='legend',validate=None,desc=None)
        self.legend.deltay           = 8
        self.legend.fontName         = fontName
        self.legend.fontSize         = fontSize
        self.legend.strokeWidth      = 0.5
        self.legend.strokeColor      = PCMYKColor(0,0,0,100)
        self.legend.autoXPadding     = 0
        self.legend.dy               = 5
        self.legend.variColumn       = True
        self.legend.subCols.minWidth = self.chart.width/2 # 175
        self.legend.colorNamePairs   = Auto(obj=self.chart)
#         self._add(self,TableWidget(),name='table',validate=None,desc=None)
#         self.table.x = 0
#         self.table.y = 0
#         self.table.height = 45
#         self.table.borderStrokeColor = PCMYKColor(0, 12, 24, 36)
#         self.table.fillColor = PCMYKColor(0, 3, 7, 6)
#         self.table.borderStrokeWidth = 0.5
#         self.table.horizontalDividerStrokeColor = PCMYKColor(0, 12, 24, 36)
#         self.table.verticalDividerStrokeColor = None
#         self.table.horizontalDividerStrokeWidth = 0.5
#         self.table.verticalDividerStrokeWidth = 0
#         self.table.dividerDashArray = None
        table_data = [['BP', None, '7.72', '7.94', '9.17', '7.04', '7.72', '8.17'], ['Shell Transport & Trading', None, '4.46', '1.97', '13.22', '10.49', '8.58', '10.74'], ['Liberty International', None, '5.14', '9.60', '5.31', '4.47', '3.51', '4.84']]
#         self.table.boxAnchor = 'sw'
#         self.table.fontName = bFontName
#         self.table.fontSize = bFontSize
#         self.table.fontColor = colors.black
#         self.table.alignment = 'left'
#         self.table.textAnchor = 'start'
        for i in range(len(self.chart.data)): self.chart.bars[i].name = table_data[i][0]
        self.chart.categoryAxis.categoryNames = ['200%d'%i for i in range(1,7)]
        self.width       = 400
#         self.table.width                        = 400
        self.height      = 200
        self.legend.dx             = 8
        self.legend.dxTextSpace    = 5
        self.legend.deltax         = 0
        self.legend.alignment      = 'right'
        self.legend.columnMaximum  = 3
        self.chart.y               = 75
        self.chart.barWidth        = 2
        self.chart.groupSpacing    = 5
        self.chart.width           = 250
        self.chart.barSpacing      = 0.5
        self.chart.x               = 140
        self.legend.y              = 75
        self.legend.boxAnchor      = 'sw'
        self.legend.x              = 24
        self.chart.bars[0].fillColor   = PCMYKColor(100,60,0,50,alpha=100)
        self.chart.bars[1].fillColor   = PCMYKColor(23,51,0,4,alpha=100)
        self.chart.bars[2].fillColor   = PCMYKColor(100,0,90,50,alpha=100)


class FactSheetHoldingsVBar(_DrawingEditorMixin,Drawing):
    def __init__(self,width=400,height=200,*args,**kw):
        apply(Drawing.__init__,(self,width,height)+args,kw)
        self._add(self,VerticalBarChart(),name='bar',validate=None,desc=None)
        self.bar.data             = [[4.22], [4.12], [3.65], [3.56], [3.49], [3.44], [3.07], [2.84], [2.76], [1.09]]
        self.bar.categoryAxis.categoryNames = ['Financials艰','Energy','Health Care','Telecoms','Consumer','Consumer 2','Industrials','Materials','Other','Liquid Assets']
        self.bar.categoryAxis.labels.fillColor = None
        self.bar.width                      = 200
        self.bar.height                     = 150
        self.bar.x                          = 30
        self.bar.y                          = 15
        self.bar.barSpacing                 = 5
        self.bar.groupSpacing               = 5
        self.bar.valueAxis.labels.fontName  = 'msyh'
        self.bar.valueAxis.labels.fontSize  = 8
        self.bar.valueAxis.forceZero        = 1
        self.bar.valueAxis.rangeRound       = 'both'
        self.bar.valueAxis.valueMax         = None#10#
        self.bar.categoryAxis.visible       = 1
        self.bar.categoryAxis.visibleTicks  = 0
        self.bar.barLabels.fontSize         = 6
        self.bar.valueAxis.labels.fontSize  = 6
        self.bar.strokeWidth                = 0.1
        self.bar.bars.strokeWidth           = 0.5
        n                                   = len(self.bar.data)
        #add and set up legend
        self._add(self,Legend(),name='legend',validate=None,desc=None)
        _ = ['Vodafone Group', 'UBS', 'British Petroleum', 'Royal bk of Scotland', 'HSBC Holdings', 'Total Elf Fina', 'Repsol', 'Novartis', 'BNP Paribas', 'Schneider Electric' ]
        self.legend.colorNamePairs  = [(Auto(chart=self.bar),(t,'%.2f'% d[0])) for t,d in zip(_,self.bar.data)]
        self.legend.columnMaximum   = 10
        self.legend.fontName        = 'msyh'
        self.legend.fontSize        = 5.5
        self.legend.boxAnchor       = 'w'
        self.legend.x               = 260
        self.legend.y               = self.height/2
        self.legend.dx              = 8
        self.legend.dy              = 8
        self.legend.alignment       = 'right'
        self.legend.yGap            = 0
        self.legend.deltay          = 11
        self.legend.dividerLines    = 1|2|4
        self.legend.subCols.rpad    = 10
        self.legend.dxTextSpace     = 5
        self.legend.strokeWidth     = 0
        self.legend.dividerOffsY    = 6
        self.legend.colEndCallout   = TotalAnnotator(rText='%.2f'%sum([x[0] for x in self.bar.data]), fontName='Helvetica-Bold', fontSize=self.legend.fontSize*1.1)
        self.legend.colorNamePairs  = [(self.bar.bars[i].fillColor, (self.bar.categoryAxis.categoryNames[i][0:20], '%0.2f' % self.bar.data[i][0])) for i in range(len(self.bar.data))]
        print self.legend.colorNamePairs
        
def drawing_chinese():
    from reportlab.graphics.charts.lineplots import LinePlot
    from reportlab.graphics.charts.textlabels import Label
    from reportlab.graphics import renderPDF
    from reportlab.graphics.widgets.markers import makeMarker
    data=[((1,100),(2,200),(3,300),(4,400),(5,500)),((1,50),(2,80),(3,400),(4,40),(5,70))]
    drawing = Drawing(500, 300)

    lp = LinePlot()
    lp.x = 50 #������������
    lp.y = 30
    lp.height = 250
    lp.width = 400
    lp.data = data
    lp.joinedLines = 1
    lp.lines.symbol = makeMarker('FilledCircle')
    
    lp.xValueAxis.valueMin = 1
    lp.xValueAxis.valueMax = 5
    lp.xValueAxis.valueStep = 1
    
    lp.yValueAxis.valueMin = 0
    lp.yValueAxis.valueMax = 500
    lp.yValueAxis.valueStep = 100
    drawing.add(lp)
    
    title = Label()
    #����Ҫ��ʾ���ģ���Ҫ��ע��һ����������
    title.fontName   = "msyh"
    title.fontSize   = 12
    title_text = u'你好吗'
    #title_text = "abc"
    title._text = title_text
    title.x          = 250
    title.y          = 280
    title.textAnchor ='middle'
    drawing.add(title)
    
    Xlabel = Label()
    Xlabel._text = 'x'
    Xlabel.fontSize   = 12
    Xlabel.x          = 480
    Xlabel.y          = 30
    Xlabel.textAnchor ='middle'
    drawing.add(Xlabel)
    
    Ylabel = Label()
    Ylabel._text = "y"
    Ylabel.fontSize   = 12
    Ylabel.x          = 40
    Ylabel.y          = 295
    Ylabel.textAnchor ='middle'
    drawing.add(Ylabel)
    
    try:
         drawing.save(formats=['gif'],outDir=".",fnRoot="abc")
    except:
        import traceback
        traceback.print_exc()
if __name__=="__main__": #NORUNTESTS
    drawing = FactSheetHoldingsVBar()
    drawing.save(formats=['pdf'],outDir='.',fnRoot=None)
    drawing.save(formats=['png'],outDir='.',fnRoot=None)
    BarChart02().save(formats=['pdf'],outDir='.',fnRoot=None)
    BarChart06().save(formats=['pdf'],outDir='.',fnRoot=None)
    drawing_chinese()