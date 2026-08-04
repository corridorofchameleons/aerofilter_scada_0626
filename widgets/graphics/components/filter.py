from PySide6.QtCore import QRectF, QPointF
from PySide6.QtGui import QPainter, QPen, Qt, QColor, QPolygonF, QBrush, QTransform
from PySide6.QtWidgets import QGraphicsItem

from widgets.settings import Settings


class Filter(QGraphicsItem):
    def __init__(
            self,
            height: int = Settings.FILTER_HEIGHT,
            width: int = Settings.FILTER_WIDTH
    ):
        super().__init__()
        self.height = height
        self.width = width

        self.is_active = False

    def boundingRect(self):
        return QRectF(
            -self.width / 2,
            -self.height / 2,
            self.width,
            self.height
        )

    def __arrow(self, x_init, y_init, rotation_angle=0):
        x = self.boundingRect().center().x() + x_init
        y = self.boundingRect().center().y() + y_init
        points = [
            QPointF(x, y - Settings.ARROW_WIDTH / 2),
            QPointF(x + Settings.ARROW_LENGTH * 0.8, y),
            QPointF(x, y + Settings.ARROW_WIDTH * 0.5),
            QPointF(x, y + Settings.ARROW_WIDTH * 0.2),
            QPointF(x - Settings.ARROW_LENGTH, y + Settings.ARROW_WIDTH * 0.2),
            QPointF(x - Settings.ARROW_LENGTH, y - Settings.ARROW_WIDTH * 0.2),
            QPointF(x, y - Settings.ARROW_WIDTH * 0.2),
        ]

        polygon = QPolygonF(points)
        transform = QTransform()
        transform.rotate(rotation_angle)

        return transform.map(polygon)

    def paint(self, painter, option, widget=None):
        painter.setRenderHint(QPainter.Antialiasing, True)

        r = self.boundingRect()
        border_pen = QPen(Qt.NoPen)
        painter.setPen(border_pen)
        painter.setBrush(QColor(Settings.FILTER_BACKGROUND_COLOR))
        painter.drawRect(r)

        x_filter_left = int(r.left() + self.width * 0.3)
        filter_width = int(self.width * 0.7)
        y_filter_top = int(r.top() + self.height * 0.25)
        filter_height = int(self.height * 0.5)

        painter.setPen(QPen(QColor(Settings.BORDER_COLOR), Settings.LINE_WIDTH))
        painter.setBrush(QColor(Settings.FILTER_BACKGROUND_COLOR_2))
        painter.drawRect(x_filter_left, y_filter_top, filter_width, filter_height)

        painter.drawLine(
            int(x_filter_left + filter_width * 0.1),
            y_filter_top,
            int(x_filter_left + filter_width * 0.1),
            y_filter_top + filter_height
        )

        painter.drawLine(
            int(x_filter_left + filter_width * 0.1),
            int(y_filter_top + filter_height * 0.33),
            x_filter_left + filter_width,
            int(y_filter_top + filter_height * 0.33),
        )

        painter.drawLine(
            int(x_filter_left + filter_width * 0.1),
            int(y_filter_top + filter_height * 0.66),
            int(x_filter_left + filter_width),
            int(y_filter_top + filter_height * 0.66),
        )

        red_pen = QPen(QColor(Settings.ARROW_COLOR), 1)
        red_pen.setJoinStyle(Qt.PenJoinStyle.MiterJoin)
        red_brush = QBrush(QColor(Settings.ARROW_COLOR))
        painter.setPen(red_pen)
        painter.setBrush(red_brush)

        arrow_1 = self.__arrow(-self.width * 0.36, 0)
        painter.drawPolygon(arrow_1)

        arrow_2 = self.__arrow(-self.width * 0.36, -self.height * 0.36, 90)
        painter.drawPolygon(arrow_2)

        arrow_3 = self.__arrow(-self.width * 0.36, -self.height * 0.18, 90)
        painter.drawPolygon(arrow_3)

        arrow_4 = self.__arrow(-self.width * 0.36, -self.height * 0.00, 90)
        painter.drawPolygon(arrow_4)

        arrow_5 = self.__arrow(-self.width * 0.36, self.height * 0.36, -90)
        painter.drawPolygon(arrow_5)

        arrow_6 = self.__arrow(-self.width * 0.36, self.height * 0.18, -90)
        painter.drawPolygon(arrow_6)

        arrow_7 = self.__arrow(-self.width * 0.36, self.height * 0.00, -90)
        painter.drawPolygon(arrow_7)

        painter.setPen(QPen(QColor(Settings.BORDER_COLOR), Settings.LINE_WIDTH))
        painter.setBrush(Qt.NoBrush)
        painter.drawRect(r)
