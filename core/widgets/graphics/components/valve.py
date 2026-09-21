from PySide6.QtCore import QRectF, Qt, QPoint, Slot, QObject, QPointF
from PySide6.QtGui import QPen, QColor, QPainter, QBrush, QLinearGradient
from PySide6.QtWidgets import QGraphicsItem

from core.models.tag import Tag
from core.settings import Settings
from core.widgets.ui_widgets.error_widget import ErrorWidget


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
        self.tag.update_ui.connect(self.update_ui)
        self.tag.disable_ui.connect(self.set_force_disabled)
        self.tag.timeout_error_signal.connect(self.handle_error)

        self.error_widget = ErrorWidget()
        self.error_widget.close_error.connect(self.close_error)

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

        if self.tag.disabled:
            overlay_color_background = QColor(0, 0, 0, 10)
            overlay_color_pen = QColor(0, 0, 0, 100)
            brush = QBrush(overlay_color_background)
            painter.setBrush(brush)
            painter.setPen(QPen(overlay_color_pen, 2))

        painter.drawPolygon(self.points)

    def set_new_status(self):
        self.tag.set_disabled_value(True)
        self.unsetCursor()
        for _ in self.contour:
            self.tag.set_value(not self.tag.value)

    @Slot()
    def update_ui(self):
        self.tag.set_disabled_value(False)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        for con in self.contour:
            self.signal.emit(con, self.tag.value)

    @Slot()
    def set_force_disabled(self):
        if self.tag.disabled:
            self.unsetCursor()
        else:
            self.setCursor(Qt.CursorShape.PointingHandCursor)

    @Slot(str)
    def handle_error(self, text: str):
        self.error_widget.label.setText(text)
        self.error_widget.show()

    @Slot()
    def close_error(self):
        self.error_widget.label.setText('')
        self.error_widget.hide()
        self.tag.set_disabled_value(False)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def mousePressEvent(self, event):
        if not self.tag.disabled:
            self.set_new_status()
