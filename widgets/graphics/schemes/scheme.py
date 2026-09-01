from PySide6.QtCore import Qt, QObject, Signal, Slot
from PySide6.QtGui import QWheelEvent
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QWidget, QGraphicsProxyWidget

from models.stand import OilStand, FuelStand
from objects.tags import BinaryTags, Tags
from widgets.graphics.components.bounding_rect import BoundingRect
from widgets.graphics.components.filter import Filter
from widgets.graphics.components.particle_counter import ParticleCounter
from widgets.graphics.components.pipe import Pipe
from widgets.graphics.components.pump import Pump
from widgets.graphics.components.rotameter import Rotameter
from widgets.graphics.components.scheme_header import SchemeHeader
from widgets.graphics.components.tank import Tank
from widgets.graphics.components.valve import Valve
from widgets.graphics.layouts.scheme_layout import START_X, START_Y, WIDTH, HEIGHT, HEADER_OIL_X, HEADER_OIL_Y, \
    HEADER_FUEL_X, HEADER_FUEL_Y, OIL_RIGHT_TOP_KNEE_X, \
    OIL_RIGHT_TOP_KNEE_Y, OIL_LEFT_TOP_KNEE_X, OIL_LEFT_TOP_KNEE_Y, OIL_LEFT_BOTTOM_KNEE_X, OIL_LEFT_BOTTOM_KNEE_Y, \
    OIL_PUMP_X, OIL_RIGHT_BOTTOM_KNEE_Y, OIL_RIGHT_BOTTOM_KNEE_X, OIL_AFTER_FILTER_TOP_X, OIL_AFTER_FILTER_TOP_Y, \
    OIL_AFTER_FILTER_BOTTOM_X, OIL_AFTER_FILTER_BOTTOM_Y, OIL_BEFORE_FILTER_TOP_X, OIL_BEFORE_FILTER_TOP_Y, \
    OIL_BEFORE_FILTER_BOTTOM_X, OIL_BEFORE_FILTER_BOTTOM_Y, CENTER_X, FUEL_RIGHT_TOP_KNEE_X, FUEL_RIGHT_TOP_KNEE_Y, \
    FUEL_LEFT_TOP_KNEE_X, FUEL_LEFT_TOP_KNEE_Y, FUEL_LEFT_BOTTOM_KNEE_X, FUEL_LEFT_BOTTOM_KNEE_Y, FUEL_PUMP_X, \
    FUEL_RIGHT_BOTTOM_KNEE_Y, FUEL_RIGHT_BOTTOM_KNEE_X, FUEL_AFTER_FILTER_TOP_X, FUEL_AFTER_FILTER_TOP_Y, \
    FUEL_AFTER_FILTER_BOTTOM_X, FUEL_AFTER_FILTER_BOTTOM_Y, FUEL_BEFORE_FILTER_TOP_X, FUEL_BEFORE_FILTER_BOTTOM_Y, \
    FUEL_BEFORE_FILTER_TOP_Y, FUEL_BEFORE_FILTER_BOTTOM_X, COUNTER_START_X, COUNTER_START_Y, COUNTER_X, COUNTER_Y, \
    OIL_TANK_1_START_X, OIL_TANK_1_START_Y, OIL_TANK_1_END_X, OIL_TANK_1_END_Y, OIL_TANK_2_END_X, OIL_TANK_2_END_Y, \
    OIL_TANK_3_END_X, OIL_TANK_3_END_Y, OIL_SMALL_PUMP_X, OIL_SMALL_PUMP_Y, OIL_TANK_4_END_Y, OIL_TANK_4_END_X, \
    FUEL_TANK_3_END_Y, FUEL_TANK_4_END_X, FUEL_TANK_1_END_X, FUEL_TANK_4_END_Y, FUEL_SMALL_PUMP_X, FUEL_SMALL_PUMP_Y, \
    FUEL_TANK_2_END_X, FUEL_TANK_2_END_Y, FUEL_TANK_3_END_X, FUEL_TANK_1_START_X, FUEL_TANK_1_END_Y, \
    FUEL_TANK_1_START_Y, OIL_TANK_5_END_X, OIL_TANK_5_END_Y, FUEL_TANK_5_END_X, FUEL_TANK_5_END_Y, OIL_VALVE_V5_X, \
    OIL_VALVE_V5_Y, OIL_VALVE_V6_Y, OIL_VALVE_V6_X, OIL_VALVE_V2_X, OIL_VALVE_V2_Y, OIL_VALVE_V3_X, OIL_VALVE_V3_Y, \
    FUEL_VALVE_V2_Y, FUEL_VALVE_V2_X, FUEL_VALVE_V3_X, FUEL_VALVE_V5_X, FUEL_VALVE_V5_Y, FUEL_VALVE_V3_Y, \
    FUEL_VALVE_V6_Y, FUEL_VALVE_V6_X, OIL_PUMP_Y, FUEL_PUMP_Y, OIL_TANK_X, OIL_TANK_Y, FUEL_TANK_X, FUEL_TANK_Y, \
    OIL_SMALL_TANK_X, OIL_SMALL_TANK_Y, FUEL_SMALL_TANK_X, FUEL_SMALL_TANK_Y, OIL_FILTER_X, OIL_FILTER_Y, \
    OIL_FILTER_SMALL_X, OIL_FILTER_SMALL_Y, FUEL_FILTER_X, FUEL_FILTER_Y, FUEL_FILTER_SMALL_X, FUEL_FILTER_SMALL_Y, \
    OIL_ROTAMETER_X, OIL_ROTAMETER_Y, FUEL_ROTAMETER_X, FUEL_ROTAMETER_Y, OIL_PRESSURE_BEFORE_X, OIL_PRESSURE_BEFORE_Y, \
    OIL_TEMPERATURE_BEFORE_X, OIL_TEMPERATURE_AFTER_Y, OIL_PRESSURE_AFTER_Y, OIL_PRESSURE_AFTER_X, \
    OIL_TEMPERATURE_BEFORE_Y, OIL_TEMPERATURE_AFTER_X, OIL_MOISTURE_BEFORE_X, OIL_MOISTURE_AFTER_Y, \
    OIL_MOISTURE_BEFORE_Y, OIL_MOISTURE_AFTER_X, OIL_TANK_TEMPERATURE_X, OIL_TANK_TEMPERATURE_Y, OIL_PUMP_FREQ_X, \
    OIL_PUMP_FREQ_Y, OIL_FLOW_X, OIL_FLOW_Y, FUEL_PRESSURE_BEFORE_X, FUEL_PRESSURE_BEFORE_Y, FUEL_TEMPERATURE_BEFORE_Y, \
    FUEL_MOISTURE_AFTER_Y, FUEL_MOISTURE_AFTER_X, FUEL_TEMPERATURE_AFTER_X, FUEL_TEMPERATURE_BEFORE_X, \
    FUEL_PRESSURE_AFTER_X, FUEL_PRESSURE_AFTER_Y, FUEL_MOISTURE_BEFORE_X, FUEL_TEMPERATURE_AFTER_Y, \
    FUEL_MOISTURE_BEFORE_Y, FUEL_TANK_TEMPERATURE_Y, FUEL_TANK_TEMPERATURE_X, FUEL_PUMP_FREQ_X, FUEL_PUMP_FREQ_Y, \
    FUEL_FLOW_Y, FUEL_FLOW_X
from widgets.settings import Settings
from widgets.ui_widgets.value_box import ValueBox


class _BorderRectangles(QWidget):
    def __init__(
            self,
            scene: QGraphicsScene
    ):
        super().__init__()
        self.scene = scene

        self.oil_border = BoundingRect(position=1)
        self.fuel_border = BoundingRect(position=2)
        self.scene.addItem(self.oil_border)
        self.scene.addItem(self.fuel_border)


class _SchemeHeaders(QWidget):
    def __init__(
            self,
            scene: QGraphicsScene
    ):
        super().__init__()
        self.scene = scene

        self.oil_header = SchemeHeader(title='Масляный стенд')
        self.oil_header_proxy = QGraphicsProxyWidget()
        self.oil_header_proxy.setWidget(self.oil_header)
        self.oil_header_proxy.setPos(HEADER_OIL_X, HEADER_OIL_Y)
        self.scene.addItem(self.oil_header_proxy)

        self.fuel_header = SchemeHeader(title='Топливный стенд')
        self.fuel_header_proxy = QGraphicsProxyWidget()
        self.fuel_header_proxy.setWidget(self.fuel_header)
        self.fuel_header_proxy.setPos(HEADER_FUEL_X, HEADER_FUEL_Y)
        self.scene.addItem(self.fuel_header_proxy)


class _PipeSystem(QObject):
    def __init__(
            self,
            scene: QGraphicsScene,
            set_active_contours,
            activate_flow
    ):
        super().__init__()
        self.scene = scene

        self.set_active_contours = set_active_contours

        self.pipes = [
            # масляный стенд

            # внешний контур
            Pipe(OIL_RIGHT_TOP_KNEE_X, OIL_RIGHT_TOP_KNEE_Y, OIL_LEFT_TOP_KNEE_X, OIL_LEFT_TOP_KNEE_Y, horizontal=True,
                 start_joint='left', end_joint='left', contour=(1,), arrow_rotation=180, activate_flow=activate_flow),
            Pipe(OIL_LEFT_TOP_KNEE_X, OIL_LEFT_TOP_KNEE_Y, OIL_LEFT_BOTTOM_KNEE_X, OIL_LEFT_BOTTOM_KNEE_Y,
                 horizontal=False, start_joint='left', end_joint='left', contour=(1,), arrow_rotation=90,
                 activate_flow=activate_flow),
            Pipe(OIL_LEFT_BOTTOM_KNEE_X, OIL_LEFT_BOTTOM_KNEE_Y, OIL_PUMP_X, OIL_LEFT_BOTTOM_KNEE_Y, horizontal=True,
                 start_joint='left', contour=(1,), arrow_num=3, activate_flow=activate_flow),
            Pipe(OIL_PUMP_X, OIL_RIGHT_BOTTOM_KNEE_Y, OIL_RIGHT_BOTTOM_KNEE_X, OIL_RIGHT_BOTTOM_KNEE_Y, horizontal=True,
                 end_joint='left', contour=(1,), arrow_num=1, activate_flow=activate_flow),
            Pipe(OIL_RIGHT_BOTTOM_KNEE_X, OIL_RIGHT_BOTTOM_KNEE_Y, OIL_RIGHT_TOP_KNEE_X, OIL_RIGHT_TOP_KNEE_Y,
                 horizontal=False, start_joint='left', end_joint='left', contour=(1,), arrow_rotation=270,
                 activate_flow=activate_flow),

            # тонкие трубы верх
            Pipe(OIL_AFTER_FILTER_TOP_X, OIL_AFTER_FILTER_TOP_Y, OIL_AFTER_FILTER_BOTTOM_X, OIL_AFTER_FILTER_BOTTOM_Y,
                 horizontal=False, start_joint='sharp', end_joint='left', thin=True, contour=(2,), arrow_rotation=90,
                 activate_flow=activate_flow),
            Pipe(OIL_AFTER_FILTER_BOTTOM_X, OIL_AFTER_FILTER_BOTTOM_Y, OIL_BEFORE_FILTER_TOP_X,
                 OIL_BEFORE_FILTER_BOTTOM_Y,
                 horizontal=True, start_joint='left', thin=True, contour=(2,), arrow_num=3,
                 activate_flow=activate_flow),
            Pipe(OIL_BEFORE_FILTER_TOP_X, OIL_BEFORE_FILTER_BOTTOM_Y, CENTER_X - Settings.PUMP_THIN_LINE_WIDTH / 2,
                 OIL_BEFORE_FILTER_BOTTOM_Y,
                 horizontal=True, start_joint='left', thin=True, contour=(2, 3), arrow_num=1,
                 activate_flow=activate_flow),
            Pipe(OIL_BEFORE_FILTER_TOP_X, OIL_BEFORE_FILTER_TOP_Y, OIL_BEFORE_FILTER_BOTTOM_X,
                 OIL_BEFORE_FILTER_BOTTOM_Y,
                 horizontal=False, start_joint='sharp', end_joint='sharp', thin=True, contour=(3,), arrow_rotation=90,
                 activate_flow=activate_flow),

            # тонкие трубы бок
            Pipe(OIL_TANK_1_START_X, OIL_TANK_1_START_Y, OIL_TANK_1_END_X,
                 OIL_TANK_1_END_Y,
                 horizontal=True, start_joint='sharp', end_joint='right', thin=True, contour=(5,), arrow_num=3,
                 activate_flow=activate_flow),
            Pipe(OIL_TANK_1_END_X, OIL_TANK_1_END_Y, OIL_TANK_3_END_X,
                 OIL_TANK_3_END_Y,
                 horizontal=False, start_joint='right', thin=True, contour=(5,), arrow_num=0,
                 activate_flow=activate_flow),
            Pipe(OIL_TANK_4_END_X, OIL_TANK_4_END_Y, OIL_TANK_5_END_X,
                 OIL_TANK_5_END_Y,
                 horizontal=False, end_joint='sharp', thin=True, contour=(6,), arrow_rotation=90, arrow_num=1,
                 activate_flow=activate_flow),

            Pipe(OIL_TANK_3_END_X, OIL_TANK_3_END_Y, OIL_TANK_2_END_X,
                 OIL_TANK_2_END_Y,
                 horizontal=False, start_joint='right', thin=True, contour=(4,), arrow_num=0,
                 activate_flow=activate_flow),
            Pipe(OIL_TANK_2_END_X, OIL_TANK_2_END_Y, OIL_SMALL_PUMP_X,
                 OIL_TANK_2_END_Y,
                 horizontal=True, start_joint='left', thin=True, contour=(4,), arrow_num=2,
                 activate_flow=activate_flow),
            Pipe(OIL_SMALL_PUMP_X, OIL_SMALL_PUMP_Y, OIL_TANK_4_END_X,
                 OIL_TANK_4_END_Y,
                 horizontal=True, end_joint='sharp', thin=True, contour=(4,), arrow_num=1, activate_flow=activate_flow),
            Pipe(OIL_TANK_4_END_X, OIL_TANK_4_END_Y, OIL_TANK_4_END_X,
                 OIL_TANK_3_END_Y,
                 horizontal=False, start_joint='left', end_joint='left', thin=True, contour=(4,), arrow_rotation=270,
                 activate_flow=activate_flow),
            Pipe(OIL_TANK_4_END_X, OIL_TANK_3_END_Y, OIL_TANK_1_END_X,
                 OIL_TANK_3_END_Y,
                 horizontal=True, start_joint='left', end_joint='sharp', thin=True, contour=(4,), arrow_num=1,
                 arrow_rotation=180, activate_flow=activate_flow),

            # топливный стенд

            # внешний контур
            Pipe(FUEL_RIGHT_TOP_KNEE_X, FUEL_RIGHT_TOP_KNEE_Y, FUEL_LEFT_TOP_KNEE_X, FUEL_LEFT_TOP_KNEE_Y,
                 horizontal=True,
                 start_joint='left', end_joint='left', contour=(7,), arrow_rotation=180, activate_flow=activate_flow),
            Pipe(FUEL_LEFT_TOP_KNEE_X, FUEL_LEFT_TOP_KNEE_Y, FUEL_LEFT_BOTTOM_KNEE_X, FUEL_LEFT_BOTTOM_KNEE_Y,
                 horizontal=False, start_joint='left', end_joint='left', contour=(7,), arrow_rotation=90,
                 activate_flow=activate_flow),
            Pipe(FUEL_LEFT_BOTTOM_KNEE_X, FUEL_LEFT_BOTTOM_KNEE_Y, FUEL_PUMP_X, FUEL_LEFT_BOTTOM_KNEE_Y,
                 horizontal=True, start_joint='left', contour=(7,), arrow_num=3, activate_flow=activate_flow),
            Pipe(FUEL_PUMP_X, FUEL_RIGHT_BOTTOM_KNEE_Y, FUEL_RIGHT_BOTTOM_KNEE_X, FUEL_RIGHT_BOTTOM_KNEE_Y,
                 horizontal=True, end_joint='left', contour=(7,), arrow_num=1, activate_flow=activate_flow),
            Pipe(FUEL_RIGHT_BOTTOM_KNEE_X, FUEL_RIGHT_BOTTOM_KNEE_Y, FUEL_RIGHT_TOP_KNEE_X, FUEL_RIGHT_TOP_KNEE_Y,
                 horizontal=False, start_joint='left', end_joint='left', contour=(7,), arrow_rotation=270,
                 activate_flow=activate_flow),

            # тонкие трубы верх
            Pipe(FUEL_BEFORE_FILTER_BOTTOM_X, FUEL_BEFORE_FILTER_BOTTOM_Y, FUEL_AFTER_FILTER_TOP_X,
                 FUEL_AFTER_FILTER_BOTTOM_Y,
                 horizontal=True, start_joint='right', thin=True, contour=(8,), arrow_num=3, arrow_rotation=180,
                 activate_flow=activate_flow),
            Pipe(FUEL_BEFORE_FILTER_TOP_X, FUEL_BEFORE_FILTER_TOP_Y, FUEL_BEFORE_FILTER_BOTTOM_X,
                 FUEL_BEFORE_FILTER_BOTTOM_Y,
                 horizontal=False, start_joint='sharp', end_joint='right', thin=True, contour=(8,), arrow_rotation=90,
                 activate_flow=activate_flow),
            Pipe(FUEL_AFTER_FILTER_TOP_X, FUEL_AFTER_FILTER_BOTTOM_Y, CENTER_X + Settings.PUMP_THIN_LINE_WIDTH / 2,
                 FUEL_AFTER_FILTER_BOTTOM_Y,
                 horizontal=True, start_joint='right', thin=True, contour=(8, 9), arrow_num=1, arrow_rotation=180,
                 activate_flow=activate_flow),
            Pipe(FUEL_AFTER_FILTER_TOP_X, FUEL_AFTER_FILTER_TOP_Y, FUEL_AFTER_FILTER_BOTTOM_X,
                 OIL_AFTER_FILTER_BOTTOM_Y,
                 horizontal=False, start_joint='sharp', end_joint='sharp', thin=True, contour=(9,), arrow_rotation=90,
                 activate_flow=activate_flow),

            # тонкие трубы бок
            Pipe(FUEL_TANK_1_START_X, FUEL_TANK_1_START_Y, FUEL_TANK_1_END_X,
                 FUEL_TANK_1_END_Y,
                 horizontal=True, start_joint='sharp', end_joint='right', thin=True, contour=(11,), arrow_num=3,
                 activate_flow=activate_flow),
            Pipe(FUEL_TANK_1_END_X, FUEL_TANK_1_END_Y, FUEL_TANK_3_END_X,
                 FUEL_TANK_3_END_Y,
                 horizontal=False, start_joint='right', thin=True, contour=(11,), arrow_num=0,
                 activate_flow=activate_flow),
            Pipe(FUEL_TANK_4_END_X, FUEL_TANK_4_END_Y, FUEL_TANK_5_END_X,
                 FUEL_TANK_5_END_Y,
                 horizontal=False, end_joint='sharp', thin=True, contour=(12,), arrow_rotation=90, arrow_num=1,
                 activate_flow=activate_flow),

            Pipe(FUEL_TANK_3_END_X, FUEL_TANK_3_END_Y, FUEL_TANK_2_END_X,
                 FUEL_TANK_2_END_Y,
                 horizontal=False, start_joint='right', thin=True, contour=(10,), arrow_num=0,
                 activate_flow=activate_flow),
            Pipe(FUEL_TANK_2_END_X, FUEL_TANK_2_END_Y, FUEL_SMALL_PUMP_X,
                 FUEL_TANK_2_END_Y,
                 horizontal=True, start_joint='left', thin=True, contour=(10,), arrow_num=2,
                 activate_flow=activate_flow),
            Pipe(FUEL_SMALL_PUMP_X, FUEL_SMALL_PUMP_Y, FUEL_TANK_4_END_X,
                 FUEL_TANK_4_END_Y,
                 horizontal=True, end_joint='sharp', thin=True, contour=(10,), arrow_num=1,
                 activate_flow=activate_flow),
            Pipe(FUEL_TANK_4_END_X, FUEL_TANK_4_END_Y, FUEL_TANK_4_END_X,
                 FUEL_TANK_3_END_Y,
                 horizontal=False, start_joint='left', end_joint='left', thin=True, contour=(10,), arrow_rotation=270,
                 activate_flow=activate_flow),
            Pipe(FUEL_TANK_4_END_X, FUEL_TANK_3_END_Y, FUEL_TANK_1_END_X,
                 FUEL_TANK_3_END_Y,
                 horizontal=True, start_joint='left', end_joint='sharp', thin=True, contour=(10,), arrow_num=1,
                 arrow_rotation=180, activate_flow=activate_flow),

            # счетчик частиц
            Pipe(COUNTER_START_X, COUNTER_START_Y, COUNTER_X, COUNTER_Y,
                 horizontal=False, start_joint='sharp', thin=True, contour=(2, 3, 8, 9), arrow_num=0,
                 activate_flow=activate_flow),
        ]

        for pipe in self.pipes:
            self.set_active_contours.connect(pipe.handle_contour_change)
            self.scene.addItem(pipe)


class _ValveSystem(QObject):
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
            (Valve(small=True, contour=(2,), tag=BinaryTags.units.get(OilStand.counter_after_valve),
                   signal=handle_status_signal), (OIL_VALVE_V2_X, OIL_VALVE_V2_Y)),
            (Valve(small=True, contour=(3,), tag=BinaryTags.units.get(OilStand.counter_before_valve),
                   signal=handle_status_signal), (OIL_VALVE_V3_X, OIL_VALVE_V3_Y)),
            (Valve(small=True, contour=(5,), rotation_angle=90, tag=BinaryTags.units.get(OilStand.mixer_input_valve),
                   signal=handle_status_signal), (OIL_VALVE_V5_X, OIL_VALVE_V5_Y)),
            (Valve(small=True, contour=(6,), tag=BinaryTags.units.get(OilStand.mixer_output_valve),
                   signal=handle_status_signal), (OIL_VALVE_V6_X, OIL_VALVE_V6_Y)),
            (Valve(small=True, contour=(8,), tag=BinaryTags.units.get(FuelStand.counter_after_valve),
                   signal=handle_status_signal), (FUEL_VALVE_V2_X, FUEL_VALVE_V2_Y)),
            (Valve(small=True, contour=(9,), tag=BinaryTags.units.get(FuelStand.counter_before_valve),
                   signal=handle_status_signal), (FUEL_VALVE_V3_X, FUEL_VALVE_V3_Y)),
            (Valve(small=True, contour=(11,), rotation_angle=90, tag=BinaryTags.units.get(FuelStand.mixer_input_valve),
                   signal=handle_status_signal), (FUEL_VALVE_V5_X, FUEL_VALVE_V5_Y)),
            (Valve(small=True, contour=(12,), tag=BinaryTags.units.get(FuelStand.mixer_output_valve),
                   signal=handle_status_signal), (FUEL_VALVE_V6_X, FUEL_VALVE_V6_Y)),
        ]

        for item in self.valves:
            self.scene.addItem(item[0])
            self.set_active_contours.connect(item[0].handle_contour_change)
            item[0].setPos(*item[1])


class _PumpSystem(QObject):
    def __init__(
            self,
            scene: QGraphicsScene,
            flow_signal,
    ):
        super().__init__()
        self.scene = scene

        self.oil_pump_1 = Pump((1, 2, 3, 5), BinaryTags.units.get(OilStand.main_pump), flow_signal)
        self.scene.addItem(self.oil_pump_1)
        self.oil_pump_1.setPos(OIL_PUMP_X, OIL_PUMP_Y)

        self.oil_pump_2 = Pump((4, 6), BinaryTags.units.get(OilStand.mixing_pump), flow_signal, small=True)
        self.scene.addItem(self.oil_pump_2)
        self.oil_pump_2.setPos(OIL_SMALL_PUMP_X, OIL_SMALL_PUMP_Y)

        self.fuel_pump_1 = Pump((7, 8, 9, 11), BinaryTags.units.get(FuelStand.main_pump), flow_signal)
        self.scene.addItem(self.fuel_pump_1)
        self.fuel_pump_1.setPos(FUEL_PUMP_X, FUEL_PUMP_Y)

        self.fuel_pump_2 = Pump((10, 12), BinaryTags.units.get(FuelStand.mixing_pump), flow_signal, small=True)
        self.scene.addItem(self.fuel_pump_2)
        self.fuel_pump_2.setPos(FUEL_SMALL_PUMP_X, FUEL_SMALL_PUMP_Y)


class _TankSystem(QObject):
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


class _ValueBoxSystem(QObject):
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


class _FilterSystem(QObject):
    def __init__(
            self,
            scene: QGraphicsScene,
    ):
        super().__init__()
        self.scene = scene

        self.oil_filter = Filter()
        self.scene.addItem(self.oil_filter)
        self.oil_filter.setPos(OIL_FILTER_X, OIL_FILTER_Y)

        self.oil_filter_small = Filter(small=True, rotation=270)
        self.scene.addItem(self.oil_filter_small)
        self.oil_filter_small.setPos(OIL_FILTER_SMALL_X, OIL_FILTER_SMALL_Y)

        self.fuel_filter = Filter()
        self.scene.addItem(self.fuel_filter)
        self.fuel_filter.setPos(FUEL_FILTER_X, FUEL_FILTER_Y)

        self.fuel_filter_small = Filter(small=True, rotation=270)
        self.scene.addItem(self.fuel_filter_small)
        self.fuel_filter_small.setPos(FUEL_FILTER_SMALL_X, FUEL_FILTER_SMALL_Y)


class _RotameterSystem(QObject):
    def __init__(
            self,
            scene: QGraphicsScene
    ):
        super().__init__()
        self.scene = scene

        self.oil_rotameter = Rotameter()
        self.oil_rotameter.setPos(OIL_ROTAMETER_X, OIL_ROTAMETER_Y)
        self.scene.addItem(self.oil_rotameter)

        self.fuel_rotameter = Rotameter()
        self.fuel_rotameter.setPos(FUEL_ROTAMETER_X, FUEL_ROTAMETER_Y)
        self.scene.addItem(self.fuel_rotameter)


class Scheme(QGraphicsView):
    set_active_contours = Signal(set)
    handle_contour_status = Signal(int, bool)

    switch_flow_signal = Signal(set, bool)
    activate_flow = Signal(set, bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setObjectName('scheme')

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # Отключаем горизонтальный скролл
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setDragMode(QGraphicsView.NoDrag)

        self.scene = QGraphicsScene()
        self.scene.setSceneRect(START_X, START_Y, WIDTH, HEIGHT)
        self.setScene(self.scene)

        self.scheme_borders = _BorderRectangles(self.scene)
        self.scheme_headers = _SchemeHeaders(self.scene)

        self.handle_contour_status.connect(self.change_contour_status)

        self.active_contours = {1, 4, 7, 10}
        self.flow_1_active = False
        self.flow_2_active = False

        self.pipe_system = _PipeSystem(self.scene, self.set_active_contours, self.activate_flow)
        self.valve_system = _ValveSystem(
            self.scene,
            self.set_active_contours,
            handle_status_signal=self.handle_contour_status
        )

        self.pump_system = _PumpSystem(self.scene, self.switch_flow_signal)
        self.tank_system = _TankSystem(self.scene)
        self.filter_system = _FilterSystem(self.scene)
        self.rotameter_system = _RotameterSystem(self.scene)
        self.value_boxes = _ValueBoxSystem(self.scene)

        self.particle_counter = ParticleCounter()
        self.particle_counter.setPos(COUNTER_X, COUNTER_Y)
        self.scene.addItem(self.particle_counter)

        self.switch_flow_signal.connect(self.repaint_flow)

        self.set_active_contours.emit(self.active_contours)

    def wheelEvent(self, event: QWheelEvent):
        pass

    @Slot(set, bool)
    def repaint_flow(self, contours: set, status: bool):
        self.activate_flow.emit(contours, status)

    @Slot(int, bool)
    def change_contour_status(self, contour: int, val: bool):
        if val:
            self.add_active_contour(contour)
        else:
            self.remove_active_contour(contour)

    def add_active_contour(self, contour: int):
        self.active_contours.add(contour)
        self.set_active_contours.emit(self.active_contours)

    def remove_active_contour(self, contour: int):
        self.active_contours.remove(contour)
        self.set_active_contours.emit(self.active_contours)
