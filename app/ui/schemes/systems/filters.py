from PySide6.QtCore import QObject
from PySide6.QtWidgets import QGraphicsScene

from app.ui.layouts.scheme_layout import OIL_FILTER_X, OIL_FILTER_Y, OIL_FILTER_SMALL_X, OIL_FILTER_SMALL_Y, \
    FUEL_FILTER_X, FUEL_FILTER_Y, FUEL_FILTER_SMALL_X, FUEL_FILTER_SMALL_Y
from core.widgets.graphics.components.filter import Filter


class FilterSystem(QObject):
    def __init__(
            self,
            scene: QGraphicsScene,
    ):
        super().__init__()
        self.scene = scene

        self.oil_filter = Filter()
        self.scene.addItem(self.oil_filter)
        self.oil_filter.setPos(OIL_FILTER_X, OIL_FILTER_Y)

        self.oil_filter_small = Filter(small=True, rotation=270)
        self.scene.addItem(self.oil_filter_small)
        self.oil_filter_small.setPos(OIL_FILTER_SMALL_X, OIL_FILTER_SMALL_Y)

        self.fuel_filter = Filter()
        self.scene.addItem(self.fuel_filter)
        self.fuel_filter.setPos(FUEL_FILTER_X, FUEL_FILTER_Y)

        self.fuel_filter_small = Filter(small=True, rotation=270)
        self.scene.addItem(self.fuel_filter_small)
        self.fuel_filter_small.setPos(FUEL_FILTER_SMALL_X, FUEL_FILTER_SMALL_Y)
