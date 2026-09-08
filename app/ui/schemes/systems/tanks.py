from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QGraphicsScene

from app.data.stands.fuel_stand import FuelStand
from app.data.stands.oil_stand import OilStand
from app.data.tags.binary_tags import BinaryTags
from app.ui.layouts.scheme_layout import OIL_TANK_X, OIL_TANK_Y, OIL_SMALL_TANK_X, OIL_SMALL_TANK_Y, FUEL_TANK_X, \
    FUEL_TANK_Y, FUEL_SMALL_TANK_X, FUEL_SMALL_TANK_Y
from core.widgets.graphics.components.tank import Tank


class TankSystem(QObject):
    oil_alarm_max_signal = Signal(bool)
    oil_alarm_min_signal = Signal(bool)

    def __init__(
            self,
            scene: QGraphicsScene,
            # heater_signal,
            # alarm_max_signal,
            # alarm_min_signal
    ):
        super().__init__()
        self.scene = scene

        # self.heater_signal = heater_signal
        # self.alarm_max_signal = alarm_max_signal
        # self.alarm_min_signal = alarm_min_signal

        self.oil_tank = Tank(BinaryTags.units.get(OilStand.tank_heater), rotate=True)
        self.scene.addItem(self.oil_tank)
        self.oil_tank.setPos(OIL_TANK_X, OIL_TANK_Y)

        self.oil_tank_small = Tank(None, small=True)
        self.scene.addItem(self.oil_tank_small)
        self.oil_tank_small.setPos(OIL_SMALL_TANK_X, OIL_SMALL_TANK_Y)

        self.fuel_tank = Tank(BinaryTags.units.get(FuelStand.tank_heater), rotate=True)
        self.scene.addItem(self.fuel_tank)
        self.fuel_tank.setPos(FUEL_TANK_X, FUEL_TANK_Y)

        self.fuel_tank_small = Tank(None, small=True)
        self.scene.addItem(self.fuel_tank_small)
        self.fuel_tank_small.setPos(FUEL_SMALL_TANK_X, FUEL_SMALL_TANK_Y)
