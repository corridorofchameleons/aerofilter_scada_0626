from PySide6.QtCore import QRectF, Qt, QPoint, Slot, Signal
from PySide6.QtGui import QPen, QColor, QPainter, QBrush, QLinearGradient
from PySide6.QtWidgets import QGraphicsItem

from widgets.settings import Settings


class Valve(QGraphicsItem):
    def __init__(
            self,
            position: tuple,
            x: int,
            y: int,
            contour: tuple,
            rotation_angle: int = 0,
            # text: str | None = None,
            small: bool = False,
            width: int = Settings.VALVE_WIDTH,
            height: int = Settings.VALVE_HEIGHT,
            signal_fn=None,
            fn=None
    ):

        super().__init__()

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
        # self.text = text
        self.contour = set(contour)

        # self.setAcceptHoverEvents(True)
        self.signal_fn = signal_fn
        self.fn = fn
        if self.signal_fn and self.fn:
            self.signal_fn.connect(self.fn)

        self._is_selected: bool = False

        self.points = [QPoint(tup[0], tup[1]) for tup in self.__points()]

        self.setPos(self.x, self.y)


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

        if self._is_selected:
            painter.setBrush(QColor(Settings.PIPE_INNER_COLOR_ACTIVE))
        else:
            painter.setBrush(QBrush(gradient))

        painter.drawPolygon(self.points)

        self.setRotation(self.rotation_angle)

        # if self.text:
        #     font = painter.font()
        #     font.setItalic(True)
        #
        #     pen = QPen(QColor(Settings.TEXT_COLOR))
        #     painter.setPen(pen)
        #     painter.setFont(font)
        #
        #     painter.drawText(
        #         QRectF(
        #             -self.width * 2,
        #             self.height * 0.2,
        #             self.width * 4,
        #             self.height * 1.5
        #         ),
        #         Qt.AlignCenter,
        #         self.text
        #     )

    def mousePressEvent(self, event):
        if self.signal_fn:
            for contour in self.contour:
                for position in self.position:
                    self.signal_fn.emit(position, contour, not self._is_selected)

    def set_selected(self, val: bool):
        self._is_selected = val

    @Slot(set)
    def handle_contour_change(self, active_contours: set):
        if self.contour.intersection(active_contours):
            self.set_selected(True)
        else:
            self.set_selected(False)
