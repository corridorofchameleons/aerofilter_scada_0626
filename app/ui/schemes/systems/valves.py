from PySide6.QtCore import QObject
from PySide6.QtWidgets import QGraphicsScene, QGraphicsProxyWidget

from app.instances.fuel_stand import FuelStand
from app.instances.oil_stand import OilStand
from app.ui.layouts.scheme_layout import OIL_VALVE_V5_X, \
    OIL_VALVE_V5_Y, OIL_VALVE_V6_Y, OIL_VALVE_V6_X, OIL_VALVE_V2_X, OIL_VALVE_V2_Y, OIL_VALVE_V3_X, OIL_VALVE_V3_Y, \
    FUEL_VALVE_V6_Y, FUEL_VALVE_V6_X, FUEL_VALVE_V5_Y, FUEL_VALVE_V5_X, FUEL_VALVE_V3_Y, FUEL_VALVE_V3_X, \
    FUEL_VALVE_V2_Y, FUEL_VALVE_V2_X
from core.settings import Settings
from core.widgets.graphics.components.valve import Valve


class ValveSystem(QObject):
    def __init__(
            self,
            scene: QGraphicsScene,
            set_active_contours,
            handle_status_signal,
    ):
        super().__init__()
        self.scene = scene

        self.set_active_contours = set_active_contours

        self.valves = [
            (Valve(
                small=True,
                contour=(2,),
                tag=OilStand.oil_probe_before_6ka4,
                signal=handle_status_signal
            ),
                   (OIL_VALVE_V2_X, OIL_VALVE_V2_Y)),
            (Valve(
                small=True,
                contour=(3,),
                tag=OilStand.oil_probe_after_6ka3,
                signal=handle_status_signal
            ),
                   (OIL_VALVE_V3_X, OIL_VALVE_V3_Y)),
            (Valve(
                small=True,
                contour=(5,), rotation_angle=90,
                tag=OilStand.oil_mixer_input_valve,
                signal=handle_status_signal
            ),
                   (OIL_VALVE_V5_X, OIL_VALVE_V5_Y)),
            (Valve(
                small=True,
                contour=(6,),
                tag=OilStand.oil_mixer_output_valve,
                signal=handle_status_signal
            ),
                   (OIL_VALVE_V6_X, OIL_VALVE_V6_Y)),

            (Valve(
                small=True,
                contour=(9,),
                tag=FuelStand.fuel_probe_before_6ka4,
                signal=handle_status_signal
            ),
             (FUEL_VALVE_V2_X, FUEL_VALVE_V2_Y)),
            (Valve(
                small=True,
                contour=(8,),
                tag=FuelStand.fuel_probe_after_6ka3,
                signal=handle_status_signal
            ),
             (FUEL_VALVE_V3_X, FUEL_VALVE_V3_Y)),
            (Valve(
                small=True,
                contour=(11,), rotation_angle=90,
                tag=FuelStand.fuel_mixer_input_valve,
                signal=handle_status_signal
            ),
             (FUEL_VALVE_V5_X, FUEL_VALVE_V5_Y)),
            (Valve(
                small=True,
                contour=(12,),
                tag=FuelStand.fuel_mixer_output_valve,
                signal=handle_status_signal
            ),
             (FUEL_VALVE_V6_X, FUEL_VALVE_V6_Y)),
        ]

        for item in self.valves:
            self.scene.addItem(item[0])
            item[0].setPos(*item[1])

            proxy_error = QGraphicsProxyWidget()
            proxy_error.setZValue(6)
            proxy_error.setWidget(item[0].error_widget)
            self.scene.addItem(proxy_error)
            proxy_error.setPos(item[1][0] - Settings.ERROR_WIDGET_WIDTH * 0.5,
                               item[1][1] - Settings.ERROR_WIDGET_HEIGHT * 1.5)
