from PySide6.QtCore import QRectF, Qt, QPoint, QPropertyAnimation, Slot
from PySide6.QtGui import QPen, QColor, QPainter, QBrush, QPainterPath, QLinearGradient
from PySide6.QtWidgets import QGraphicsItem, QGraphicsItemGroup, \
    QGraphicsObject

from core.models.tag import Tag, BoolTag
from core.settings import Settings


class _Impeller(QGraphicsObject):
    def __init__(
            self,
            pump_height: int,
            radius: int,
            rotation_angle: int = 0,
    ):

        super().__init__()
        self.radius = radius
        self.pump_height = pump_height
        self.rotation_angle = rotation_angle
        self.setZValue(2)

    def boundingRect(self):
        return QRectF(
            -self.radius,
            -self.radius,
            self.radius * 2,
            self.radius * 2
        )

    def paint(self, painter, option, widget=None):
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)

        thin_pen = QPen()
        thin_pen.setColor(QColor(Settings.BORDER_COLOR))
        thin_pen.setWidth(Settings.PUMP_THIN_LINE_WIDTH)

        thin_pen.setCapStyle(Qt.PenCapStyle.RoundCap)

        # рисуем крыльчатку
        painter.setPen(thin_pen)

        radius = int(self.pump_height * 0.125)
        size = int(radius * 2)
        length = int(self.radius - radius)
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

        body_brush = QBrush(QColor(Settings.BACKGROUND_COLOR))
        painter.setBrush(body_brush)

        painter.drawEllipse(-radius, -radius, size, size)


class _PumpBody(QGraphicsItem):
    def __init__(
            self,
            height: int,
            width: int,
            impeller_radius: int,
            is_active,
            rotation_angle: int = 0
    ):

        super().__init__()
        self.height = height
        self.width = width

        self.impeller_radius = impeller_radius
        self.rotation_angle = rotation_angle
        self.setZValue(2)

        self.is_active = is_active

    def boundingRect(self):
        return QRectF(
            -self.width / 2,
            -self.height / 2,
            self.width,
            self.height
        )

    def paint(self, painter, option, widget=None):
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)

        thick_pen = QPen()
        thick_pen.setColor(QColor(Settings.BORDER_COLOR))
        thick_pen.setWidth(Settings.LINE_WIDTH)

        thick_pen.setCapStyle(Qt.PenCapStyle.RoundCap)

        painter.setPen(thick_pen)

        gradient = QLinearGradient(0, -self.height, 0, self.height)

        gradient.setColorAt(0.0, QColor(Settings.ELEMENT_GRADIENT_LIGHT))
        gradient.setColorAt(1.0, QColor(Settings.ELEMENT_GRADIENT_DARK))

        painter.setBrush(QBrush(gradient))

        rect1_path = QPainterPath()

        rect1_path.addRect(
            int(self.width),
            -int((self.height / 2)),
            -int(self.height),
            int(self.height)
        )

        rect2_path = QPainterPath()
        rect2_path.addRect(
            0,
            -int(self.height),
            -int(self.width),
            int(self.height)
        )

        ellipse_path = QPainterPath()
        ellipse_path.addEllipse(
            -int(self.height),
            -int(self.height),
            int(self.height * 2),
            int(self.height * 2)
        )

        combined_path = rect1_path.united(ellipse_path).united(rect2_path)
        painter.drawPath(combined_path)

        painter.setBrush(QBrush(QColor(Settings.IMPELLER_BACKGROUND_COLOR)))

        painter.drawEllipse(
            -int(self.impeller_radius),
            -int(self.impeller_radius),
            int(self.impeller_radius * 2),
            int(self.impeller_radius * 2)
        )


class Pump(QGraphicsItemGroup):
    def __init__(
            self,
            contour: tuple,
            tag: BoolTag,
            switch_flow,
            height: int = Settings.PUMP_HEIGHT,
            width: int = Settings.PUMP_WIDTH,
            impeller_radius: int = Settings.IMPELLER_RADIUS,
            small: bool = False
    ):
        super().__init__()
        self.contour = set(contour)
        self.tag = tag
        self.tag.update_ui.connect(self.update_ui)

        self.switch_flow = switch_flow

        self.height = height
        self.width = width
        self.impeller_radius = impeller_radius

        if small:
            self.height = self.height * Settings.SMALL_PUMP_QUOTIENT
            self.width = self.width * Settings.SMALL_PUMP_QUOTIENT
            self.impeller_radius = self.impeller_radius * Settings.SMALL_PUMP_QUOTIENT

        self.setAcceptHoverEvents(True)

        if not self.tag.disabled:
            self.setCursor(Qt.CursorShape.PointingHandCursor)

        self.body = _PumpBody(self.height, self.width, self.impeller_radius, self.tag.value)
        self.impeller = _Impeller(self.height, self.impeller_radius)

        self.addToGroup(self.body)
        self.addToGroup(self.impeller)

        self.anim = QPropertyAnimation(self.impeller, b"rotation")

    def boundingRect(self):
        return self.body.boundingRect()

    def set_new_status(self):
        self.tag.set_disabled_value(True)
        self.unsetCursor()
        self.tag.set_value(not self.tag.value)

    @Slot()
    def update_ui(self):
        self.tag.set_disabled_value(False)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        if self.tag.value:
            self.start_rotation()
        else:
            self.stop_rotation()
        self.switch_flow.emit(self.contour, self.tag.value)

    def mousePressEvent(self, event):
        if not self.tag.disabled:
            self.set_new_status()

    def start_rotation(self, speed=0):
        self.anim.setDuration(Settings.STREAM_DURATION)
        self.anim.setStartValue(360.0)
        self.anim.setEndValue(0.0)
        self.anim.setLoopCount(-1)
        self.anim.start()

    def stop_rotation(self):
        self.anim.stop()
