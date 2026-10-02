from PySide6.QtCore import QRectF
from PySide6.QtGui import QPainter, QPen, QColor, Qt
from PySide6.QtWidgets import QGraphicsItem

from core.settings import Settings

class BoundingRect(QGraphicsItem):
    def __init__(
            self,
            height: int,
            width: int,
            start_x: int,
            start_y: int,
            color: str = 'white',
            thickness: int = 2

    ):
        super().__init__()
        self.color = color
        self.start_x = start_x
        self.start_y = start_y
        self.height = height
        self.width = width
        self.thickness = thickness

        self.highlighted = False
        self.setZValue(0)

    def boundingRect(self):
        return QRectF(
            self.start_x - 2,
            self.start_y - 2,
            self.width + 4,
            self.height + 4
        )

    def paint(self, painter, option, widget=None):
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, False)

        if not self.highlighted:
            pen = QPen(QColor(self.color), self.thickness)
        else:
            pen = QPen(QColor(Settings.BORDER_ACTIVE_COLOR), self.thickness * 3)

        pen.setJoinStyle(Qt.PenJoinStyle.MiterJoin)

        painter.setPen(pen)
        painter.drawRect(QRectF(self.start_x, self.start_y, self.width, self.height))

    def set_highlighted(self, val: bool):
        self.highlighted = val
        self.update()
