import time

from PySide6.QtCore import Qt, QRectF, QObject, Signal, QPointF, Slot
from PySide6.QtGui import QPen, QColor, QWheelEvent, QPainter
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsItem, QWidget, QGraphicsProxyWidget

from models.device import Device
from objects.tags import BinaryTags
from widgets.graphics.components.bounding_rect import BoundingRect
from widgets.graphics.components.pipe import Pipe
from widgets.graphics.components.scheme_header import SchemeHeader
from widgets.graphics.components.valve import Valve
from widgets.graphics.layouts.fuel_layout import VALVE_V6_X
from widgets.graphics.layouts.scheme_layout import STAND_BORDER_HEIGHT, STAND_BORDER_WIDTH, START_OIL_X, START_OIL_Y, \
    START_X, START_Y, WIDTH, HEIGHT, HEADER_OIL_X, HEADER_OIL_Y, HEADER_FUEL_X, HEADER_FUEL_Y, OIL_RIGHT_TOP_KNEE_X, \
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
    FUEL_VALVE_V6_Y, FUEL_VALVE_V6_X
from widgets.settings import Settings


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

        self.oil_header = SchemeHeader(position=Device.PLC1)
        self.oil_header_proxy = QGraphicsProxyWidget()
        self.oil_header_proxy.setWidget(self.oil_header)
        self.oil_header_proxy.setPos(HEADER_OIL_X, HEADER_OIL_Y)
        self.scene.addItem(self.oil_header_proxy)

        self.fuel_header = SchemeHeader(position=Device.PLC2)
        self.fuel_header_proxy = QGraphicsProxyWidget()
        self.fuel_header_proxy.setWidget(self.fuel_header)
        self.fuel_header_proxy.setPos(HEADER_FUEL_X, HEADER_FUEL_Y)
        self.scene.addItem(self.fuel_header_proxy)

class _PipeSystem(QObject):
    def __init__(
            self,
            scene: QGraphicsScene,
            set_active_contours,
    ):
        super().__init__()
        self.scene = scene

        self.set_active_contours = set_active_contours

        self.pipes = [
            # масляный стенд

            # внешний контур
            Pipe((Device.PLC1,), OIL_RIGHT_TOP_KNEE_X, OIL_RIGHT_TOP_KNEE_Y, OIL_LEFT_TOP_KNEE_X, OIL_LEFT_TOP_KNEE_Y, horizontal=True,
                 start_joint='left', end_joint='left', contour=(1,), arrow_rotation=180),
            Pipe((Device.PLC1,), OIL_LEFT_TOP_KNEE_X, OIL_LEFT_TOP_KNEE_Y, OIL_LEFT_BOTTOM_KNEE_X, OIL_LEFT_BOTTOM_KNEE_Y,
                 horizontal=False, start_joint='left', end_joint='left', contour=(1,), arrow_rotation=90),
            Pipe((Device.PLC1,), OIL_LEFT_BOTTOM_KNEE_X, OIL_LEFT_BOTTOM_KNEE_Y, OIL_PUMP_X, OIL_LEFT_BOTTOM_KNEE_Y,
                 horizontal=True, start_joint='left', contour=(1,), arrow_num=3),
            Pipe((Device.PLC1,), OIL_PUMP_X, OIL_RIGHT_BOTTOM_KNEE_Y, OIL_RIGHT_BOTTOM_KNEE_X, OIL_RIGHT_BOTTOM_KNEE_Y,
                 horizontal=True, end_joint='left', contour=(1,), arrow_num=1),
            Pipe((Device.PLC1,), OIL_RIGHT_BOTTOM_KNEE_X, OIL_RIGHT_BOTTOM_KNEE_Y, OIL_RIGHT_TOP_KNEE_X, OIL_RIGHT_TOP_KNEE_Y,
                 horizontal=False, start_joint='left', end_joint='left', contour=(1,), arrow_rotation=270),

            # тонкие трубы верх
            Pipe((Device.PLC1,), OIL_AFTER_FILTER_TOP_X, OIL_AFTER_FILTER_TOP_Y, OIL_AFTER_FILTER_BOTTOM_X, OIL_AFTER_FILTER_BOTTOM_Y,
                 horizontal=False, start_joint='sharp', end_joint='left', thin=True, contour=(2,), arrow_rotation=90),
            Pipe((Device.PLC1,), OIL_AFTER_FILTER_BOTTOM_X, OIL_AFTER_FILTER_BOTTOM_Y, OIL_BEFORE_FILTER_TOP_X,
                 OIL_BEFORE_FILTER_BOTTOM_Y,
                 horizontal=True, start_joint='left', thin=True, contour=(2,), arrow_num=3),
            Pipe((Device.PLC1,), OIL_BEFORE_FILTER_TOP_X, OIL_BEFORE_FILTER_BOTTOM_Y, CENTER_X - Settings.PUMP_THIN_LINE_WIDTH / 2,
                 OIL_BEFORE_FILTER_BOTTOM_Y,
                 horizontal=True, start_joint='left', thin=True, contour=(2, 3), arrow_num=1),
            Pipe((Device.PLC1,), OIL_BEFORE_FILTER_TOP_X, OIL_BEFORE_FILTER_TOP_Y, OIL_BEFORE_FILTER_BOTTOM_X,
                 OIL_BEFORE_FILTER_BOTTOM_Y,
                 horizontal=False, start_joint='sharp', end_joint='sharp', thin=True, contour=(3,), arrow_rotation=90),

            # тонкие трубы бок
            Pipe((Device.PLC1,), OIL_TANK_1_START_X, OIL_TANK_1_START_Y, OIL_TANK_1_END_X,
                 OIL_TANK_1_END_Y,
                 horizontal=True, start_joint='sharp', end_joint='right', thin=True, contour=(5,), arrow_num=3),
            Pipe((Device.PLC1,), OIL_TANK_1_END_X, OIL_TANK_1_END_Y, OIL_TANK_3_END_X,
                 OIL_TANK_3_END_Y,
                 horizontal=False, start_joint='right', thin=True, contour=(5,), arrow_num=0),
            Pipe((Device.PLC1,), OIL_TANK_4_END_X, OIL_TANK_4_END_Y, OIL_TANK_5_END_X,
                 OIL_TANK_5_END_Y,
                 horizontal=False, end_joint='sharp', thin=True, contour=(6,), arrow_rotation=90),

            Pipe((Device.PLC1,), OIL_TANK_3_END_X, OIL_TANK_3_END_Y, OIL_TANK_2_END_X,
                 OIL_TANK_2_END_Y,
                 horizontal=False, start_joint='right', thin=True, contour=(4,), arrow_num=0),
            Pipe((Device.PLC1,), OIL_TANK_2_END_X, OIL_TANK_2_END_Y, OIL_SMALL_PUMP_X,
                 OIL_TANK_2_END_Y,
                 horizontal=True, start_joint='left', thin=True, contour=(4,), arrow_num=2),
            Pipe((Device.PLC1,), OIL_SMALL_PUMP_X, OIL_SMALL_PUMP_Y, OIL_TANK_4_END_X,
                 OIL_TANK_4_END_Y,
                 horizontal=True, end_joint='sharp', thin=True, contour=(4,), arrow_num=1),
            Pipe((Device.PLC1,), OIL_TANK_4_END_X, OIL_TANK_4_END_Y, OIL_TANK_4_END_X,
                 OIL_TANK_3_END_Y,
                 horizontal=False, start_joint='left', end_joint='left', thin=True, contour=(4,), arrow_rotation=270),
            Pipe((Device.PLC1,), OIL_TANK_4_END_X, OIL_TANK_3_END_Y, OIL_TANK_1_END_X,
                 OIL_TANK_3_END_Y,
                 horizontal=True, start_joint='left', end_joint='sharp', thin=True, contour=(4,), arrow_num = 1,
                 arrow_rotation=180),

            # топливный стенд

            # внешний контур
            Pipe((Device.PLC2,), FUEL_RIGHT_TOP_KNEE_X, FUEL_RIGHT_TOP_KNEE_Y, FUEL_LEFT_TOP_KNEE_X, FUEL_LEFT_TOP_KNEE_Y,
                 horizontal=True,
                 start_joint='left', end_joint='left', contour=(7,), arrow_rotation=180),
            Pipe((Device.PLC2,), FUEL_LEFT_TOP_KNEE_X, FUEL_LEFT_TOP_KNEE_Y, FUEL_LEFT_BOTTOM_KNEE_X, FUEL_LEFT_BOTTOM_KNEE_Y,
                 horizontal=False, start_joint='left', end_joint='left', contour=(7,), arrow_rotation=90),
            Pipe((Device.PLC2,), FUEL_LEFT_BOTTOM_KNEE_X, FUEL_LEFT_BOTTOM_KNEE_Y, FUEL_PUMP_X, FUEL_LEFT_BOTTOM_KNEE_Y,
                 horizontal=True, start_joint='left', contour=(7,), arrow_num=3),
            Pipe((Device.PLC2,), FUEL_PUMP_X, FUEL_RIGHT_BOTTOM_KNEE_Y, FUEL_RIGHT_BOTTOM_KNEE_X, FUEL_RIGHT_BOTTOM_KNEE_Y,
                 horizontal=True, end_joint='left', contour=(7,), arrow_num=1),
            Pipe((Device.PLC2,), FUEL_RIGHT_BOTTOM_KNEE_X, FUEL_RIGHT_BOTTOM_KNEE_Y, FUEL_RIGHT_TOP_KNEE_X, FUEL_RIGHT_TOP_KNEE_Y,
                 horizontal=False, start_joint='left', end_joint='left', contour=(7,), arrow_rotation=270),

            # тонкие трубы верх
            Pipe((Device.PLC2,), FUEL_BEFORE_FILTER_BOTTOM_X, FUEL_BEFORE_FILTER_BOTTOM_Y, FUEL_AFTER_FILTER_TOP_X,
                 FUEL_AFTER_FILTER_BOTTOM_Y,
                 horizontal=True, start_joint='right', thin=True, contour=(8,), arrow_num=3, arrow_rotation=180),
            Pipe((Device.PLC2,), FUEL_BEFORE_FILTER_TOP_X, FUEL_BEFORE_FILTER_TOP_Y, FUEL_BEFORE_FILTER_BOTTOM_X,
                 FUEL_BEFORE_FILTER_BOTTOM_Y,
                 horizontal=False, start_joint='sharp', end_joint='right', thin=True, contour=(8,), arrow_rotation=90),
            Pipe((Device.PLC2,), FUEL_AFTER_FILTER_TOP_X, FUEL_AFTER_FILTER_BOTTOM_Y, CENTER_X + Settings.PUMP_THIN_LINE_WIDTH / 2,
                 FUEL_AFTER_FILTER_BOTTOM_Y,
                 horizontal=True, start_joint='right', thin=True, contour=(8, 9), arrow_num=1, arrow_rotation=180),
            Pipe((Device.PLC2,), FUEL_AFTER_FILTER_TOP_X, FUEL_AFTER_FILTER_TOP_Y, FUEL_AFTER_FILTER_BOTTOM_X,
                 OIL_AFTER_FILTER_BOTTOM_Y,
                 horizontal=False, start_joint='sharp', end_joint='sharp', thin=True, contour=(9,), arrow_rotation=90),

            # тонкие трубы бок
            Pipe((Device.PLC2,), FUEL_TANK_1_START_X, FUEL_TANK_1_START_Y, FUEL_TANK_1_END_X,
                 FUEL_TANK_1_END_Y,
                 horizontal=True, start_joint='sharp', end_joint='right', thin=True, contour=(11,), arrow_num=3),
            Pipe((Device.PLC2,), FUEL_TANK_1_END_X, FUEL_TANK_1_END_Y, FUEL_TANK_3_END_X,
                 FUEL_TANK_3_END_Y,
                 horizontal=False, start_joint='right', thin=True, contour=(11,), arrow_num=0),
            Pipe((Device.PLC2,), FUEL_TANK_4_END_X, FUEL_TANK_4_END_Y, FUEL_TANK_5_END_X,
                 FUEL_TANK_5_END_Y,
                 horizontal=False, end_joint='sharp', thin=True, contour=(12,), arrow_rotation=90),

            Pipe((Device.PLC2,), FUEL_TANK_3_END_X, FUEL_TANK_3_END_Y, FUEL_TANK_2_END_X,
                 FUEL_TANK_2_END_Y,
                 horizontal=False, start_joint='right', thin=True, contour=(10,), arrow_num=0),
            Pipe((Device.PLC2,), FUEL_TANK_2_END_X, FUEL_TANK_2_END_Y, FUEL_SMALL_PUMP_X,
                 FUEL_TANK_2_END_Y,
                 horizontal=True, start_joint='left', thin=True, contour=(10,), arrow_num=2),
            Pipe((Device.PLC2,), FUEL_SMALL_PUMP_X, FUEL_SMALL_PUMP_Y, FUEL_TANK_4_END_X,
                 FUEL_TANK_4_END_Y,
                 horizontal=True, end_joint='sharp', thin=True, contour=(10,), arrow_num=1),
            Pipe((Device.PLC2,), FUEL_TANK_4_END_X, FUEL_TANK_4_END_Y, FUEL_TANK_4_END_X,
                 FUEL_TANK_3_END_Y,
                 horizontal=False, start_joint='left', end_joint='left', thin=True, contour=(10,), arrow_rotation=270),
            Pipe((Device.PLC2,), FUEL_TANK_4_END_X, FUEL_TANK_3_END_Y, FUEL_TANK_1_END_X,
                 FUEL_TANK_3_END_Y,
                 horizontal=True, start_joint='left', end_joint='sharp', thin=True, contour=(10,), arrow_num = 1,
                 arrow_rotation=180),


            # счетчик частиц
            Pipe((Device.PLC1, Device.PLC2), COUNTER_START_X, COUNTER_START_Y, COUNTER_X, COUNTER_Y,
                 horizontal=False, start_joint='sharp', thin=True, contour=(2,3,8,9), arrow_num=0),
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
            Valve((Device.PLC1,), OIL_VALVE_V2_X, OIL_VALVE_V2_Y, small=True, contour=(2,),
                  tag=BinaryTags.units.get('oil_valve_2'), signal=handle_status_signal),
            Valve((Device.PLC1,), OIL_VALVE_V3_X, OIL_VALVE_V3_Y, small=True, contour=(3,),
                  tag=BinaryTags.units.get('oil_valve_3'), signal=handle_status_signal),
            Valve((Device.PLC1, ), OIL_VALVE_V5_X, OIL_VALVE_V5_Y, small=True, contour=(5, ), rotation_angle=90,
                  tag=BinaryTags.units.get('oil_valve_5'), signal=handle_status_signal),
            Valve((Device.PLC1,), OIL_VALVE_V6_X, OIL_VALVE_V6_Y, small=True, contour=(6,),
                  tag=BinaryTags.units.get('oil_valve_6'), signal=handle_status_signal),

            Valve((Device.PLC2,), FUEL_VALVE_V2_X, FUEL_VALVE_V2_Y, small=True, contour=(8,),
                  tag=BinaryTags.units.get('fuel_valve_2'), signal=handle_status_signal),
            Valve((Device.PLC2,), FUEL_VALVE_V3_X, FUEL_VALVE_V3_Y, small=True, contour=(9,),
                  tag=BinaryTags.units.get('fuel_valve_3'), signal=handle_status_signal),
            Valve((Device.PLC2,), FUEL_VALVE_V5_X, FUEL_VALVE_V5_Y, small=True, contour=(11,), rotation_angle=90,
                  tag=BinaryTags.units.get('fuel_valve_5'), signal=handle_status_signal),
            Valve((Device.PLC2,), FUEL_VALVE_V6_X, FUEL_VALVE_V6_Y, small=True, contour=(12,),
                  tag=BinaryTags.units.get('fuel_valve_6'), signal=handle_status_signal),
        ]

        for valve in self.valves:
            self.set_active_contours.connect(valve.handle_contour_change)

            self.scene.addItem(valve)


class Scheme(QGraphicsView):
    set_active_contours = Signal(set)
    handle_contour_status = Signal(int, int, bool)

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

        self.active_contours = {1,4,7,10}

        self.pipe_system = _PipeSystem(self.scene, self.set_active_contours)
        self.valve_system = _ValveSystem(
            self.scene,
            self.set_active_contours,
            handle_status_signal=self.handle_contour_status
        )

        self.set_active_contours.emit(self.active_contours)


    def wheelEvent(self, event: QWheelEvent):
        pass

    @Slot(int, int, bool)
    def change_contour_status(self, device: int, contour: int, val: bool):
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