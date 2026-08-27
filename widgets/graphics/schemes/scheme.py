from PySide6.QtCore import Qt, QRectF, QObject
from PySide6.QtGui import QPen, QColor, QWheelEvent, QPainter
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsItem, QWidget, QGraphicsProxyWidget

from models.device import Device
from widgets.graphics.components.bounding_rect import BoundingRect
from widgets.graphics.components.pipe import Pipe
from widgets.graphics.components.scheme_header import SchemeHeader
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
    FUEL_TANK_1_START_Y, OIL_TANK_5_END_X, OIL_TANK_5_END_Y, FUEL_TANK_5_END_X, FUEL_TANK_5_END_Y
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
            signal_fn_contour=None,
            signal_fn_flow=None
    ):
        super().__init__()
        self.scene = scene

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
                 start_joint='left', end_joint='left', contour=(1,), arrow_rotation=180),
            Pipe((Device.PLC2,), FUEL_LEFT_TOP_KNEE_X, FUEL_LEFT_TOP_KNEE_Y, FUEL_LEFT_BOTTOM_KNEE_X, FUEL_LEFT_BOTTOM_KNEE_Y,
                 horizontal=False, start_joint='left', end_joint='left', contour=(1,), arrow_rotation=90),
            Pipe((Device.PLC2,), FUEL_LEFT_BOTTOM_KNEE_X, FUEL_LEFT_BOTTOM_KNEE_Y, FUEL_PUMP_X, FUEL_LEFT_BOTTOM_KNEE_Y,
                 horizontal=True, start_joint='left', contour=(1,), arrow_num=3),
            Pipe((Device.PLC2,), FUEL_PUMP_X, FUEL_RIGHT_BOTTOM_KNEE_Y, FUEL_RIGHT_BOTTOM_KNEE_X, FUEL_RIGHT_BOTTOM_KNEE_Y,
                 horizontal=True, end_joint='left', contour=(1,), arrow_num=1),
            Pipe((Device.PLC2,), FUEL_RIGHT_BOTTOM_KNEE_X, FUEL_RIGHT_BOTTOM_KNEE_Y, FUEL_RIGHT_TOP_KNEE_X, FUEL_RIGHT_TOP_KNEE_Y,
                 horizontal=False, start_joint='left', end_joint='left', contour=(1,), arrow_rotation=270),

            # тонкие трубы верх
            Pipe((Device.PLC2,), FUEL_BEFORE_FILTER_BOTTOM_X, FUEL_BEFORE_FILTER_BOTTOM_Y, FUEL_AFTER_FILTER_TOP_X,
                 FUEL_AFTER_FILTER_BOTTOM_Y,
                 horizontal=True, start_joint='right', thin=True, contour=(2,), arrow_num=3, arrow_rotation=180),
            Pipe((Device.PLC2,), FUEL_BEFORE_FILTER_TOP_X, FUEL_BEFORE_FILTER_TOP_Y, FUEL_BEFORE_FILTER_BOTTOM_X,
                 FUEL_BEFORE_FILTER_BOTTOM_Y,
                 horizontal=False, start_joint='sharp', end_joint='right', thin=True, contour=(3,), arrow_rotation=90),
            Pipe((Device.PLC2,), FUEL_AFTER_FILTER_TOP_X, FUEL_AFTER_FILTER_BOTTOM_Y, CENTER_X + Settings.PUMP_THIN_LINE_WIDTH / 2,
                 FUEL_AFTER_FILTER_BOTTOM_Y,
                 horizontal=True, start_joint='right', thin=True, contour=(2, 3), arrow_num=1, arrow_rotation=180),
            Pipe((Device.PLC2,), FUEL_AFTER_FILTER_TOP_X, FUEL_AFTER_FILTER_TOP_Y, FUEL_AFTER_FILTER_BOTTOM_X,
                 OIL_AFTER_FILTER_BOTTOM_Y,
                 horizontal=False, start_joint='sharp', end_joint='sharp', thin=True, contour=(2,), arrow_rotation=90),

            # тонкие трубы бок
            Pipe((Device.PLC2,), FUEL_TANK_1_START_X, FUEL_TANK_1_START_Y, FUEL_TANK_1_END_X,
                 FUEL_TANK_1_END_Y,
                 horizontal=True, start_joint='sharp', end_joint='right', thin=True, contour=(5,), arrow_num=3),
            Pipe((Device.PLC2,), FUEL_TANK_1_END_X, FUEL_TANK_1_END_Y, FUEL_TANK_3_END_X,
                 FUEL_TANK_3_END_Y,
                 horizontal=False, start_joint='right', thin=True, contour=(5,), arrow_num=0),
            Pipe((Device.PLC2,), FUEL_TANK_4_END_X, FUEL_TANK_4_END_Y, FUEL_TANK_5_END_X,
                 FUEL_TANK_5_END_Y,
                 horizontal=False, end_joint='sharp', thin=True, contour=(6,), arrow_rotation=90),

            Pipe((Device.PLC2,), FUEL_TANK_3_END_X, FUEL_TANK_3_END_Y, FUEL_TANK_2_END_X,
                 FUEL_TANK_2_END_Y,
                 horizontal=False, start_joint='right', thin=True, contour=(4,), arrow_num=0),
            Pipe((Device.PLC2,), FUEL_TANK_2_END_X, FUEL_TANK_2_END_Y, FUEL_SMALL_PUMP_X,
                 FUEL_TANK_2_END_Y,
                 horizontal=True, start_joint='left', thin=True, contour=(4,), arrow_num=2),
            Pipe((Device.PLC2,), FUEL_SMALL_PUMP_X, FUEL_SMALL_PUMP_Y, FUEL_TANK_4_END_X,
                 FUEL_TANK_4_END_Y,
                 horizontal=True, end_joint='sharp', thin=True, contour=(4,), arrow_num=1),
            Pipe((Device.PLC2,), FUEL_TANK_4_END_X, FUEL_TANK_4_END_Y, FUEL_TANK_4_END_X,
                 FUEL_TANK_3_END_Y,
                 horizontal=False, start_joint='left', end_joint='left', thin=True, contour=(4,), arrow_rotation=270),
            Pipe((Device.PLC2,), FUEL_TANK_4_END_X, FUEL_TANK_3_END_Y, FUEL_TANK_1_END_X,
                 FUEL_TANK_3_END_Y,
                 horizontal=True, start_joint='left', end_joint='sharp', thin=True, contour=(4,), arrow_num = 1,
                 arrow_rotation=180),


            # счетчик частиц
            Pipe((Device.PLC1, Device.PLC2), COUNTER_START_X, COUNTER_START_Y, COUNTER_X, COUNTER_Y,
                 horizontal=False, start_joint='sharp', thin=True, contour=(2,3), arrow_num=0),
        ]

        for pipe in self.pipes:
            # signal_fn_contour.connect(pipe.handle_contour_change)
            # signal_fn_flow.connect(pipe.handle_flow_change)
            self.scene.addItem(pipe)

class Scheme(QGraphicsView):
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

        self.pipe_system = _PipeSystem(self.scene)

    def wheelEvent(self, event: QWheelEvent):
        pass