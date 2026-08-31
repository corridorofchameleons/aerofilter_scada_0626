from PySide6.QtCore import QRectF, Qt, QPoint, Slot, Signal, QPropertyAnimation, QTimer, Property, QEasingCurve, \
    QObject, QPointF
from PySide6.QtGui import QPen, QColor, QPainter, QBrush, QLinearGradient
from PySide6.QtWidgets import QGraphicsItem, QGraphicsColorizeEffect

from models.tag import BinaryTag
from mqtt.topics import COMMAND_TOPIC
from signals.signal_bus import bus
from widgets.settings import Settings


class Valve(QGraphicsItem, QObject):
    handle_contour_change = Signal(int, int, bool)

    def __init__(
            self,
            position: tuple,
            x: int,
            y: int,
            contour: tuple,
            rotation_angle: int = 0,
            small: bool = False,
            width: int = Settings.VALVE_WIDTH,
            height: int = Settings.VALVE_HEIGHT,
            tag: BinaryTag=None,
            signal=None
    ):

        super().__init__()

        self.setAcceptHoverEvents(True)

        self.tag = tag
        self.tag.set_new_status.connect(self.update_status)

        self.signal = signal

        self.position = position
        self.x = x
        self.y = y
        self.small = small
        self.width = width
        self.height = height
        if self.small:
            self.width = self.width * 0.7
            self.height = self.height * 0.7
        self.rotation_angle = rotation_angle

        self.contour = set(contour)
        self._is_selected: bool = False
        self._is_active: bool = True
        self.setCursor(Qt.PointingHandCursor)

        self.points = [QPoint(tup[0], tup[1]) for tup in self.__points()]

        self.setPos(self.x, self.y)

        self.start_pt = QPointF(0, 0)
        self.end_pt = QPointF(1, 0)
        self.grad_off = QLinearGradient(self.start_pt, self.end_pt)
        self.grad_on = QLinearGradient(self.start_pt, self.end_pt)

        self.grad_off.setCoordinateMode(QLinearGradient.ObjectBoundingMode)
        self.grad_on.setCoordinateMode(QLinearGradient.ObjectBoundingMode)

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

        painter.setRenderHint(QPainter.Antialiasing, True)
        self.setRotation(self.rotation_angle)

        rect = self.boundingRect()
        bg_brush = painter.background()
        painter.fillRect(rect, bg_brush)

        pen = QPen()
        pen.setColor(QColor(Settings.BORDER_COLOR))
        pen.setWidth(Settings.LINE_WIDTH * 0.5)
        pen.setCapStyle(Qt.RoundCap)

        painter.setPen(pen)

        gradient = QLinearGradient(1, 0, 0, 1)
        gradient.setCoordinateMode(QLinearGradient.ObjectBoundingMode)

        if self._is_selected:
            painter.setBrush(QBrush(self.grad_on))
        else:
            painter.setBrush(QBrush(self.grad_off))

        if not self._is_active:
            overlay_color_background = QColor(0, 0, 0, 10)
            overlay_color_pen = QColor(0, 0, 0, 100)
            brush = QBrush(overlay_color_background)
            painter.setBrush(brush)
            painter.setPen(QPen(overlay_color_pen, 2))

        painter.drawPolygon(self.points)

    @Slot(bool)
    def update_status(self, status: bool):
        if self.signal:
            for pos in self.position:
                for con in self.contour:
                    self.signal.emit(pos, con, status)

    def set_new_status(self):
        if self.tag:
            self.unsetCursor()
            self._is_active = False
            for _ in self.position:
                for _ in self.contour:
                    bus.mqtt_publish_signal.emit(
                        COMMAND_TOPIC,
                        {
                            'name': self.tag.name,
                            'value': not self._is_selected
                        }
                    )

    def mousePressEvent(self, event):
        if self._is_active:
            self.set_new_status()
        pass

    def set_selected(self, val: bool):
        self._is_selected = val

    @Slot(set)
    def handle_contour_change(self, active_contours: set):
        if self.contour.intersection(active_contours):
            self.set_selected(True)
        else:
            self.set_selected(False)
        self._is_active = True
        self.setCursor(Qt.PointingHandCursor)
