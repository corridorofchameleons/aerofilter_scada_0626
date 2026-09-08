from PySide6.QtCore import QObject
from PySide6.QtWidgets import QGraphicsScene, QGraphicsProxyWidget

from app.data.stands.fuel_stand import FuelStand
from app.data.stands.oil_stand import OilStand
from app.data.tags.telemetry_tags import Tags
from app.ui.layouts.scheme_layout import OIL_PRESSURE_BEFORE_X, OIL_PRESSURE_BEFORE_Y, \
    OIL_TEMPERATURE_BEFORE_X, OIL_TEMPERATURE_AFTER_Y, OIL_PRESSURE_AFTER_Y, OIL_PRESSURE_AFTER_X, \
    OIL_TEMPERATURE_BEFORE_Y, OIL_TEMPERATURE_AFTER_X, OIL_MOISTURE_BEFORE_X, OIL_MOISTURE_AFTER_Y, \
    OIL_MOISTURE_BEFORE_Y, OIL_MOISTURE_AFTER_X, OIL_TANK_TEMPERATURE_X, OIL_TANK_TEMPERATURE_Y, OIL_PUMP_FREQ_X, \
    OIL_PUMP_FREQ_Y, OIL_FLOW_X, OIL_FLOW_Y, FUEL_PRESSURE_BEFORE_X, FUEL_PRESSURE_BEFORE_Y, FUEL_TEMPERATURE_BEFORE_Y, \
    FUEL_MOISTURE_AFTER_Y, FUEL_MOISTURE_AFTER_X, FUEL_TEMPERATURE_AFTER_X, FUEL_TEMPERATURE_BEFORE_X, \
    FUEL_PRESSURE_AFTER_X, FUEL_PRESSURE_AFTER_Y, FUEL_MOISTURE_BEFORE_X, FUEL_TEMPERATURE_AFTER_Y, \
    FUEL_MOISTURE_BEFORE_Y, FUEL_TANK_TEMPERATURE_Y, FUEL_TANK_TEMPERATURE_X, FUEL_PUMP_FREQ_X, FUEL_PUMP_FREQ_Y, \
    FUEL_FLOW_Y, FUEL_FLOW_X
from core.widgets.ui_widgets.value_box import ValueBox


class ValueBoxSystem(QObject):
    def __init__(
            self,
            scene: QGraphicsScene
    ):
        super().__init__()
        self.scene = scene

        self.value_boxes = [
            (ValueBox(Tags.units.get(OilStand.pressure_before), 'Давление\nдо, Па'),
             (OIL_PRESSURE_BEFORE_X, OIL_PRESSURE_BEFORE_Y)),
            (ValueBox(Tags.units.get(OilStand.pressure_after), 'Давление\nпосле, Па'),
             (OIL_PRESSURE_AFTER_X, OIL_PRESSURE_AFTER_Y)),
            (ValueBox(Tags.units.get(OilStand.temperature_before), 'Темп\nдо, С'),
             (OIL_TEMPERATURE_BEFORE_X, OIL_TEMPERATURE_BEFORE_Y)),
            (ValueBox(Tags.units.get(OilStand.temperature_after), 'Темп\nпосле, С'),
             (OIL_TEMPERATURE_AFTER_X, OIL_TEMPERATURE_AFTER_Y)),
            (ValueBox(Tags.units.get(OilStand.moisture_before), 'Влаж.\n до, %'),
             (OIL_MOISTURE_BEFORE_X, OIL_MOISTURE_BEFORE_Y)),
            (ValueBox(Tags.units.get(OilStand.moisture_after), 'Влаж.\nпосле, %'),
             (OIL_MOISTURE_AFTER_X, OIL_MOISTURE_AFTER_Y)),
            (ValueBox(Tags.units.get(OilStand.tank_temperature), 'Темп., С'),
             (OIL_TANK_TEMPERATURE_X, OIL_TANK_TEMPERATURE_Y)),
            (ValueBox(Tags.units.get(OilStand.main_pump_frequency), 'Частота\nнасоса, Гц'),
             (OIL_PUMP_FREQ_X, OIL_PUMP_FREQ_Y)),
            (ValueBox(Tags.units.get(OilStand.flow_meter), 'Факт. рас-\nход, л3/ч'), (OIL_FLOW_X, OIL_FLOW_Y)),

            (ValueBox(Tags.units.get(FuelStand.pressure_before), 'Давление\nдо, Па'),
             (FUEL_PRESSURE_BEFORE_X, FUEL_PRESSURE_BEFORE_Y)),
            (ValueBox(Tags.units.get(FuelStand.pressure_after), 'Давление\nпосле, Па'),
             (FUEL_PRESSURE_AFTER_X, FUEL_PRESSURE_AFTER_Y)),
            (ValueBox(Tags.units.get(FuelStand.temperature_before), 'Темп\nдо, С'),
             (FUEL_TEMPERATURE_BEFORE_X, FUEL_TEMPERATURE_BEFORE_Y)),
            (ValueBox(Tags.units.get(FuelStand.temperature_after), 'Темп\nпосле, С'),
             (FUEL_TEMPERATURE_AFTER_X, FUEL_TEMPERATURE_AFTER_Y)),
            (ValueBox(Tags.units.get(FuelStand.moisture_before), 'Влаж.\n до, %'),
             (FUEL_MOISTURE_BEFORE_X, FUEL_MOISTURE_BEFORE_Y)),
            (ValueBox(Tags.units.get(FuelStand.moisture_after), 'Влаж.\nпосле, %'),
             (FUEL_MOISTURE_AFTER_X, FUEL_MOISTURE_AFTER_Y)),
            (ValueBox(Tags.units.get(FuelStand.tank_temperature), 'Темп., С'),
             (FUEL_TANK_TEMPERATURE_X, FUEL_TANK_TEMPERATURE_Y)),
            (ValueBox(Tags.units.get(FuelStand.main_pump_frequency), 'Частота\nнасоса, Гц'),
             (FUEL_PUMP_FREQ_X, FUEL_PUMP_FREQ_Y)),
            (ValueBox(Tags.units.get(FuelStand.flow_meter), 'Факт. рас-\nход, л3/ч'), (FUEL_FLOW_X, FUEL_FLOW_Y)),
        ]

        for vb in self.value_boxes:
            proxy = QGraphicsProxyWidget()
            proxy.setWidget(vb[0])
            self.scene.addItem(proxy)
            proxy.setPos(*vb[1])
