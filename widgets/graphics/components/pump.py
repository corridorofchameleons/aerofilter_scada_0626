from PySide6.QtCore import QRectF, Qt, QPoint, QPropertyAnimation, Slot
from PySide6.QtGui import QPen, QColor, QPainter, QBrush, QPainterPath, QLinearGradient
from PySide6.QtWidgets import QGraphicsItem, QGraphicsItemGroup, \
    QGraphicsObject

from widgets.graphics.constants import SCENE_SCALE, IMPELLER_RADIUS, PUMP_HALF_HEIGHT, PUMP_HALF_WIDTH, \
    PUMP_LINE_WIDTH, ELEMENT_GRADIENT_LIGHT, ELEMENT_GRADIENT_DARK, PUMP_THIN_LINE_WIDTH


class Impeller(QGraphicsObject):
    def __init__(
            self,
            rotation_angle: int = 0
    ):

        super().__init__()

        self.rotation_angle = rotation_angle
        self.setZValue(2)

    def boundingRect(self):
        coords = [
            int(coord) for coord in
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
        thin_pen.setWidth(PUMP_THIN_LINE_WIDTH)

        thin_pen.setCapStyle(Qt.RoundCap)

        # рисуем крыльчатку
        painter.setPen(thin_pen)

        radius = int((PUMP_HALF_HEIGHT / 10))
        size = int(radius * 2)
        length = int(IMPELLER_RADIUS - radius)
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
            rotation_angle: int = 0
    ):

        super().__init__()

        self.rotation_angle = rotation_angle
        self.setZValue(2)


    def boundingRect(self):
        coords = [
            int(coord) for coord in
            [
                (-PUMP_HALF_WIDTH),
                (-PUMP_HALF_HEIGHT),
                PUMP_HALF_WIDTH * 2,
                PUMP_HALF_HEIGHT * 2
            ]
        ]

        return QRectF(*coords)


    def paint(self, painter, option, widget=None):
        painter.setRenderHint(QPainter.Antialiasing, True)

        thick_pen = QPen()
        thick_pen.setColor(QColor(100, 100, 100))
        thick_pen.setWidth(PUMP_LINE_WIDTH)

        thick_pen.setCapStyle(Qt.RoundCap)

        painter.setPen(thick_pen)

        gradient = QLinearGradient(0, -PUMP_HALF_HEIGHT, 0, PUMP_HALF_HEIGHT)

        gradient.setColorAt(0.0, QColor(ELEMENT_GRADIENT_LIGHT))
        gradient.setColorAt(1.0, QColor(ELEMENT_GRADIENT_DARK))

        painter.setBrush(QBrush(gradient))

        rect1_path = QPainterPath()

        rect1_path.addRect(
            -int(PUMP_HALF_WIDTH),
            -int((PUMP_HALF_HEIGHT / 2)),
            int(PUMP_HALF_HEIGHT),
            int(PUMP_HALF_HEIGHT)
        )

        rect2_path = QPainterPath()
        rect2_path.addRect(
            0,
            -int(PUMP_HALF_HEIGHT),
            int(PUMP_HALF_WIDTH),
            int(PUMP_HALF_HEIGHT)
        )

        ellipse_path = QPainterPath()
        ellipse_path.addEllipse(
            -int(PUMP_HALF_HEIGHT),
            -int(PUMP_HALF_HEIGHT),
            int(PUMP_HALF_HEIGHT * 2),
            int(PUMP_HALF_HEIGHT * 2)
        )

        combined_path = rect1_path.united(ellipse_path).united(rect2_path)
        painter.drawPath(combined_path)

        painter.setBrush(QBrush(QColor("lightgray")))

        painter.drawEllipse(
            -int(IMPELLER_RADIUS),
            -int(IMPELLER_RADIUS ),
            int(IMPELLER_RADIUS * 2),
            int(IMPELLER_RADIUS * 2)
        )


class Pump(QGraphicsItemGroup):
    def __init__(
            self,
            signal_fn,
    ):
        super().__init__()

        self.body = PumpBody()
        self.impeller = Impeller()

        signal_fn.connect(self.switch_rotation_active)

        self.addToGroup(self.body)
        self.addToGroup(self.impeller)

        self.anim = QPropertyAnimation(self.impeller, b"rotation")

    @Slot()
    def switch_rotation_active(self, start: bool):
        if start:
            self.start_rotation()
        else:
            self.stop_rotation()

    def start_rotation(self, speed=0):
        self.anim.setDuration(600)
        self.anim.setStartValue(0.0)
        self.anim.setEndValue(360.0)
        self.anim.setLoopCount(-1)
        self.anim.start()

    def stop_rotation(self):
        self.anim.stop()
