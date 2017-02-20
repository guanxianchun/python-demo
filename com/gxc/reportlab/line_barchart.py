#-*- encoding:utf-8 -*-

from reportlab.graphics.charts.linecharts import HorizontalLineChart
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.widgets.markers import makeMarker
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.lib.colors import Color
from reportlab.lib import colors

if __name__=="__main__":
    
    drawing = Drawing(400, 200)
    data = [
    (2, -10, 0, 0, 0, 0, 0, 4)
    ]
    lc = HorizontalLineChart()
    lc.x = 50
    lc.y = 50
    lc.height = 125
    lc.width = 300
    lc.data = data
    lc.joinedLines = 1
    lc.lines.symbol = makeMarker('Circle')
#     lc.valueAxis.visibleAxis =0
#     lc.valueAxis.visibleGrid =0
#     lc.valueAxis.visibleLabels =0
#     lc.valueAxis.visible =0
    lc.categoryAxis.visible =0
#     lc.categoryAxis.visibleLabels =0
#     lc.categoryAxis.labels.boxAnchor = 'n'
#     lc.valueAxis.valueMin = 0
#     lc.valueAxis.valueMax = 60
#     lc.valueAxis.valueStep = 15
    lc.lines[0].strokeWidth = 1
    lc.lines[1].strokeWidth = 1
    lc.lines[0].strokeColor=colors.blue
    lc.lines[1].strokeColor=colors.green
    
    
    data = [
    (13, 5, 20, 22, 37, 45, 19, 4)
    ]
    bc = VerticalBarChart()
    bc.x = 50
    bc.y = 50
    bc.height = 125
    bc.width = 300
    bc.data = data
    bc.valueAxis.valueMin = -10
    bc.valueAxis.valueMax = 50
    bc.valueAxis.valueStep = 10
    bc.categoryAxis.labels.boxAnchor = 'ne'
    bc.categoryAxis.labels.dx = 8
    bc.categoryAxis.labels.dy = -2
    bc.categoryAxis.labels.angle = 30
    bc.strokeWidth= 0.1
    bc.bars.strokeWidth= 0.2
    bc.categoryAxis.categoryNames = ['Jan-99','Feb-99','Mar-99',
    'Apr-99','May-99','Jun-99','Jul-99','Aug-99']
    
    bc.categoryAxis.style = 'stacked'
    bc.strokeWidth= 0.1
    bc.bars.strokeWidth= 0.2
    
    drawing.add(bc)
    drawing.add(lc)
    drawing.save(['pdf'])