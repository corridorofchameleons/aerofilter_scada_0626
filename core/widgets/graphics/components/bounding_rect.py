from PySide6.QtCore import QRectF
from PySide6.QtGui import QPainter, QPen, QColor, Qt
from PySide6.QtWidgets import QGraphicsItem

# from app.layouts.scheme_layout import STAND_BORDER_HEIGHT, STAND_BORDER_WIDTH, START_OIL_X, START_FUEL_X, START_BORDER_Y
from core.settings import Settings

class BoundingRect(QGraphicsItem):
    def __init__(
            self,
            position: int,
            height: int,
            width: int,
            start_x: int,
            start_y: int
    ):
        super().__init__()
        self.position = position
        self.color = Settings.BORDER_OIL_COLOR if self.position == 1 else Settings.BORDER_FUEL_COLOR
        self.start_x = start_x
        self.start_y = start_y
        self.height = height
        self.width = width

    def boundingRect(self):
        return QRectF(
            self.start_x,
            self.start_y,
            self.width,
            self.height
        )

    def paint(self, painter, option, widget=None):
        painter.setRenderHint(QPainter.Antialiasing, False)
        pen = QPen(QColor(self.color), 3)
        pen.setJoinStyle(Qt.MiterJoin)

        painter.setPen(pen)
        painter.drawRect(self.boundingRect())