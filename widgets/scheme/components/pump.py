from PySide6.QtCore import QRectF, Qt, QPoint, QPropertyAnimation
from PySide6.QtGui import QPen, QColor, QPainter, QBrush, QPainterPath, QLinearGradient
from PySide6.QtWidgets import QGraphicsItem, QGraphicsItemGroup, \
    QGraphicsObject

HALF_WIDTH = 40
HALF_HEIGHT = 25
LINE_WIDTH = 4
THIN_WIDTH = 2
IMPELLER_RADIUS = HALF_HEIGHT / 1.6

class Impeller(QGraphicsObject):
    def __init__(
            self,
            ratio: float,
            rotation_angle: int = 0
    ):

        super().__init__()
        self.ratio = ratio

        self.rotation_angle = rotation_angle
        self.setZValue(3)

    def boundingRect(self):
        coords = [
            int(coord * self.ratio) for coord in
            [
                (-IMPELLER_RADIUS),
                (-IMPELLER_RADIUS),
                IMPELLER_RADIUS * 2,
                IMPELLER_RADIUS * 2
            ]
        ]

        return QRectF(*coords)

    def paint(self, painter, option, widget=None):
        painter.setRenderHint(QPainter.Antialiasing, True)

        thin_pen = QPen()
        thin_pen.setColor(QColor(100,100,100))
        thin_pen.setWidth(THIN_WIDTH)

        thin_pen.setCapStyle(Qt.RoundCap)

        # рисуем крыльчатку
        painter.setPen(thin_pen)

        radius = int((HALF_HEIGHT / 10) * self.ratio)
        size = int(radius * 2)
        length = int(IMPELLER_RADIUS * self.ratio - radius)
        width = int(radius * 0.75)

        painter.drawPolyline([
            QPoint(0, 0),
            QPoint(-width, int(-length / 2)),
            QPoint(0, -length),
            QPoint(width, int(-length / 2)),
            QPoint(0, 0)
        ])

        painter.drawPolyline([
            QPoint(0, 0),
            QPoint(int(length / 2), -width),
            QPoint(length, 0),
            QPoint(int(length / 2), width),
            QPoint(0, 0)
        ])

        painter.drawPolyline([
            QPoint(0, 0),
            QPoint(-width, int(length / 2)),
            QPoint(0, length),
            QPoint(width, int(length / 2)),
            QPoint(0, 0)
        ])

        painter.drawPolyline([
            QPoint(0, 0),
            QPoint(int(-length / 2), -width),
            QPoint(-length, 0),
            QPoint(int(-length / 2), width),
            QPoint(0, 0)
        ])

        body_brush = QBrush(QColor("gray"))
        painter.setBrush(body_brush)

        painter.drawEllipse(-radius, -radius, size, size)


class PumpBody(QGraphicsItem):

    def __init__(
            self,
            ratio: float,
            rotation_angle: int = 0
    ):

        super().__init__()
        self.ratio = ratio

        self.rotation_angle = rotation_angle
        self.setZValue(2)


    def boundingRect(self):
        coords = [
            int(coord * self.ratio) for coord in
            [
                (-HALF_WIDTH),
                (-HALF_HEIGHT),
                HALF_WIDTH * 2,
                HALF_HEIGHT * 2
            ]
        ]

        return QRectF(*coords)


    def paint(self, painter, option, widget=None):
        painter.setRenderHint(QPainter.Antialiasing, True)

        thick_pen = QPen()
        thick_pen.setColor(QColor(100, 100, 100))
        thick_pen.setWidth(LINE_WIDTH)

        thick_pen.setCapStyle(Qt.RoundCap)

        painter.setPen(thick_pen)

        gradient = QLinearGradient(0, -HALF_HEIGHT * self.ratio, 0, HALF_HEIGHT * self.ratio)

        gradient.setColorAt(0.0, QColor("#ECEFF1"))
        gradient.setColorAt(1.0, QColor("#B0BEC5"))

        painter.setBrush(QBrush(gradient))

        rect1_path = QPainterPath()

        rect1_path.addRect(
            -int(HALF_WIDTH * self.ratio),
            -int((HALF_HEIGHT / 2) * self.ratio),
            int(HALF_HEIGHT * self.ratio),
            int(HALF_HEIGHT * self.ratio)
        )

        rect2_path = QPainterPath()
        rect2_path.addRect(
            0,
            -int(HALF_HEIGHT * self.ratio),
            int(HALF_WIDTH * self.ratio),
            int(HALF_HEIGHT * self.ratio)
        )

        ellipse_path = QPainterPath()
        ellipse_path.addEllipse(
            -int(HALF_HEIGHT * self.ratio),
            -int(HALF_HEIGHT * self.ratio),
            int(HALF_HEIGHT * 2 * self.ratio),
            int(HALF_HEIGHT * 2 * self.ratio)
        )

        combined_path = rect1_path.united(ellipse_path).united(rect2_path)
        painter.drawPath(combined_path)

        painter.setBrush(QBrush(QColor("lightgray")))

        painter.drawEllipse(
            -int(IMPELLER_RADIUS * self.ratio),
            -int(IMPELLER_RADIUS * self.ratio),
            int(IMPELLER_RADIUS * 2 * self.ratio),
            int(IMPELLER_RADIUS * 2 * self.ratio)
        )


class Pump(QGraphicsItemGroup):
    def __init__(
            self,
            ratio: float,
            x: int,
            y: int
    ):
        super().__init__()

        self.x = x
        self.y = y
        self.ratio = ratio

        self.body = PumpBody(self.ratio)
        self.impeller = Impeller(self.ratio)

        self.addToGroup(self.body)
        self.addToGroup(self.impeller)

        self.anim = QPropertyAnimation(self.impeller, b"rotation")

        # Настройки цикла
        self.setPos(x, y)


    def rotate(self, speed=0):
        self.anim.setDuration(600)
        self.anim.setStartValue(360.0)
        self.anim.setEndValue(0.0)
        self.anim.setLoopCount(-1)
        self.anim.start()
