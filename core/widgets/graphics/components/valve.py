from PySide6.QtCore import QRectF, Qt, QPoint, Slot, QObject, QPointF
from PySide6.QtGui import QPen, QColor, QPainter, QBrush, QLinearGradient
from PySide6.QtWidgets import QGraphicsItem

from core.models.tag import Tag
from core.settings import Settings


class Valve(QGraphicsItem, QObject):
    def __init__(
            self,
            contour: tuple,
            rotation_angle: int = 0,
            small: bool = False,
            width: int = Settings.VALVE_WIDTH,
            height: int = Settings.VALVE_HEIGHT,
            tag: Tag=None,
            signal=None
    ):

        super().__init__()
        self.signal = signal

        self.tag = tag
        self.tag.set_bool_value.connect(self.update_status)

        if not self.tag.disabled:
            self.setCursor(Qt.CursorShape.PointingHandCursor)
        else:
            self.unsetCursor()

        self.small = small
        self.width = width
        self.height = height
        if self.small:
            self.width = self.width * 0.7
            self.height = self.height * 0.7
        self.rotation_angle = rotation_angle

        self.contour = set(contour)

        self.points = [QPoint(tup[0], tup[1]) for tup in self.__points()]

        self.start_pt = QPointF(0, 0)
        self.end_pt = QPointF(1, 0)
        self.grad_off = QLinearGradient(self.start_pt, self.end_pt)
        self.grad_on = QLinearGradient(self.start_pt, self.end_pt)

        self.grad_off.setCoordinateMode(QLinearGradient.CoordinateMode.ObjectBoundingMode)
        self.grad_on.setCoordinateMode(QLinearGradient.CoordinateMode.ObjectBoundingMode)

        self.grad_off.setColorAt(0.3, QColor(Settings.ELEMENT_GRADIENT_DARK))
        self.grad_off.setColorAt(0.5, QColor(Settings.ELEMENT_GRADIENT_LIGHT))
        self.grad_off.setColorAt(0.7, QColor(Settings.ELEMENT_GRADIENT_DARK))

        self.grad_on.setColorAt(0.3, QColor(Settings.ELEMENT_GRADIENT_ACTIVE_DARK))
        self.grad_on.setColorAt(0.5, QColor(Settings.ELEMENT_GRADIENT_ACTIVE_LIGHT))
        self.grad_on.setColorAt(0.7, QColor(Settings.ELEMENT_GRADIENT_ACTIVE_DARK))

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

        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        self.setRotation(self.rotation_angle)

        rect = self.boundingRect()
        bg_brush = painter.background()
        painter.fillRect(rect, bg_brush)

        pen = QPen()
        pen.setColor(QColor(Settings.BORDER_COLOR))
        pen.setWidth(Settings.LINE_WIDTH * 0.5)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)

        painter.setPen(pen)

        gradient = QLinearGradient(1, 0, 0, 1)
        gradient.setCoordinateMode(QLinearGradient.CoordinateMode.ObjectBoundingMode)

        if self.tag.value:
            painter.setBrush(QBrush(self.grad_on))
        else:
            painter.setBrush(QBrush(self.grad_off))

        if self.tag.disabled:
            overlay_color_background = QColor(0, 0, 0, 10)
            overlay_color_pen = QColor(0, 0, 0, 100)
            brush = QBrush(overlay_color_background)
            painter.setBrush(brush)
            painter.setPen(QPen(overlay_color_pen, 2))

        painter.drawPolygon(self.points)

    def set_new_status(self):
        self.tag.set_disabled_value(True)
        if self.tag:
            self.unsetCursor()
            for _ in self.contour:
                self.tag.set_value()

    @Slot(bool)
    def update_status(self, status: bool):
        self.tag.value = status
        self.tag.set_disabled_value(False)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        if self.signal:
            for con in self.contour:
                self.signal.emit(con, status)

    def mousePressEvent(self, event):
        if not self.tag.disabled:
            self.set_new_status()
