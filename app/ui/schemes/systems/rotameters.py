from PySide6.QtCore import QObject
from PySide6.QtWidgets import QGraphicsScene

from app.ui.layouts.scheme_layout import OIL_ROTAMETER_X, OIL_ROTAMETER_Y, FUEL_ROTAMETER_X, FUEL_ROTAMETER_Y
from core.widgets.graphics.components.rotameter import Rotameter


class RotameterSystem(QObject):
    def __init__(
            self,
            scene: QGraphicsScene
    ):
        super().__init__()
        self.scene = scene

        self.oil_rotameter = Rotameter()
        self.oil_rotameter.setPos(OIL_ROTAMETER_X, OIL_ROTAMETER_Y)
        self.scene.addItem(self.oil_rotameter)

        self.fuel_rotameter = Rotameter()
        self.fuel_rotameter.setPos(FUEL_ROTAMETER_X, FUEL_ROTAMETER_Y)
        self.scene.addItem(self.fuel_rotameter)
