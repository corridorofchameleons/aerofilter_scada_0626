from PySide6.QtCore import QObject
from PySide6.QtWidgets import QGraphicsScene

from app.instances.stands import FuelStand, OilStand
from app.ui.layouts.scheme_layout import OIL_LAMP_X, OIL_LAMP_Y, FUEL_LAMP_X, FUEL_LAMP_Y
from core.widgets.graphics.components.lamp import Lamp


class LampSystem(QObject):
    def __init__(
            self,
            scene: QGraphicsScene
    ):
        super().__init__()
        self.scene = scene

        self.oil_lamp = Lamp(OilStand.oil_light)
        self.oil_lamp.setPos(OIL_LAMP_X, OIL_LAMP_Y)
        self.scene.addItem(self.oil_lamp)

        self.fuel_lamp = Lamp(FuelStand.fuel_light)
        self.fuel_lamp.setPos(FUEL_LAMP_X, FUEL_LAMP_Y)
        self.scene.addItem(self.fuel_lamp)
