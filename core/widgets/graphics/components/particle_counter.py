from PySide6.QtCore import Qt, QRectF, Slot
from PySide6.QtGui import QColor, QPen, QPainter, QBrush
from PySide6.QtWidgets import QLabel, QGraphicsItem

from core.models.items import Stateful
from core.models.tag import Tag
from core.settings import Settings


class ParticleCounter(QGraphicsItem, Stateful):
    def __init__(
            self,
            tag: Tag = None,
            radius: int = Settings.CIRCLE_LABEL_RADIUS,
    ):
        super().__init__()
        Stateful.__init__(self, tag)
        self.text = 'Счетчик\nчастиц'
        self.label = QLabel(self.text)
        self.radius = radius

    def boundingRect(self):
        return QRectF(
            -self.radius,
            -self.radius,
            self.radius * 2,
            self.radius * 2
        )

    def paint(self, painter, option, widget=None):
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        r = self.boundingRect()

        if self.tag and self.tag.value is True:
            bg_brush = QBrush(Settings.BUTTON_BACKGROUND_COLOR_ACTIVE)
        else:
            bg_brush = QBrush(Settings.ELEMENT_GRADIENT_DARK)

        painter.setBrush(bg_brush)
        painter.setPen(QPen(QColor(Settings.BORDER_COLOR), 2))
        painter.drawEllipse(r)

        font = painter.font()
        font.setPointSize(Settings.CIRCLE_LABEL_RADIUS * 0.28)
        font.setItalic(True)

        pen = QPen(QColor('black'))
        painter.setPen(pen)
        painter.setFont(font)

        painter.drawText(r, Qt.AlignmentFlag.AlignCenter, self.text)

    @Slot()
    def update_ui(self):
        self.update()
