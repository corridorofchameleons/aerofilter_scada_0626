from PySide6.QtCore import QObject
from PySide6.QtWidgets import QGraphicsScene, QGraphicsProxyWidget

from app.data.stands.fuel_stand import FuelStand
from app.data.stands.oil_stand import OilStand
from app.data.tags.value_tags import ValueTags
from app.ui.layouts.scheme_layout import OIL_TANK_TEMPERATURE_X, OIL_TANK_TEMPERATURE_Y, \
    FUEL_TANK_TEMPERATURE_Y, FUEL_TANK_TEMPERATURE_X

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
            (ValueInput(ValueTags.units.get(OilStand.set_tank_temperature), 'Заданная\nтемп., С', min_value=10, max_value=100),
             (OIL_TANK_TEMPERATURE_X + Settings.VALUE_BOX_WIDTH, OIL_TANK_TEMPERATURE_Y)),

            (ValueInput(ValueTags.units.get(FuelStand.set_tank_temperature), 'Заданная\nтемп., С'),
             (FUEL_TANK_TEMPERATURE_X + Settings.VALUE_BOX_WIDTH, FUEL_TANK_TEMPERATURE_Y)),
        ]

        for vi in self.value_inputs:
            proxy = QGraphicsProxyWidget()
            proxy.setWidget(vi[0])
            self.scene.addItem(proxy)
            proxy.setPos(*vi[1])