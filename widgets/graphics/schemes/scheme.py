from PySide6.QtCore import Qt, QRectF, QObject
from PySide6.QtGui import QPen, QColor, QWheelEvent, QPainter
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsItem, QWidget, QGraphicsProxyWidget

from widgets.graphics.components.arrow import Arrow
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

        self.oil_header = SchemeHeader(position=1)
        self.oil_header_proxy = QGraphicsProxyWidget()
        self.oil_header_proxy.setWidget(self.oil_header)
        self.oil_header_proxy.setPos(HEADER_OIL_X, HEADER_OIL_Y)
        self.scene.addItem(self.oil_header_proxy)

        self.fuel_header = SchemeHeader(position=2)
        self.fuel_header_proxy = QGraphicsProxyWidget()
        self.fuel_header_proxy.setWidget(self.fuel_header)
        self.fuel_header_proxy.setPos(HEADER_FUEL_X, HEADER_FUEL_Y)
        self.scene.addItem(self.fuel_header_proxy)

class _PipeSystem(QObject):
    def __init__(
            self,
            scene: QGraphicsScene,
            position: int,
            signal_fn_contour=None,
            signal_fn_flow=None
    ):
        super().__init__()
        self.position = position
        self.scene = scene

        self.pipes = [
            # масляный стенд

            # внешний контур
            Pipe((1,), OIL_RIGHT_TOP_KNEE_X, OIL_RIGHT_TOP_KNEE_Y, OIL_LEFT_TOP_KNEE_X, OIL_LEFT_TOP_KNEE_Y, horizontal=True,
                 start_joint='left', end_joint='left', contour=(1,), arrow_rotation=180),
            Pipe((1,), OIL_LEFT_TOP_KNEE_X, OIL_LEFT_TOP_KNEE_Y, OIL_LEFT_BOTTOM_KNEE_X, OIL_LEFT_BOTTOM_KNEE_Y,
                 horizontal=False, start_joint='left', end_joint='left', contour=(1,), arrow_rotation=90),
            Pipe((1,), OIL_LEFT_BOTTOM_KNEE_X, OIL_LEFT_BOTTOM_KNEE_Y, OIL_PUMP_X, OIL_LEFT_BOTTOM_KNEE_Y,
                 horizontal=True, start_joint='left', contour=(1,), arrow_num=3),
            Pipe((1,), OIL_PUMP_X, OIL_RIGHT_BOTTOM_KNEE_Y, OIL_RIGHT_BOTTOM_KNEE_X, OIL_RIGHT_BOTTOM_KNEE_Y,
                 horizontal=True, end_joint='left', contour=(1,), arrow_num=1),
            Pipe((1,), OIL_RIGHT_BOTTOM_KNEE_X, OIL_RIGHT_BOTTOM_KNEE_Y, OIL_RIGHT_TOP_KNEE_X, OIL_RIGHT_TOP_KNEE_Y,
                 horizontal=False, start_joint='left', end_joint='left', contour=(1,), arrow_rotation=270),

            # тонкие трубы верх
            Pipe((1,), OIL_AFTER_FILTER_TOP_X, OIL_AFTER_FILTER_TOP_Y, OIL_AFTER_FILTER_BOTTOM_X, OIL_AFTER_FILTER_BOTTOM_Y,
                 horizontal=False, start_joint='sharp', end_joint='left', thin=True, contour=(2,), arrow_rotation=90),
            Pipe((1,), OIL_AFTER_FILTER_BOTTOM_X, OIL_AFTER_FILTER_BOTTOM_Y, OIL_BEFORE_FILTER_TOP_X,
                 OIL_BEFORE_FILTER_BOTTOM_Y,
                 horizontal=True, start_joint='left', thin=True, contour=(2,), arrow_num=3),
            Pipe((1,), OIL_BEFORE_FILTER_TOP_X, OIL_BEFORE_FILTER_BOTTOM_Y, CENTER_X - Settings.PUMP_THIN_LINE_WIDTH / 2,
                 OIL_BEFORE_FILTER_BOTTOM_Y,
                 horizontal=True, start_joint='left', thin=True, contour=(2, 3), arrow_num=1),
            Pipe((1,), OIL_BEFORE_FILTER_TOP_X, OIL_BEFORE_FILTER_TOP_Y, OIL_BEFORE_FILTER_BOTTOM_X,
                 OIL_BEFORE_FILTER_BOTTOM_Y,
                 horizontal=False, start_joint='sharp', end_joint='sharp', thin=True, contour=(3,), arrow_rotation=90),

            # тонкие трубы бок
            Pipe((1,), OIL_TANK_1_START_X, OIL_TANK_1_START_Y, OIL_TANK_1_END_X,
                 OIL_TANK_1_END_Y,
                 horizontal=True, start_joint='sharp', end_joint='right', thin=True, contour=(5,), arrow_num=3),
            Pipe((1,), OIL_TANK_1_END_X, OIL_TANK_1_END_Y, OIL_TANK_3_END_X,
                 OIL_TANK_3_END_Y,
                 horizontal=False, start_joint='right', thin=True, contour=(5,), arrow_num=0),
            Pipe((1,), OIL_TANK_4_END_X, OIL_TANK_4_END_Y, OIL_TANK_5_END_X,
                 OIL_TANK_5_END_Y,
                 horizontal=False, end_joint='sharp', thin=True, contour=(6,), arrow_rotation=90),

            Pipe((1,), OIL_TANK_3_END_X, OIL_TANK_3_END_Y, OIL_TANK_2_END_X,
                 OIL_TANK_2_END_Y,
                 horizontal=False, start_joint='right', thin=True, contour=(4,), arrow_num=0),
            Pipe((1,), OIL_TANK_2_END_X, OIL_TANK_2_END_Y, OIL_SMALL_PUMP_X,
                 OIL_TANK_2_END_Y,
                 horizontal=True, start_joint='left', thin=True, contour=(4,), arrow_num=2),
            Pipe((1,), OIL_SMALL_PUMP_X, OIL_SMALL_PUMP_Y, OIL_TANK_4_END_X,
                 OIL_TANK_4_END_Y,
                 horizontal=True, end_joint='sharp', thin=True, contour=(4,), arrow_num=1),
            Pipe((1,), OIL_TANK_4_END_X, OIL_TANK_4_END_Y, OIL_TANK_4_END_X,
                 OIL_TANK_3_END_Y,
                 horizontal=False, start_joint='left', end_joint='left', thin=True, contour=(4,), arrow_rotation=270),
            Pipe((1,), OIL_TANK_4_END_X, OIL_TANK_3_END_Y, OIL_TANK_1_END_X,
                 OIL_TANK_3_END_Y,
                 horizontal=True, start_joint='left', end_joint='sharp', thin=True, contour=(4,), arrow_num = 1,
                 arrow_rotation=180),


            # топливный стенд

            # внешний контур
            Pipe((2,), FUEL_RIGHT_TOP_KNEE_X, FUEL_RIGHT_TOP_KNEE_Y, FUEL_LEFT_TOP_KNEE_X, FUEL_LEFT_TOP_KNEE_Y,
                 horizontal=True,
                 start_joint='left', end_joint='left', contour=(1,), arrow_rotation=180),
            Pipe((2,), FUEL_LEFT_TOP_KNEE_X, FUEL_LEFT_TOP_KNEE_Y, FUEL_LEFT_BOTTOM_KNEE_X, FUEL_LEFT_BOTTOM_KNEE_Y,
                 horizontal=False, start_joint='left', end_joint='left', contour=(1,), arrow_rotation=90),
            Pipe((2,), FUEL_LEFT_BOTTOM_KNEE_X, FUEL_LEFT_BOTTOM_KNEE_Y, FUEL_PUMP_X, FUEL_LEFT_BOTTOM_KNEE_Y,
                 horizontal=True, start_joint='left', contour=(1,), arrow_num=3),
            Pipe((2,), FUEL_PUMP_X, FUEL_RIGHT_BOTTOM_KNEE_Y, FUEL_RIGHT_BOTTOM_KNEE_X, FUEL_RIGHT_BOTTOM_KNEE_Y,
                 horizontal=True, end_joint='left', contour=(1,), arrow_num=1),
            Pipe((2,), FUEL_RIGHT_BOTTOM_KNEE_X, FUEL_RIGHT_BOTTOM_KNEE_Y, FUEL_RIGHT_TOP_KNEE_X, FUEL_RIGHT_TOP_KNEE_Y,
                 horizontal=False, start_joint='left', end_joint='left', contour=(1,), arrow_rotation=270),

            # тонкие трубы верх
            Pipe((2,), FUEL_BEFORE_FILTER_BOTTOM_X, FUEL_BEFORE_FILTER_BOTTOM_Y, FUEL_AFTER_FILTER_TOP_X,
                 FUEL_AFTER_FILTER_BOTTOM_Y,
                 horizontal=True, start_joint='right', thin=True, contour=(2,), arrow_num=3, arrow_rotation=180),
            Pipe((2,), FUEL_BEFORE_FILTER_TOP_X, FUEL_BEFORE_FILTER_TOP_Y, FUEL_BEFORE_FILTER_BOTTOM_X,
                 FUEL_BEFORE_FILTER_BOTTOM_Y,
                 horizontal=False, start_joint='sharp', end_joint='right', thin=True, contour=(3,), arrow_rotation=90),
            Pipe((2,), FUEL_AFTER_FILTER_TOP_X, FUEL_AFTER_FILTER_BOTTOM_Y, CENTER_X + Settings.PUMP_THIN_LINE_WIDTH / 2,
                 FUEL_AFTER_FILTER_BOTTOM_Y,
                 horizontal=True, start_joint='right', thin=True, contour=(2, 3), arrow_num=1, arrow_rotation=180),
            Pipe((2,), FUEL_AFTER_FILTER_TOP_X, FUEL_AFTER_FILTER_TOP_Y, FUEL_AFTER_FILTER_BOTTOM_X,
                 OIL_AFTER_FILTER_BOTTOM_Y,
                 horizontal=False, start_joint='sharp', end_joint='sharp', thin=True, contour=(2,), arrow_rotation=90),

            # тонкие трубы бок
            Pipe((1,), FUEL_TANK_1_START_X, FUEL_TANK_1_START_Y, FUEL_TANK_1_END_X,
                 FUEL_TANK_1_END_Y,
                 horizontal=True, start_joint='sharp', end_joint='right', thin=True, contour=(5,), arrow_num=3),
            Pipe((1,), FUEL_TANK_1_END_X, FUEL_TANK_1_END_Y, FUEL_TANK_3_END_X,
                 FUEL_TANK_3_END_Y,
                 horizontal=False, start_joint='right', thin=True, contour=(5,), arrow_num=0),
            Pipe((1,), FUEL_TANK_4_END_X, FUEL_TANK_4_END_Y, FUEL_TANK_5_END_X,
                 FUEL_TANK_5_END_Y,
                 horizontal=False, end_joint='sharp', thin=True, contour=(6,), arrow_rotation=90),

            Pipe((1,), FUEL_TANK_3_END_X, FUEL_TANK_3_END_Y, FUEL_TANK_2_END_X,
                 FUEL_TANK_2_END_Y,
                 horizontal=False, start_joint='right', thin=True, contour=(4,), arrow_num=0),
            Pipe((1,), FUEL_TANK_2_END_X, FUEL_TANK_2_END_Y, FUEL_SMALL_PUMP_X,
                 FUEL_TANK_2_END_Y,
                 horizontal=True, start_joint='left', thin=True, contour=(4,), arrow_num=2),
            Pipe((1,), FUEL_SMALL_PUMP_X, FUEL_SMALL_PUMP_Y, FUEL_TANK_4_END_X,
                 FUEL_TANK_4_END_Y,
                 horizontal=True, end_joint='sharp', thin=True, contour=(4,), arrow_num=1),
            Pipe((1,), FUEL_TANK_4_END_X, FUEL_TANK_4_END_Y, FUEL_TANK_4_END_X,
                 FUEL_TANK_3_END_Y,
                 horizontal=False, start_joint='left', end_joint='left', thin=True, contour=(4,), arrow_rotation=270),
            Pipe((1,), FUEL_TANK_4_END_X, FUEL_TANK_3_END_Y, FUEL_TANK_1_END_X,
                 FUEL_TANK_3_END_Y,
                 horizontal=True, start_joint='left', end_joint='sharp', thin=True, contour=(4,), arrow_num = 1,
                 arrow_rotation=180),


            # счетчик частиц
            Pipe((1, 2), COUNTER_START_X, COUNTER_START_Y, COUNTER_X, COUNTER_Y,
                 horizontal=False, start_joint='sharp', thin=True, contour=(2,3), arrow_num=0),

            # Pipe(RIGHT, HIGHER_BOTTOM, PUMP_X, HIGHER_BOTTOM, horizontal=True, start_joint='right', contour=(1, 2)),
            # Pipe(PUMP_X, BOTTOM, LEFT, BOTTOM, horizontal=True, end_joint='right', contour=(1, 2)),
            # Pipe(LEFT, BOTTOM, LEFT, MIDDLE_PIPE_Y, horizontal=False, start_joint='right', contour=(1, 2)),
            #
            # толстые трубы верхняя часть (контур 2)
            #
            # Pipe(LEFT, MIDDLE_PIPE_Y - Settings.PIPE_THICK_WIDTH, LEFT, TOP, horizontal=False, end_joint='right',
            #      contour=(2,)),
            # Pipe(LEFT, TOP, RIGHT, TOP, horizontal=True, start_joint='right', end_joint='right', contour=(2,)),
            # Pipe(RIGHT, TOP, RIGHT, MIDDLE_PIPE_Y - Settings.PIPE_THICK_WIDTH, horizontal=False,
            #      start_joint='right', contour=(2,)),
            # Pipe(RIGHT, RIGHT_KNEE_Y, RIGHT_KNEE_X, RIGHT_KNEE_Y, horizontal=True, start_joint='sharp',
            #      end_joint='left', contour=(2,)),
            # Pipe(RIGHT_KNEE_X, RIGHT_KNEE_Y, KNEE_END_X, KNEE_END_Y, horizontal=False, start_joint='left',
            #      contour=(2,)),
            #
            # # тонкие трубы верхняя часть (контур 2)
            #
            # Pipe(LEFT, LEFT_THIN_KNEE_Y, LEFT_THIN_KNEE_X, LEFT_THIN_KNEE_Y, horizontal=True, start_joint='sharp',
            #      end_joint='right',
            #      thin=True, contour=(2,)),
            # Pipe(LEFT_THIN_KNEE_X, LEFT_THIN_KNEE_Y, LEFT_THIN_KNEE_LOWER_X, LEFT_THIN_KNEE_LOWER_Y,
            #      horizontal=False, start_joint='right', end_joint='left',
            #      thin=True, contour=(2,)),
            # Pipe(LEFT_THIN_KNEE_LOWER_X, LEFT_THIN_KNEE_LOWER_Y, RIGHT, LEFT_THIN_KNEE_LOWER_Y, horizontal=True,
            #      start_joint='left', end_joint='sharp',
            #      thin=True, contour=(2,)),
            #
            # Pipe(RIGHT, RIGHT_THIN_KNEE_Y, RIGHT_THIN_KNEE_X, RIGHT_THIN_KNEE_Y, horizontal=True,
            #      start_joint='sharp', end_joint='left',
            #      thin=True, contour=(2,)),
            # Pipe(RIGHT_THIN_KNEE_X, RIGHT_THIN_KNEE_Y, RIGHT_THIN_KNEE_LOWER_X, RIGHT_THIN_KNEE_LOWER_Y,
            #      horizontal=False, start_joint='left', end_joint='left',
            #      thin=True, contour=(2,)),
            # Pipe(RIGHT_THIN_KNEE_LOWER_X, RIGHT_THIN_KNEE_LOWER_Y, RIGHT, RIGHT_THIN_KNEE_LOWER_Y, horizontal=True,
            #      start_joint='left', end_joint='sharp',
            #      thin=True, contour=(2,)),
            #
            # # толстые трубы средняя часть (контур 1)
            #
            # Pipe(LEFT, MIDDLE_PIPE_Y, RIGHT, MIDDLE_PIPE_Y, horizontal=True, start_joint='sharp', end_joint='sharp',
            #      contour=(1,)),
            # Pipe(MIDDLE_VALVE_PIPE_X, MIDDLE_PIPE_Y, MIDDLE_VALVE_PIPE_X, MIDDLE_VALVE_PIPE_Y, horizontal=False,
            #      start_joint='sharp', contour=(1,)),
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

        self.oil_pipe_system = _PipeSystem(self.scene, position=1)

    def wheelEvent(self, event: QWheelEvent):
        pass