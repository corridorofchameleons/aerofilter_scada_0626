from PySide6.QtCore import QObject
from PySide6.QtWidgets import QGraphicsScene, QGraphicsProxyWidget

from app.instances.fuel_stand import FuelStand
from app.instances.oil_stand import OilStand
from app.ui.layouts.scheme_layout import OIL_PRESSURE_BEFORE_X, OIL_PRESSURE_BEFORE_Y, \
    OIL_TEMPERATURE_BEFORE_X, OIL_TEMPERATURE_AFTER_Y, OIL_PRESSURE_AFTER_Y, OIL_PRESSURE_AFTER_X, \
    OIL_TEMPERATURE_BEFORE_Y, OIL_TEMPERATURE_AFTER_X, OIL_MOISTURE_BEFORE_X, OIL_MOISTURE_AFTER_Y, \
    OIL_MOISTURE_BEFORE_Y, OIL_MOISTURE_AFTER_X, OIL_TANK_TEMPERATURE_X, OIL_TANK_TEMPERATURE_Y, \
    OIL_FLOW_X, OIL_FLOW_Y, FUEL_FLOW_X, FUEL_FLOW_Y, FUEL_PRESSURE_BEFORE_Y, FUEL_PRESSURE_BEFORE_X, \
    FUEL_PRESSURE_AFTER_X, FUEL_PRESSURE_AFTER_Y, FUEL_TEMPERATURE_BEFORE_Y, FUEL_TEMPERATURE_BEFORE_X, \
    FUEL_TEMPERATURE_AFTER_X, FUEL_TEMPERATURE_AFTER_Y, FUEL_MOISTURE_BEFORE_Y, FUEL_MOISTURE_BEFORE_X, \
    FUEL_MOISTURE_AFTER_X, FUEL_MOISTURE_AFTER_Y, FUEL_TANK_TEMPERATURE_Y, FUEL_TANK_TEMPERATURE_X
from core.widgets.ui_widgets.value_box import ValueBox


class ValueBoxSystem(QObject):
    def __init__(
            self,
            scene: QGraphicsScene
    ):
        super().__init__()
        self.scene = scene

        self.value_boxes = [
            (ValueBox(OilStand.oil_pressure_before, 'Давление\nдо, Па'),
             (OIL_PRESSURE_BEFORE_X, OIL_PRESSURE_BEFORE_Y)),
            (ValueBox(OilStand.oil_pressure_after, 'Давление\nпосле, Па'),
             (OIL_PRESSURE_AFTER_X, OIL_PRESSURE_AFTER_Y)),
            (ValueBox(OilStand.oil_temperature_before, 'Темп\nдо, С'),
             (OIL_TEMPERATURE_BEFORE_X, OIL_TEMPERATURE_BEFORE_Y)),
            (ValueBox(OilStand.oil_temperature_after, 'Темп\nпосле, С'),
             (OIL_TEMPERATURE_AFTER_X, OIL_TEMPERATURE_AFTER_Y)),
            (ValueBox(OilStand.oil_moisture_before, 'Влаж.\n до, %'),
             (OIL_MOISTURE_BEFORE_X, OIL_MOISTURE_BEFORE_Y)),
            (ValueBox(OilStand.oil_moisture_after, 'Влаж.\nпосле, %'),
             (OIL_MOISTURE_AFTER_X, OIL_MOISTURE_AFTER_Y)),
            (ValueBox(OilStand.oil_tank_temperature, 'Темп., С'),
             (OIL_TANK_TEMPERATURE_X, OIL_TANK_TEMPERATURE_Y)),
            (ValueBox(OilStand.oil_flow_meter, 'Факт. рас-\nход, л3/ч'),
             (OIL_FLOW_X, OIL_FLOW_Y)),

            (ValueBox(FuelStand.fuel_pressure_before, 'Давление\nдо, Па'),
             (FUEL_PRESSURE_BEFORE_X, FUEL_PRESSURE_BEFORE_Y)),
            (ValueBox(FuelStand.fuel_pressure_after, 'Давление\nпосле, Па'),
             (FUEL_PRESSURE_AFTER_X, FUEL_PRESSURE_AFTER_Y)),
            (ValueBox(FuelStand.fuel_temperature_before, 'Темп\nдо, С'),
             (FUEL_TEMPERATURE_BEFORE_X, FUEL_TEMPERATURE_BEFORE_Y)),
            (ValueBox(FuelStand.fuel_temperature_after, 'Темп\nпосле, С'),
             (FUEL_TEMPERATURE_AFTER_X, FUEL_TEMPERATURE_AFTER_Y)),
            (ValueBox(FuelStand.fuel_moisture_before, 'Влаж.\n до, %'),
             (FUEL_MOISTURE_BEFORE_X, FUEL_MOISTURE_BEFORE_Y)),
            (ValueBox(FuelStand.fuel_moisture_after, 'Влаж.\nпосле, %'),
             (FUEL_MOISTURE_AFTER_X, FUEL_MOISTURE_AFTER_Y)),
            (ValueBox(FuelStand.fuel_tank_temperature, 'Темп., С'),
             (FUEL_TANK_TEMPERATURE_X, FUEL_TANK_TEMPERATURE_Y)),
            (ValueBox(FuelStand.fuel_flow_meter, 'Факт. рас-\nход, л3/ч'), (FUEL_FLOW_X, FUEL_FLOW_Y)),
        ]

        for vb in self.value_boxes:
            proxy = QGraphicsProxyWidget()
            proxy.setWidget(vb[0])
            self.scene.addItem(proxy)
            proxy.setPos(*vb[1])
