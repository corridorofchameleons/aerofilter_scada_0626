from PySide6.QtCore import QRectF, Qt, QPoint
from PySide6.QtGui import QPen, QColor
from PySide6.QtWidgets import QGraphicsItem

HALF_WIDTH = 6
HALF_HEIGHT = 16
LINE_WIDTH = 1

class Valve(QGraphicsItem):

    def __init__(self, ratio, x, y):

        super().__init__()
        self.x = x
        self.y = y
        self.ratio = ratio
        self.points = [QPoint(tup[0], tup[1]) for tup in self.__points()]

    def __points(self):
        return [
            (int(-HALF_WIDTH * self.ratio), int(-HALF_HEIGHT * self.ratio)),
            (int(HALF_WIDTH * self.ratio), int(-HALF_HEIGHT * self.ratio)),
            (int(-HALF_WIDTH * self.ratio), int(HALF_HEIGHT * self.ratio)),
            (int(HALF_WIDTH * self.ratio), int(HALF_HEIGHT * self.ratio)),
            (int(-HALF_WIDTH * self.ratio), int(-HALF_HEIGHT * self.ratio))
        ]

    def boundingRect(self):
        coords = [
            int(coord * self.ratio) for coord in
            [
                self.x - HALF_WIDTH,
                self.y - HALF_HEIGHT,
                self.x + HALF_WIDTH,
                self.y + HALF_HEIGHT
            ]
        ]

        return QRectF(*coords)

    def paint(self, painter, option, widget=None):

        pen = QPen()
        pen.setColor(QColor(79, 195, 247))
        pen.setWidth(LINE_WIDTH)
        pen.setJoinStyle(Qt.MiterJoin)
        painter.setPen(pen)

        painter.drawPolyline(self.points)