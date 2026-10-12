from PySide6.QtCore import QRectF, Qt, QPoint, Slot, QObject, QPointF
from PySide6.QtGui import QPen, QColor, QPainter, QBrush, QLinearGradient
from PySide6.QtWidgets import QGraphicsItem

from core.models.items import Stateful
from core.models.tag import Tag
from core.settings import Settings


class Valve(QGraphicsItem, Stateful):
    def __init__(
            self,
            contour: tuple,
            rotation_angle: int = 0,
            small: bool = False,
            width: int = Settings.VALVE_WIDTH,
            height: int = Settings.VALVE_HEIGHT,
            tag: Tag=None,
            signal=None,
            error_widget: bool = False
    ):

        super().__init__()
        Stateful.__init__(self, tag, error_widget=error_widget)
        self.signal = signal

        self.small = small
        self.width = width
        self.height = height
        if self.small:
            self.width = self.width * 0.7
            self.height = self.height * 0.7
        self.rotation_angle = rotation_angle

        self.contour = set(contour)

        self.points = [QPoint(tup[0], tup[1]) for tup in self.__points()]

        self.setRotation(self.rotation_angle)

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
        rect = self.boundingRect()
        bg_brush = painter.background()
        painter.fillRect(rect, bg_brush)

        pen = QPen()
        pen.setColor(QColor(Settings.BORDER_COLOR))
        pen.setWidth(Settings.PUMP_THIN_LINE_WIDTH)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)

        painter.setPen(pen)

        gradient = QLinearGradient(0, 0, 1, 0)
        gradient.setCoordinateMode(QLinearGradient.CoordinateMode.ObjectBoundingMode)

        if self.tag.value:
            gradient.setColorAt(0.3, QColor(Settings.ELEMENT_GRADIENT_ACTIVE_DARK))
            gradient.setColorAt(0.5, QColor(Settings.ELEMENT_GRADIENT_ACTIVE_LIGHT))
            gradient.setColorAt(0.7, QColor(Settings.ELEMENT_GRADIENT_ACTIVE_DARK))
        else:
            gradient.setColorAt(0.3, QColor(Settings.ELEMENT_GRADIENT_DARK))
            gradient.setColorAt(0.5, QColor(Settings.ELEMENT_GRADIENT_LIGHT))
            gradient.setColorAt(0.7, QColor(Settings.ELEMENT_GRADIENT_DARK))

        painter.setBrush(gradient)

        if self.tag.disabled or self.tag.pending:
            overlay_color_background = QColor(0, 0, 0, 10)
            overlay_color_pen = QColor(0, 0, 0, 100)
            brush = QBrush(overlay_color_background)
            painter.setBrush(brush)
            painter.setPen(QPen(overlay_color_pen, 2))

        painter.drawPolygon(self.points)

    def set_new_status(self, val=None):
        self.tag.pending = True
        self.update()
        for _ in self.contour:
            self.tag.set_value(not self.tag.value)

    @Slot()
    def update_ui(self):
        super().update_ui()
        for con in self.contour:
            pass
            self.signal.emit(con, self.tag.value)

    def mousePressEvent(self, event):
        if not self.tag.pending and not self.tag.disabled:
            self.set_new_status()
