from PySide6.QtCore import QObject
from PySide6.QtWidgets import QGraphicsScene, QGraphicsProxyWidget

from app.instances.stands import FuelStand, OilStand
from app.ui.layouts.scheme_layout import OIL_PUMP_X, OIL_PUMP_Y, OIL_SMALL_PUMP_X, OIL_SMALL_PUMP_Y, FUEL_PUMP_X, \
    FUEL_PUMP_Y, FUEL_SMALL_PUMP_X, FUEL_SMALL_PUMP_Y
from core.settings import Settings
from core.widgets.graphics.components.pump import Pump


class PumpSystem(QObject):
    def __init__(
            self,
            scene: QGraphicsScene,
            flow_signal,
    ):
        super().__init__()
        self.scene = scene

        self.oil_pump_1 = Pump((1, 2, 3, 5), tag=OilStand.oil_main_pump, freq_tag=OilStand.oil_set_pump_frequency,
                               switch_flow=flow_signal)
        self.scene.addItem(self.oil_pump_1)
        self.oil_pump_1.setPos(OIL_PUMP_X, OIL_PUMP_Y)

        proxy_error = QGraphicsProxyWidget()
        proxy_error.setZValue(10)
        proxy_error.setWidget(self.oil_pump_1.error_widget)
        self.scene.addItem(proxy_error)
        proxy_error.setPos(OIL_PUMP_X - Settings.ERROR_WIDGET_WIDTH * 0.5,
                           OIL_PUMP_Y - Settings.ERROR_WIDGET_HEIGHT * 1.5)

        self.oil_pump_2 = Pump((4, 6), tag=OilStand.oil_mixing_pump, switch_flow=flow_signal, small=True)
        self.oil_pump_2.freq = 50
        self.scene.addItem(self.oil_pump_2)
        self.oil_pump_2.setPos(OIL_SMALL_PUMP_X, OIL_SMALL_PUMP_Y)

        proxy_error = QGraphicsProxyWidget()
        proxy_error.setZValue(10)
        proxy_error.setWidget(self.oil_pump_2.error_widget)
        self.scene.addItem(proxy_error)
        proxy_error.setPos(OIL_SMALL_PUMP_X - Settings.ERROR_WIDGET_WIDTH * 0.5,
                           OIL_SMALL_PUMP_Y - Settings.ERROR_WIDGET_HEIGHT * 1.5)

        self.fuel_pump_1 = Pump((7, 8, 9, 11), tag=FuelStand.fuel_main_pump, freq_tag=FuelStand.fuel_set_pump_frequency,
                                switch_flow=flow_signal)
        self.scene.addItem(self.fuel_pump_1)
        self.fuel_pump_1.setPos(FUEL_PUMP_X, FUEL_PUMP_Y)

        proxy_error = QGraphicsProxyWidget()
        proxy_error.setZValue(10)
        proxy_error.setWidget(self.fuel_pump_1.error_widget)
        self.scene.addItem(proxy_error)
        proxy_error.setPos(FUEL_PUMP_X - Settings.ERROR_WIDGET_WIDTH * 0.5,
                           FUEL_PUMP_Y - Settings.ERROR_WIDGET_HEIGHT * 1.5)

        self.fuel_pump_2 = Pump((10, 12), tag=FuelStand.fuel_mixing_pump, switch_flow=flow_signal, small=True)
        self.fuel_pump_2.freq = 50
        self.scene.addItem(self.fuel_pump_2)
        self.fuel_pump_2.setPos(FUEL_SMALL_PUMP_X, FUEL_SMALL_PUMP_Y)

        proxy_error = QGraphicsProxyWidget()
        proxy_error.setZValue(10)
        proxy_error.setWidget(self.fuel_pump_2.error_widget)
        self.scene.addItem(proxy_error)
        proxy_error.setPos(FUEL_SMALL_PUMP_X - Settings.ERROR_WIDGET_WIDTH * 0.5,
                           FUEL_SMALL_PUMP_Y - Settings.ERROR_WIDGET_HEIGHT * 1.5)
