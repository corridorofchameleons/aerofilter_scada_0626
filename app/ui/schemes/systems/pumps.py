from PySide6.QtCore import QObject
from PySide6.QtWidgets import QGraphicsScene

from app.instances.fuel_stand import FuelStand
from app.instances.oil_stand import OilStand
from app.ui.layouts.scheme_layout import OIL_PUMP_X, OIL_PUMP_Y, OIL_SMALL_PUMP_X, OIL_SMALL_PUMP_Y, FUEL_PUMP_X, \
    FUEL_PUMP_Y, FUEL_SMALL_PUMP_X, FUEL_SMALL_PUMP_Y
from core.widgets.graphics.components.pump import Pump


class PumpSystem(QObject):
    def __init__(
            self,
            scene: QGraphicsScene,
            flow_signal,
    ):
        super().__init__()
        self.scene = scene

        self.oil_pump_1 = Pump((1, 2, 3, 5), tag=OilStand.oil_main_pump, switch_flow=flow_signal)
        self.scene.addItem(self.oil_pump_1)
        self.oil_pump_1.setPos(OIL_PUMP_X, OIL_PUMP_Y)

        self.oil_pump_2 = Pump((4, 6), tag=OilStand.oil_mixing_pump, switch_flow=flow_signal, small=True)
        self.scene.addItem(self.oil_pump_2)
        self.oil_pump_2.setPos(OIL_SMALL_PUMP_X, OIL_SMALL_PUMP_Y)

        self.fuel_pump_1 = Pump((7, 8, 9, 11), FuelStand.fuel_main_pump, flow_signal)
        self.scene.addItem(self.fuel_pump_1)
        self.fuel_pump_1.setPos(FUEL_PUMP_X, FUEL_PUMP_Y)

        self.fuel_pump_2 = Pump((10, 12), FuelStand.fuel_mixing_pump, flow_signal, small=True)
        self.scene.addItem(self.fuel_pump_2)
        self.fuel_pump_2.setPos(FUEL_SMALL_PUMP_X, FUEL_SMALL_PUMP_Y)
