from PySide6.QtCore import QRectF, QPointF
from PySide6.QtGui import QBrush, Qt, QPainter, QPen, QColor, QPainterPath, QPolygonF, QLinearGradient
from PySide6.QtWidgets import QGraphicsItem, QGraphicsItemGroup

from widgets.graphics.constants import SCENE_SCALE, TANK_HALF_WIDTH, TANK_HALF_HEIGHT, TANK_LINE_WIDTH, \
    TANK_BORDER_COLOR, TANK_BACKGROUND_COLOR, TANK_CORNER_HEIGHT, ELEMENT_GRADIENT_LIGHT, ELEMENT_GRADIENT_DARK, \
    ELEMENT_GRADIENT_DARKER


class TankBody(QGraphicsItem):
    def __init__(self):
        super().__init__()

    def boundingRect(self):
        coords = [
            int(coord * SCENE_SCALE) for coord in
            [
                - TANK_HALF_WIDTH,
                - TANK_HALF_HEIGHT,
                TANK_HALF_WIDTH * 2,
                TANK_HALF_HEIGHT * 2
            ]
        ]
        return QRectF(*coords)

    def paint(self, painter, option, widget=None):
        painter.setRenderHint(QPainter.Antialiasing, True)

        path = QPainterPath()

        rect = self.boundingRect()

        pen = QPen(QColor(TANK_BORDER_COLOR), TANK_LINE_WIDTH)
        painter.setPen(pen)

        body_gradient = QLinearGradient(rect.topLeft(), rect.topRight())

        body_gradient.setColorAt(0.0, ELEMENT_GRADIENT_DARKER)
        body_gradient.setColorAt(0.2, ELEMENT_GRADIENT_DARK)
        body_gradient.setColorAt(0.4, ELEMENT_GRADIENT_LIGHT)
        body_gradient.setColorAt(0.6, ELEMENT_GRADIENT_LIGHT)
        body_gradient.setColorAt(0.8, ELEMENT_GRADIENT_DARK)
        body_gradient.setColorAt(1.0, ELEMENT_GRADIENT_DARKER)

        painter.setBrush(body_gradient)

        path.addRect(rect)

        ch = int(TANK_CORNER_HEIGHT)

        cutter1 = QPolygonF([
            QPointF(rect.left(), rect.top()),
            QPointF(rect.left() + ch, rect.top()),
            QPointF(rect.left(), rect.top() + ch)
        ])

        cutter2 = QPolygonF([
            QPointF(rect.right(), rect.top()),
            QPointF(rect.right() - ch, rect.top()),
            QPointF(rect.right(), top_y := rect.top() + ch)
        ])

        cutter3 = QPolygonF([
            QPointF(rect.left(), rect.bottom()),
            QPointF(rect.left() + ch, rect.bottom()),
            QPointF(rect.left(), rect.bottom() - ch)
        ])

        cutter4 = QPolygonF([
            QPointF(rect.right(), rect.bottom()),
            QPointF(rect.right() - ch, rect.bottom()),
            QPointF(rect.right(), rect.bottom() - ch)
        ])

        tri_1 = QPainterPath()
        tri_2 = QPainterPath()
        tri_3 = QPainterPath()
        tri_4 = QPainterPath()

        tri_1.addPolygon(cutter1)
        tri_2.addPolygon(cutter2)
        tri_3.addPolygon(cutter3)
        tri_4.addPolygon(cutter4)

        path = path.subtracted(tri_1)
        path = path.subtracted(tri_2)
        path = path.subtracted(tri_3)
        path = path.subtracted(tri_4)

        painter.drawPath(path)

        painter.drawLine(
            int(rect.left() * 0.98), int(rect.top() + ch),
            int(rect.right() * 0.98), int(rect.top() + ch)
        )

        painter.drawLine(
            int(rect.left() * 0.98), int(rect.bottom() - ch),
            int(rect.right() * 0.98), int(rect.bottom() - ch)
        )


class Tank(QGraphicsItemGroup):
    def __init__(
            self,
            x: int,
            y: int
    ):
        super().__init__()

        self.x = x
        self.y = y

        self.body = TankBody()

        self.addToGroup(self.body)


        self.setPos(self.x * SCENE_SCALE, self.y * SCENE_SCALE)