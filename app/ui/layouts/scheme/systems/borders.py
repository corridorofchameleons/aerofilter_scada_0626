from PySide6.QtWidgets import QWidget, QGraphicsScene

from app.ui.layouts.scheme.scheme_layout import STAND_BORDER_HEIGHT, STAND_BORDER_WIDTH, START_OIL_X, START_BORDER_Y, \
    START_FUEL_X
from core.settings import Settings
from core.widgets.graphics.components.bounding_rect import BoundingRect


class BorderRectangles(QWidget):
    def __init__(
            self,
            scene: QGraphicsScene
    ):
        super().__init__()
        self.scene = scene

        self.oil_border = BoundingRect(
            height=STAND_BORDER_HEIGHT - 8,
            width=STAND_BORDER_WIDTH + 4,
            start_x=START_OIL_X - 2,
            start_y=START_BORDER_Y + 2,
            color=Settings.BORDER_OIL_COLOR
        )
        self.fuel_border = BoundingRect(
            height=STAND_BORDER_HEIGHT - 8,
            width=STAND_BORDER_WIDTH + 4,
            start_x=START_FUEL_X - 2,
            start_y=START_BORDER_Y + 2,
            color=Settings.BORDER_FUEL_COLOR
        )

        self.scene.addItem(self.oil_border)
        self.scene.addItem(self.fuel_border)
