from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import QPolygonF, QTransform, QPainter, QPen, QColor, QBrush
from PySide6.QtWidgets import QGraphicsItem

from widgets.settings import Settings


class Arrow(QGraphicsItem):
    def __init__(
            self,
            small: bool = False,
            rotation_angle: int = 0,
            x: int = 0,
            y: int = 0
    ):
        super().__init__()
        self.small = small
        self.rotation_angle = rotation_angle
        self.x = x
        self.y = y
        self.width = Settings.ARROW_WIDTH
        self.length = Settings.ARROW_LENGTH
        if self.small:
            self.width = self.width / 2
            self.length = self.length / 2


    def boundingRect(self):
        return QRectF(
            -self.width / 2,
            -self.length / 2,
            self.width,
            self.length
        )

    def paint(self, painter, option, widget=None):
        painter.setRenderHint(QPainter.Antialiasing, True)

        red_pen = QPen(QColor(Settings.ARROW_COLOR), 1)
        red_pen.setJoinStyle(Qt.PenJoinStyle.MiterJoin)
        red_brush = QBrush(QColor(Settings.ARROW_COLOR))
        painter.setPen(red_pen)
        painter.setBrush(red_brush)

        points = [
            QPointF(self.x, self.y - self.width / 2),
            QPointF(self.x + self.length * 0.8, self.y),
            QPointF(self.x, self.y + self.width * 0.5),
            QPointF(self.x, self.y + self.width * 0.2),
            QPointF(self.x - self.length, self.y + self.width * 0.2),
            QPointF(self.x - self.length, self.y - self.width * 0.2),
            QPointF(self.x, self.y - self.width * 0.2),
        ]

        polygon = QPolygonF(points)
        transform = QTransform()
        transform.rotate(self.rotation_angle)

        painter.drawPolygon(transform.map(polygon))