from PySide6.QtWidgets import QWidget, QGraphicsScene

from app.ui.layouts.scheme_layout import STAND_BORDER_HEIGHT, STAND_BORDER_WIDTH, START_OIL_X, START_BORDER_Y, \
    START_FUEL_X
from core.widgets.graphics.components.bounding_rect import BoundingRect


class BorderRectangles(QWidget):
    def __init__(
            self,
            scene: QGraphicsScene
    ):
        super().__init__()
        self.scene = scene

        self.oil_border = BoundingRect(
            position=1,
            height=STAND_BORDER_HEIGHT,
            width=STAND_BORDER_WIDTH,
            start_x=START_OIL_X,
            start_y=START_BORDER_Y
        )
        self.fuel_border = BoundingRect(
            position=2,
            height=STAND_BORDER_HEIGHT,
            width=STAND_BORDER_WIDTH,
            start_x=START_FUEL_X,
            start_y=START_BORDER_Y
        )
        self.scene.addItem(self.oil_border)
        self.scene.addItem(self.fuel_border)
