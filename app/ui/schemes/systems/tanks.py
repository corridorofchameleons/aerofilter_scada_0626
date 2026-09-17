from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QGraphicsScene, QGraphicsProxyWidget

from app.instances.stands import FuelStand, OilStand
from app.ui.layouts.scheme_layout import OIL_TANK_X, OIL_TANK_Y, OIL_SMALL_TANK_X, OIL_SMALL_TANK_Y, FUEL_TANK_X, \
    FUEL_TANK_Y, FUEL_SMALL_TANK_X, FUEL_SMALL_TANK_Y
from core.settings import Settings
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

        self.oil_tank = Tank(heater_tag=OilStand.oil_tank_heater, rotate=True)
        self.scene.addItem(self.oil_tank)
        self.oil_tank.setPos(OIL_TANK_X, OIL_TANK_Y)

        proxy_error = QGraphicsProxyWidget()
        proxy_error.setZValue(6)
        proxy_error.setWidget(self.oil_tank.heater.error_widget)
        self.scene.addItem(proxy_error)
        proxy_error.setPos(OIL_TANK_X - Settings.ERROR_WIDGET_WIDTH * 0.5,
                           OIL_TANK_Y - Settings.ERROR_WIDGET_HEIGHT * 1.5)

        self.oil_tank_small = Tank(small=True)
        self.scene.addItem(self.oil_tank_small)
        self.oil_tank_small.setPos(OIL_SMALL_TANK_X, OIL_SMALL_TANK_Y)

        self.fuel_tank = Tank(heater_tag=FuelStand.fuel_tank_heater, rotate=True)
        self.scene.addItem(self.fuel_tank)
        self.fuel_tank.setPos(FUEL_TANK_X, FUEL_TANK_Y)

        proxy_error = QGraphicsProxyWidget()
        proxy_error.setZValue(6)
        proxy_error.setWidget(self.fuel_tank.heater.error_widget)
        self.scene.addItem(proxy_error)
        proxy_error.setPos(FUEL_TANK_X - Settings.ERROR_WIDGET_WIDTH * 0.5,
                           FUEL_TANK_Y - Settings.ERROR_WIDGET_HEIGHT * 1.5)

        self.fuel_tank_small = Tank(small=True)
        self.scene.addItem(self.fuel_tank_small)
        self.fuel_tank_small.setPos(FUEL_SMALL_TANK_X, FUEL_SMALL_TANK_Y)
