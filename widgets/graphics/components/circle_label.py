from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QBrush, QColor, QPen, QPainter, QFont
from PySide6.QtWidgets import QLabel, QGraphicsItem

from widgets.graphics.constants import CIRCLE_LABEL_RADIUS, BORDER_COLOR


class CircleLabel(QGraphicsItem):
    def __init__(self, text: str):
        super().__init__()
        self.text = text
        self.label = QLabel()
        self.label.setText(text)

    def boundingRect(self):
        return QRectF(
            -CIRCLE_LABEL_RADIUS,
            -CIRCLE_LABEL_RADIUS,
            CIRCLE_LABEL_RADIUS * 2,
            CIRCLE_LABEL_RADIUS * 2
        )

    def paint(self, painter, option, widget=None):
        painter.setRenderHint(QPainter.Antialiasing, True)
        r = self.boundingRect()

        bg_brush = painter.background()
        painter.setBrush(bg_brush)  # Серый фон
        painter.setPen(QPen(QColor(BORDER_COLOR), 2))
        painter.drawEllipse(r)

        font = painter.font()
        font.setPointSize(CIRCLE_LABEL_RADIUS * 0.28)
        font.setItalic(True)

        pen = QPen(QColor('black'))
        painter.setPen(pen)
        painter.setFont(font)

        painter.drawText(r, Qt.AlignCenter, self.text)

