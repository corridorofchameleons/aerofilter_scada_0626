from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPainter, QPen, QColor, QWheelEvent
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QGraphicsView, QGraphicsScene

from widgets.scheme.components.valve import Valve
from widgets.scheme.components.pump import Pump

WIDGET_SIZE: tuple[int, int] = 1500, 800

class Scheme(QGraphicsView):
    def __init__(self, parent=None, ratio=1.2):
        super().__init__(parent)
        self.ratio = ratio
        self.setFixedSize(WIDGET_SIZE[0], WIDGET_SIZE[1])
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setObjectName('schemeView')

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # Отключаем горизонтальный скролл
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setDragMode(QGraphicsView.NoDrag)

        self.scene = QGraphicsScene()
        self.setScene(self.scene)

        self.valve = Valve(self.ratio, 100, 100)
        self.pump = Pump(
            self.ratio, -100, -100
        )

        self.scene.addItem(self.valve)
        self.scene.addItem(self.pump)
        self.pump.rotate()


    def wheelEvent(self, event: QWheelEvent):
        pass


