from PySide6.QtCore import QObject
from PySide6.QtWidgets import QGraphicsScene

from app.data.stands.fuel_stand import FuelStand
from app.data.stands.oil_stand import OilStand
from app.data.tags.binary_tags import BinaryTags
from app.ui.layouts.scheme_layout import OIL_LAMP_X, OIL_LAMP_Y, FUEL_LAMP_Y, FUEL_LAMP_X
from core.widgets.graphics.components.lamp import Lamp


class LampSystem(QObject):
    def __init__(
            self,
            scene: QGraphicsScene
    ):
        super().__init__()
        self.scene = scene

        self.oil_lamp = Lamp(BinaryTags.units.get(OilStand.light))
        self.oil_lamp.setPos(OIL_LAMP_X, OIL_LAMP_Y)
        self.scene.addItem(self.oil_lamp)

        self.fuel_lamp = Lamp(BinaryTags.units.get(FuelStand.light))
        self.fuel_lamp.setPos(FUEL_LAMP_X, FUEL_LAMP_Y)
        self.scene.addItem(self.fuel_lamp)
