from PySide6.QtCore import QRectF, Qt, QPointF
from PySide6.QtGui import QPainter, QPen, QColor, QLinearGradient, QBrush, QPolygonF
from PySide6.QtWidgets import QGraphicsItem

from widgets.settings import Settings


class Rotameter(QGraphicsItem):
    def __init__(
            self,
            width: int | float = Settings.ROTAMETER_WIDTH,
            height: int | float = Settings.ROTAMETER_HEIGHT
    ):
        super().__init__()
        self.width = width
        self.height = height

    def boundingRect(self):
        return QRectF(
            -self.width * 0.5,
            -self.height * 0.5,
            self.width,
            self.height
        )

    def paint(self, painter, option, /, widget=None):
        painter.setRenderHint(QPainter.Antialiasing, True)

        r = self.boundingRect()

        pen = QPen()
        pen.setColor(QColor(Settings.BORDER_COLOR))
        pen.setWidth(Settings.LINE_WIDTH * 0.5)
        pen.setCapStyle(Qt.RoundCap)

        grad = QLinearGradient(r.topLeft(), r.topRight())
        grad.setColorAt(0.0, QColor(Settings.ELEMENT_GRADIENT_LIGHT))
        grad.setColorAt(1.0, QColor(Settings.ELEMENT_GRADIENT_DARK))

        brush = QBrush(grad)

        painter.setPen(pen)
        painter.setBrush(brush)

        painter.drawRect(r)

        pen.setWidth(2)
        points = [
            QPointF(-self.width * 0.2, -self.width * 0.2),
            QPointF(self.width * 0.2, -self.width * 0.2),
            QPointF(0, self.width * 0.2),
        ]

        polygon = QPolygonF(points)
        painter.drawPolygon(polygon)
