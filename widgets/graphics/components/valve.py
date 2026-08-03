from PySide6.QtCore import QRectF, Qt, QPoint
from PySide6.QtGui import QPen, QColor, QPainter, QBrush, QLinearGradient
from PySide6.QtWidgets import QGraphicsItem

from widgets.graphics.constants import SCENE_SCALE, ELEMENT_GRADIENT_LIGHT, ELEMENT_GRADIENT_DARK, VALVE_HALF_WIDTH, \
    VALVE_HALF_HEIGHT, VALVE_LINE_WIDTH, BORDER_COLOR


class Valve(QGraphicsItem):

    def __init__(
            self,
            x: int,
            y: int,
            rotation_angle: int = 0,
            text: str | None = None
    ):

        super().__init__()

        self.x = x
        self.y = y
        self.rotation_angle = rotation_angle
        self.text = text
        self.points = [QPoint(tup[0], tup[1]) for tup in self.__points()]
        self.setPos(self.x * SCENE_SCALE, self.y * SCENE_SCALE)

    def __points(self):
        return [
            (int(-VALVE_HALF_WIDTH), int(-VALVE_HALF_HEIGHT)),
            (int(VALVE_HALF_WIDTH), int(-VALVE_HALF_HEIGHT)),
            (int(-VALVE_HALF_WIDTH), int(VALVE_HALF_HEIGHT)),
            (int(VALVE_HALF_WIDTH), int(VALVE_HALF_HEIGHT)),
            (int(-VALVE_HALF_WIDTH), int(-VALVE_HALF_HEIGHT))
        ]

    def boundingRect(self):
        coords = [
            int(coord) for coord in
            [
                - VALVE_HALF_WIDTH,
                - VALVE_HALF_HEIGHT,
                VALVE_HALF_WIDTH * 2,
                VALVE_HALF_HEIGHT * 2
            ]
        ]

        return QRectF(*coords)

    def paint(self, painter, option, widget=None):

        painter.setRenderHint(QPainter.Antialiasing, True)

        rect = self.boundingRect()
        bg_brush = painter.background()
        painter.fillRect(rect, bg_brush)

        pen = QPen()
        pen.setColor(QColor(BORDER_COLOR))
        pen.setWidth(VALVE_LINE_WIDTH)
        pen.setCapStyle(Qt.RoundCap)

        painter.setPen(pen)

        gradient = QLinearGradient(0, 0, 0, 1)
        gradient.setCoordinateMode(QLinearGradient.ObjectBoundingMode)

        gradient.setColorAt(0.0, QColor(ELEMENT_GRADIENT_LIGHT))
        gradient.setColorAt(1.0, QColor(ELEMENT_GRADIENT_DARK))

        painter.setBrush(QBrush(gradient))

        painter.drawPolygon(self.points)

        self.setRotation(self.rotation_angle)

        if self.text:
            font = painter.font()
            font.setItalic(True)

            pen = QPen(QColor('black'))
            painter.setPen(pen)
            painter.setFont(font)

            painter.drawText(
                QRectF(
                    - 40 * SCENE_SCALE,
                    VALVE_HALF_HEIGHT * 0.75,
                    80 * SCENE_SCALE,
                    VALVE_HALF_HEIGHT * 1.5
                ),
                Qt.AlignCenter,
                self.text
            )
