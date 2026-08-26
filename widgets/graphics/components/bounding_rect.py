from PySide6.QtCore import QRectF, QPointF, Slot
from PySide6.QtGui import QPainter, QPen, QColor, QPainterPath, QPolygonF, QLinearGradient, Qt, QBrush
from PySide6.QtWidgets import QGraphicsItem, QGraphicsItemGroup

from widgets.graphics.layouts.scheme_layout import STAND_BORDER_HEIGHT, STAND_BORDER_WIDTH, START_OIL_X, START_OIL_Y, \
    START_FUEL_X, START_BORDER_Y
from widgets.settings import Settings

class BoundingRect(QGraphicsItem):
    def __init__(
            self,
            position: int,
    ):
        super().__init__()
        self.position = position
        self.color = Settings.BORDER_OIL_COLOR if self.position == 1 else Settings.BORDER_FUEL_COLOR
        self.start_x = START_OIL_X if self.position == 1 else START_FUEL_X

    def boundingRect(self):
        return QRectF(
            self.start_x,
            START_BORDER_Y,
            STAND_BORDER_WIDTH,
            STAND_BORDER_HEIGHT
        )

    def paint(self, painter, option, widget=None):
        painter.setRenderHint(QPainter.Antialiasing, False)
        pen = QPen(QColor(self.color), 3)
        pen.setJoinStyle(Qt.MiterJoin)

        painter.setPen(pen)
        painter.drawRect(self.boundingRect())