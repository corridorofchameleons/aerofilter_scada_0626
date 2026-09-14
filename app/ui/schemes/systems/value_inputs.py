from PySide6.QtCore import QObject
from PySide6.QtWidgets import QGraphicsScene, QGraphicsProxyWidget

from app.data.stands.fuel_stand import FuelStand
from app.data.stands.oil_stand import OilStand
from app.data.tags.value_tags import ValueTags
from app.ui.layouts.scheme_layout import OIL_TANK_TEMPERATURE_X, OIL_TANK_TEMPERATURE_Y, \
    FUEL_TANK_TEMPERATURE_Y, FUEL_TANK_TEMPERATURE_X, OIL_PUMP_X, OIL_PUMP_Y, FUEL_PUMP_X, FUEL_PUMP_Y, OIL_FLOW_X, \
    OIL_FLOW_Y, FUEL_FLOW_X, FUEL_FLOW_Y

from core.settings import Settings
from core.widgets.ui_widgets.error_widget import ErrorWidget
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
                ValueTags.units.get(OilStand.set_tank_temperature),
                'Заданная\nтемп., С',
                min_value=10,
                max_value=100,
                error_widget=True
            ),
             (OIL_TANK_TEMPERATURE_X + Settings.VALUE_BOX_WIDTH, OIL_TANK_TEMPERATURE_Y)),
            (ValueInput(
                ValueTags.units.get(OilStand.set_pump_frequency),
                'Частота,\n Гц',
                min_value=50,
                max_value=500,
                error_widget=True
            ),
             (OIL_PUMP_X - Settings.ERROR_WIDGET_WIDTH * 0.4,
              OIL_PUMP_Y - Settings.PUMP_HEIGHT - Settings.VALUE_BOX_HEIGHT * 1.2)),
            (ValueInput(
                ValueTags.units.get(OilStand.set_flow),
                'Заданный\nрасход',
                min_value=0,
                max_value=5000,
                error_widget=True
            ),
             (OIL_FLOW_X - Settings.ERROR_WIDGET_WIDTH * 0.8,
              OIL_FLOW_Y)),

            (ValueInput(
                ValueTags.units.get(FuelStand.set_tank_temperature),
                'Заданная\nтемп., С',
                error_widget=True
            ),
             (FUEL_TANK_TEMPERATURE_X + Settings.VALUE_BOX_WIDTH, FUEL_TANK_TEMPERATURE_Y)),
            (ValueInput(
                ValueTags.units.get(OilStand.set_pump_frequency),
                'Частота,\n Гц',
                min_value=50,
                max_value=500,
                error_widget=True
            ),
             (FUEL_PUMP_X - Settings.ERROR_WIDGET_WIDTH * 0.4,
              FUEL_PUMP_Y - Settings.PUMP_HEIGHT - Settings.VALUE_BOX_HEIGHT * 1.2)),
            (ValueInput(
                ValueTags.units.get(FuelStand.set_flow),
                'Заданный\nрасход',
                min_value=0,
                max_value=5000,
                error_widget=True
            ),
             (FUEL_FLOW_X - Settings.ERROR_WIDGET_WIDTH * 0.8,
              FUEL_FLOW_Y)),
        ]

        for vi in self.value_inputs:
            proxy_box = QGraphicsProxyWidget()
            proxy_box.setWidget(vi[0])
            proxy_box.setPos(*vi[1])
            self.scene.addItem(proxy_box)

        for vi in self.value_inputs:
            proxy_error = QGraphicsProxyWidget()
            if vi[0].error_widget:
                proxy_error.setWidget(vi[0].error_widget)
            self.scene.addItem(proxy_error)
            proxy_error.setPos(vi[1][0] + Settings.VALUE_BOX_WIDTH * 0.5 - Settings.ERROR_WIDGET_WIDTH * 0.5, vi[1][1] - Settings.ERROR_WIDGET_HEIGHT * 1.2)