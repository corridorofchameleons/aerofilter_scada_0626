from PySide6.QtCore import QRectF, Slot
from PySide6.QtGui import QPainter, QPen, QColor
from PySide6.QtWidgets import QGraphicsItem

from core.models.tag import Tag
from core.settings import Settings


class Lamp(QGraphicsItem):
    def __init__(
            self,
            tag: Tag,
            radius: int = Settings.LAMP_SIZE,
    ):
        super().__init__()
        self.tag = tag
        if self.tag:
            self.tag.signal_fn.connect(self.update_status)

        self.radius = radius
        self.active = False

    def boundingRect(self):
        return QRectF(
            -self.radius / 2,
            -self.radius / 2,
            self.radius,
            self.radius
        )

    @Slot(bool)
    def update_status(self, val: bool):
        self.active = val
        self.update()

    def paint(self, painter, option, widget=None):

        painter.setRenderHint(QPainter.Antialiasing, True)

        r = self.boundingRect()

        pen = QPen(QColor('black'), 3)

        color = Settings.LAMP_ACTIVE_COLOR if self.active else Settings.LAMP_INACTIVE_COLOR

        painter.setBrush(QColor(color))
        painter.setPen(pen)

        painter.drawEllipse(r)
