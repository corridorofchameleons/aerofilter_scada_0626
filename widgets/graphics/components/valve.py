from PySide6.QtCore import QRectF, Qt, QPoint
from PySide6.QtGui import QPen, QColor, QPainter, QBrush, QLinearGradient
from PySide6.QtWidgets import QGraphicsItem

from widgets.settings import Settings


class Valve(QGraphicsItem):

    def __init__(
            self,
            contour: int,
            rotation_angle: int = 0,
            text: str | None = None,
            width: int = Settings.VALVE_WIDTH,
            height: int = Settings.VALVE_HEIGHT
    ):

        super().__init__()
        self.width = width
        self.height = height
        self.rotation_angle = rotation_angle
        self.text = text
        self.contour = contour
        self.points = [QPoint(tup[0], tup[1]) for tup in self.__points()]

    def __points(self):
        return [
            (int(-self.width * 0.5), int(-self.height * 0.5)),
            (int(self.width * 0.5), int(-self.height * 0.5)),
            (int(-self.width * 0.5), int(self.height * 0.5)),
            (int(self.width * 0.5), int(self.height * 0.5)),
            (int(-self.width * 0.5), int(-self.height * 0.5))
        ]

    def boundingRect(self):
        return QRectF(
            -self.width * 0.5,
            -self.height * 0.5,
            self.width,
            self.height
        )

    def paint(self, painter, option, widget=None):

        painter.setRenderHint(QPainter.Antialiasing, True)

        rect = self.boundingRect()
        bg_brush = painter.background()
        painter.fillRect(rect, bg_brush)

        pen = QPen()
        pen.setColor(QColor(Settings.BORDER_COLOR))
        pen.setWidth(Settings.LINE_WIDTH)
        pen.setCapStyle(Qt.RoundCap)

        painter.setPen(pen)

        gradient = QLinearGradient(0, 0, 0, 1)
        gradient.setCoordinateMode(QLinearGradient.ObjectBoundingMode)

        gradient.setColorAt(0.0, QColor(Settings.ELEMENT_GRADIENT_LIGHT))
        gradient.setColorAt(1.0, QColor(Settings.ELEMENT_GRADIENT_DARK))

        painter.setBrush(QBrush(gradient))

        painter.drawPolygon(self.points)

        self.setRotation(self.rotation_angle)

        if self.text:
            font = painter.font()
            font.setItalic(True)

            pen = QPen(QColor(Settings.TEXT_COLOR))
            painter.setPen(pen)
            painter.setFont(font)

            painter.drawText(
                QRectF(
                    -self.width * 2,
                    self.height * 0.2,
                    self.width * 4,
                    self.height * 1.5
                ),
                Qt.AlignCenter,
                self.text
            )
