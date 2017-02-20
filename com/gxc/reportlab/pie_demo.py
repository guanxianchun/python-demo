#-*- encoding:utf-8 -*-
from reportlab.graphics.shapes import Drawing
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import platform
from reportlab.lib import colors
sysstr = platform.system()
if "Windows" == sysstr:
    pdfmetrics.registerFont(TTFont('msyh', 'msyh.ttf'))
else:
    pdfmetrics.registerFont(TTFont('msyh', '/usr/share/fonts/liberation/msyh.ttf'))
def get_pie_image(width,height,x,y,datas,lables,_colors):
    """
        ��ɱ�״ͼ
    @param width: ͼƬ���
    @param height: ͼƬ�Ŀ��
    @param x: ͼƬ��x���
    @param y: ͼƬ��y���
    @param datas: ���ͼƬ�����
    @param lables: ��״ͼ���������
    """
    
    from reportlab.graphics.charts.piecharts import Pie
    drawing = Drawing(width, height)
    pc = Pie()
    pc.width = 80
    pc.height = 80
    pc.x = x
    pc.y = y
    pc.data = datas
    pc.labels = lables
    pc.slices.strokeWidth=0.5
    pc.startAngle = 90
    pc.checkLabelOverlap=True
    pc.sideLabels = True
    pc.sideLabelsOffset =0.1
    pc.direction = 'clockwise'
    for i in range(len(lables)):
        pc.slices[i].fontName = "msyh"
        pc.slices[i].fontSize =3
        pc.slices[i].labelRadius = 3
        pc.slices[i].popout = 5
        pc.slices[i].fillColor = _colors[i]
    drawing.add(pc)
    return drawing

if __name__ == '__main__':
    datas=[1,1000,800,12,12]
    _colors = [colors.red,colors.gold,colors.black,colors.blue,colors.green]
    lables =['成功','失败','成功且有警告','已停止','部分成功']
    d = get_pie_image(400, 200, 60, 60, datas, lables,_colors)
    d.save(formats=['pdf'])