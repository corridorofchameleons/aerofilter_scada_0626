from PySide6.QtCore import QRectF, Qt, QPoint
from PySide6.QtGui import QPen, QColor, QPainter
from PySide6.QtWidgets import QGraphicsItem

HALF_WIDTH = 12
HALF_HEIGHT = 17
LINE_WIDTH = 3

class Valve(QGraphicsItem):

    def __init__(
            self,
            ratio: float,
            x: int,
            y: int,
            rotation_angle: int = 0
    ):

        super().__init__()
        self.x = x
        self.y = y
        self.ratio = ratio
        self.rotation_angle = rotation_angle
        self.points = [QPoint(tup[0], tup[1]) for tup in self.__points()]
        self.setPos(self.x, self.y)

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
                (self.x - HALF_WIDTH) * self.ratio,
                (self.y - HALF_HEIGHT) * self.ratio,
                HALF_WIDTH * 2 * self.ratio,
                HALF_HEIGHT * 2 * self.ratio
            ]
        ]

        return QRectF(*coords)

    def paint(self, painter, option, widget=None):

        painter.save()
        painter.translate(int(self.x * self.ratio), int(self.y * self.ratio))
        painter.setRenderHint(QPainter.Antialiasing, True)
        # painter.setCompositionMode(QPainter.CompositionMode_SourceOver)

        pen = QPen()
        pen.setColor(QColor(100,100,100))
        pen.setWidth(LINE_WIDTH)

        pen.setCapStyle(Qt.RoundCap)

        painter.setPen(pen)

        painter.drawPolyline(self.points)

        self.setRotation(self.rotation_angle)

        painter.restore()