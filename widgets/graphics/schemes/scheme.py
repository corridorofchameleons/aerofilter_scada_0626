from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QPen, QColor, QWheelEvent, QPainter
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsItem, QWidget

from widgets.graphics.components.bounding_rect import BoundingRect
from widgets.graphics.layouts.scheme_layout import STAND_BORDER_HEIGHT, STAND_BORDER_WIDTH, START_OIL_X, START_OIL_Y, \
    START_X, START_Y, WIDTH, HEIGHT
from widgets.settings import Settings


class _BorderRectangles(QWidget):
    def __init__(
            self,
            scene: QGraphicsScene
    ):
        super().__init__()
        self.scene = scene

        self.oil_border = BoundingRect(position=1)
        self.fuel_border = BoundingRect(position=2)
        self.scene.addItem(self.oil_border)
        self.scene.addItem(self.fuel_border)

class Scheme(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setObjectName('scheme')

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # Отключаем горизонтальный скролл
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setDragMode(QGraphicsView.NoDrag)

        self.scene = QGraphicsScene()
        self.scene.setSceneRect(START_X, START_Y, WIDTH, HEIGHT)
        self.setScene(self.scene)

        self.oil_border = _BorderRectangles(self.scene)

    def wheelEvent(self, event: QWheelEvent):
        pass