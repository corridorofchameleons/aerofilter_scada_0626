from PySide6.QtCore import QRectF
from PySide6.QtGui import QPainter, QPen, Qt, QColor, QBrush
from PySide6.QtWidgets import QGraphicsItem, QGraphicsItemGroup

from widgets.graphics.components.arrow import Arrow
from widgets.settings import Settings


class _FilterBody(QGraphicsItem):
    def __init__(
            self,
            height: int = Settings.FILTER_HEIGHT,
            width: int = Settings.FILTER_WIDTH,
            small: bool = False
    ):
        super().__init__()
        self.height = height
        self.width = width

        if small:
            self.height *= 0.5
            self.width *= 0.5

        self.is_active = False

    def boundingRect(self):
        return QRectF(
            -self.width / 2,
            -self.height / 2,
            self.width,
            self.height
        )

    def paint(self, painter, option, widget=None):
        painter.setRenderHint(QPainter.Antialiasing, True)

        r = self.boundingRect()
        border_pen = QPen(Qt.NoPen)
        painter.setPen(border_pen)
        painter.setBrush(QColor(Settings.FILTER_BACKGROUND_COLOR))
        painter.drawRect(r)

        x_filter_left = int(r.left())
        filter_width = int(self.width * 0.7)
        y_filter_top = int(r.top() + self.height * 0.25)
        filter_height = int(self.height * 0.5)

        painter.setPen(QPen(QColor(Settings.BORDER_COLOR), Settings.LINE_WIDTH))
        painter.setBrush(QColor(Settings.FILTER_BACKGROUND_COLOR_2))
        painter.drawRect(x_filter_left, y_filter_top, filter_width, filter_height)

        painter.drawLine(
            int(x_filter_left + filter_width * 0.85),
            int(y_filter_top * 0.98),
            int(x_filter_left + filter_width * 0.85),
            int((y_filter_top + filter_height) * 0.98)
        )

        painter.drawLine(
            int(x_filter_left),
            int(y_filter_top + filter_height * 0.33),
            int(x_filter_left + filter_width * 0.84),
            int(y_filter_top + filter_height * 0.33),
        )

        painter.drawLine(
            int(x_filter_left),
            int(y_filter_top + filter_height * 0.66),
            int(x_filter_left + filter_width * 0.84),
            int(y_filter_top + filter_height * 0.66),
        )

        red_pen = QPen(QColor(Settings.ARROW_COLOR), 1)
        red_pen.setJoinStyle(Qt.PenJoinStyle.MiterJoin)
        red_brush = QBrush(QColor(Settings.ARROW_COLOR))
        painter.setPen(red_pen)
        painter.setBrush(red_brush)

        painter.setPen(QPen(QColor(Settings.BORDER_COLOR), Settings.LINE_WIDTH))
        painter.setBrush(Qt.NoBrush)
        painter.drawRect(r)


class Filter(QGraphicsItemGroup):
    def __init__(self, small=False, rotation=0):
        super().__init__()
        self.small = small
        self.filter_body = _FilterBody(small=self.small)
        self.addToGroup(self.filter_body)

        arrow_1 = Arrow(small=self.small, rotation_angle=180)
        arrow_1.setPos(self.filter_body.width * 0.4, 0)
        self.addToGroup(arrow_1)

        arrow_2 = Arrow(small=self.small, rotation_angle=90)
        arrow_2.setPos(-self.filter_body.width * 0.36, -self.filter_body.height * 0.36)
        self.addToGroup(arrow_2)

        arrow_3 = Arrow(small=self.small, rotation_angle=90)
        arrow_3.setPos(-self.filter_body.width * 0.18, -self.filter_body.height * 0.36)
        self.addToGroup(arrow_3)

        arrow_4 = Arrow(small=self.small, rotation_angle=90)
        arrow_4.setPos(-self.filter_body.width * 0.00, -self.filter_body.height * 0.36)
        self.addToGroup(arrow_4)

        arrow_5 = Arrow(small=self.small, rotation_angle=270)
        arrow_5.setPos(-self.filter_body.width * 0.36, self.filter_body.height * 0.36)
        self.addToGroup(arrow_5)

        arrow_6 = Arrow(small=self.small, rotation_angle=270)
        arrow_6.setPos(-self.filter_body.width * 0.18, self.filter_body.height * 0.36)
        self.addToGroup(arrow_6)

        arrow_7 = Arrow(small=self.small, rotation_angle=270)
        arrow_7.setPos(-self.filter_body.width * 0.00, self.filter_body.height * 0.36)
        self.addToGroup(arrow_7)

        if rotation:
            self.setRotation(rotation)


        # arrow_2 = self.__arrow(-self.width * 0.36, -self.height * 0.36, 90)
        # painter.drawPolygon(arrow_2)
        #
        # arrow_3 = self.__arrow(-self.width * 0.36, -self.height * 0.18, 90)
        # painter.drawPolygon(arrow_3)
        #
        # arrow_4 = self.__arrow(-self.width * 0.36, -self.height * 0.00, 90)
        # painter.drawPolygon(arrow_4)
        #
        # arrow_5 = self.__arrow(-self.width * 0.36, self.height * 0.36, -90)
        # painter.drawPolygon(arrow_5)
        #
        # arrow_6 = self.__arrow(-self.width * 0.36, self.height * 0.18, -90)
        # painter.drawPolygon(arrow_6)
        #
        # arrow_7 = self.__arrow(-self.width * 0.36, self.height * 0.00, -90)
        # painter.drawPolygon(arrow_7)