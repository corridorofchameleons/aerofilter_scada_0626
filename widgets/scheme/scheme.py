from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QPen, QColor
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QGraphicsView, QGraphicsScene

from widgets.scheme.components.valve import Valve

WIDGET_SIZE = 1000, 500

class Scheme(QGraphicsView):
    def __init__(self, parent=None, ratio=1):
        super().__init__(parent)
        self.ratio = ratio
        self.setFixedSize(self.ratio * WIDGET_SIZE[0], self.ratio * WIDGET_SIZE[1])
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setObjectName('schemeView')

        self.scene = QGraphicsScene()
        self.setScene(self.scene)

        self.valve = Valve(self.ratio, 0, 0)
        self.scene.addItem(self.valve)
