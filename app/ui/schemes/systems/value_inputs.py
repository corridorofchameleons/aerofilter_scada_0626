from PySide6.QtCore import QObject
from PySide6.QtWidgets import QGraphicsScene, QGraphicsProxyWidget

from app.instances.fuel_stand import FuelStand
from app.instances.oil_stand import OilStand
from app.ui.layouts.scheme_layout import OIL_TANK_TEMPERATURE_X, OIL_TANK_TEMPERATURE_Y, \
    OIL_PUMP_X, OIL_PUMP_Y, OIL_FLOW_X, \
    OIL_FLOW_Y, FUEL_TANK_TEMPERATURE_X, FUEL_TANK_TEMPERATURE_Y, FUEL_PUMP_X, FUEL_PUMP_Y, FUEL_FLOW_X, FUEL_FLOW_Y

from core.settings import Settings
from core.widgets.ui_widgets.value_input import ValueInput


class ValueInputSystem(QObject):
    def __init__(
            self,
            scene: QGraphicsScene
    ):
        super().__init__()
        self.scene = scene

        self.value_inputs = [
            (ValueInput(
                OilStand.oil_set_tank_temperature,
                'Заданная\nтемп., С',
                min_value=10,
                max_value=100
            ),
             (OIL_TANK_TEMPERATURE_X + Settings.VALUE_BOX_WIDTH, OIL_TANK_TEMPERATURE_Y)),
            (ValueInput(
                OilStand.oil_set_pump_frequency,
                'Частота,\n Гц',
                min_value=0,
                max_value=100
            ),
             (OIL_PUMP_X - Settings.ERROR_WIDGET_WIDTH * 0.4,
              OIL_PUMP_Y - Settings.PUMP_HEIGHT - Settings.VALUE_BOX_HEIGHT * 1.2)),
            (ValueInput(
                OilStand.oil_set_flow,
                'Заданный\nрасход',
                min_value=0,
                max_value=5000
            ),
             (OIL_FLOW_X - Settings.ERROR_WIDGET_WIDTH * 0.8,
              OIL_FLOW_Y)),

            (ValueInput(
                FuelStand.fuel_set_tank_temperature,
                'Заданная\nтемп., С',
                min_value=10,
                max_value=100
            ),
             (FUEL_TANK_TEMPERATURE_X + Settings.VALUE_BOX_WIDTH, FUEL_TANK_TEMPERATURE_Y)),
            (ValueInput(
                FuelStand.fuel_set_pump_frequency,
                'Частота,\n Гц',
                min_value=0,
                max_value=100
            ),
             (FUEL_PUMP_X - Settings.ERROR_WIDGET_WIDTH * 0.4,
              FUEL_PUMP_Y - Settings.PUMP_HEIGHT - Settings.VALUE_BOX_HEIGHT * 1.2)),
            (ValueInput(
                FuelStand.fuel_set_flow,
                'Заданный\nрасход',
                min_value=0,
                max_value=5000
            ),
             (FUEL_FLOW_X - Settings.ERROR_WIDGET_WIDTH * 0.8,
              FUEL_FLOW_Y)),
        ]

        for vi in self.value_inputs:
            proxy_box = QGraphicsProxyWidget()
            proxy_box.setWidget(vi[0])
            proxy_box.setPos(*vi[1])
            self.scene.addItem(proxy_box)

            proxy_error = QGraphicsProxyWidget()
            proxy_error.setWidget(vi[0].error_widget)
            proxy_error.setZValue(20)
            self.scene.addItem(proxy_error)
            proxy_error.setPos(vi[1][0] + Settings.VALUE_BOX_WIDTH * 0.5 - Settings.ERROR_WIDGET_WIDTH * 0.5,
                               vi[1][1] - Settings.ERROR_WIDGET_HEIGHT * 1.2)
