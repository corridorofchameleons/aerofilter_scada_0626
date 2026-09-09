from PySide6.QtCore import QObject
from PySide6.QtWidgets import QGraphicsScene

from app.ui.layouts.scheme_layout import (
    OIL_RIGHT_X, OIL_LEFT_X, OIL_TOP_Y, OIL_BOTTOM_Y, OIL_RIGHT_BOTTOM_Y,
    OIL_PUMP_X, OIL_AFTER_FILTER_X, OIL_FILTER_BOTTOM_Y, OIL_BEFORE_FILTER_X, CENTER_X, OIL_TANK_5_Y,
    OIL_TANK_4_TOP_Y, OIL_TANK_4_BOTTOM_Y, OIL_SMALL_PUMP_X, OIL_TANK_4_LEFT_X, OIL_TANK_4_RIGHT_X, FUEL_RIGHT_X,
    FUEL_TOP_Y, FUEL_LEFT_X, FUEL_BOTTOM_Y, FUEL_PUMP_X, FUEL_RIGHT_BOTTOM_Y, FUEL_AFTER_FILTER_X, FUEL_FILTER_BOTTOM_Y,
    FUEL_BEFORE_FILTER_X, FUEL_TANK_5_Y, FUEL_TANK_4_LEFT_X, FUEL_TANK_4_TOP_Y, FUEL_TANK_4_RIGHT_X,
    FUEL_TANK_4_BOTTOM_Y, FUEL_SMALL_PUMP_X, COUNTER_START_X, COUNTER_START_Y, COUNTER_X, COUNTER_Y
)
from core.settings import Settings
from core.widgets.graphics.components.pipe import Pipe


class PipeSystem(QObject):
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
            Pipe(x=OIL_RIGHT_X, y=OIL_TOP_Y, x2=OIL_LEFT_X,
                 start_joint='left', end_joint='left', contour=(1,), activate_flow=activate_flow, arrows=(0.05, 0.66, 0.95)),
            Pipe(x=OIL_LEFT_X, y=OIL_TOP_Y, y2=OIL_BOTTOM_Y,
                 start_joint='left', end_joint='left', contour=(1,), arrows=(0.45,), activate_flow=activate_flow),
            Pipe(x=OIL_LEFT_X, y=OIL_BOTTOM_Y, x2=OIL_PUMP_X,
                 start_joint='left', contour=(1,), arrows=(0.5, 0.8), activate_flow=activate_flow),
            Pipe(x=OIL_PUMP_X, y=OIL_RIGHT_BOTTOM_Y, x2=OIL_RIGHT_X,
                 end_joint='left', contour=(1,), arrows=(0.7,), activate_flow=activate_flow),
            Pipe(x=OIL_RIGHT_X, y=OIL_RIGHT_BOTTOM_Y, y2=OIL_TOP_Y,
                 start_joint='left', end_joint='left', contour=(1,), arrows=(0.1, 0.5), activate_flow=activate_flow),

            # тонкие трубы верх
            Pipe(x=OIL_AFTER_FILTER_X, y=OIL_TOP_Y, y2=OIL_FILTER_BOTTOM_Y,
                 start_joint='sharp', end_joint='left', thin=True, contour=(2,), arrows=(0.4, 0.8),
                 activate_flow=activate_flow),
            Pipe(x=OIL_AFTER_FILTER_X, y=OIL_FILTER_BOTTOM_Y, x2=OIL_BEFORE_FILTER_X,
                 start_joint='left', thin=True, contour=(2,), arrows=(0.5,),
                 activate_flow=activate_flow),
            Pipe(x=OIL_BEFORE_FILTER_X, y=OIL_FILTER_BOTTOM_Y, x2=CENTER_X - Settings.PIPE_THIN_WIDTH / 2,
                 start_joint='left', thin=True, contour=(2, 3), arrows=(0.5,),
                 activate_flow=activate_flow),
            Pipe(x=OIL_BEFORE_FILTER_X, y=OIL_TOP_Y, y2=OIL_FILTER_BOTTOM_Y,
                 start_joint='sharp', end_joint='sharp', thin=True, contour=(3,), arrows=(0.4, 0.8),
                 activate_flow=activate_flow),

            # тонкие трубы бок
            Pipe(x=OIL_LEFT_X, y=OIL_TANK_5_Y, x2=OIL_TANK_4_LEFT_X,
                 start_joint='sharp', end_joint='right', thin=True, contour=(5,), arrows=(0.4, 0.8),
                 activate_flow=activate_flow),
            Pipe(x=OIL_TANK_4_LEFT_X, y=OIL_TANK_5_Y, y2=OIL_TANK_4_TOP_Y,
                 start_joint='right', thin=True, contour=(5,),
                 activate_flow=activate_flow),

            Pipe(x=OIL_TANK_4_RIGHT_X, y=OIL_TANK_4_BOTTOM_Y, y2=OIL_BOTTOM_Y,
                 end_joint='sharp', thin=True, contour=(6,), arrows=(0.48,),
                 activate_flow=activate_flow),

            Pipe(x=OIL_TANK_4_LEFT_X, y=OIL_TANK_4_TOP_Y, y2=OIL_TANK_4_BOTTOM_Y - Settings.PUMP_HEIGHT * Settings.SMALL_PUMP_QUOTIENT * 0.5,
                 end_joint='left', thin=True, contour=(4,), arrows=(0.8,),
                 activate_flow=activate_flow),
            Pipe(x=OIL_TANK_4_LEFT_X, y=OIL_TANK_4_BOTTOM_Y - Settings.PUMP_HEIGHT * Settings.SMALL_PUMP_QUOTIENT * 0.5, x2=OIL_SMALL_PUMP_X,
                 start_joint='left', thin=True, contour=(4,), arrows=(0.2,),
                 activate_flow=activate_flow),
            Pipe(x=OIL_SMALL_PUMP_X, y=OIL_TANK_4_BOTTOM_Y, x2=OIL_TANK_4_RIGHT_X,
                 end_joint='sharp', thin=True, contour=(4,), arrows=(0.7,),
                 activate_flow=activate_flow),
            Pipe(x=OIL_TANK_4_RIGHT_X, y=OIL_TANK_4_BOTTOM_Y, y2=OIL_TANK_4_TOP_Y,
                 start_joint='left', end_joint='left', thin=True, contour=(4,), arrows=(0.3, 0.7),
                 activate_flow=activate_flow),
            Pipe(x=OIL_TANK_4_RIGHT_X, y=OIL_TANK_4_TOP_Y, x2=OIL_TANK_4_LEFT_X,
                 start_joint='left', end_joint='sharp', thin=True, contour=(4,), arrows=(0.5,),
                 activate_flow=activate_flow),

            # топливный стенд

            # внешний контур
            Pipe(x=FUEL_RIGHT_X, y=FUEL_TOP_Y, x2=FUEL_LEFT_X,
                 start_joint='left', end_joint='left', contour=(7,), activate_flow=activate_flow,
                 arrows=(0.05, 0.66, 0.95)),
            Pipe(x=FUEL_LEFT_X, y=FUEL_TOP_Y, y2=FUEL_BOTTOM_Y,
                 start_joint='left', end_joint='left', contour=(7,), arrows=(0.45,), activate_flow=activate_flow),
            Pipe(x=FUEL_LEFT_X, y=FUEL_BOTTOM_Y, x2=FUEL_PUMP_X,
                 start_joint='left', contour=(7,), arrows=(0.5, 0.8), activate_flow=activate_flow),
            Pipe(x=FUEL_PUMP_X, y=FUEL_RIGHT_BOTTOM_Y, x2=FUEL_RIGHT_X,
                 end_joint='left', contour=(7,), arrows=(0.7,), activate_flow=activate_flow),
            Pipe(x=FUEL_RIGHT_X, y=FUEL_RIGHT_BOTTOM_Y, y2=FUEL_TOP_Y,
                 start_joint='left', end_joint='left', contour=(7,), arrows=(0.1, 0.5), activate_flow=activate_flow),

            # тонкие трубы верх
            Pipe(x=FUEL_BEFORE_FILTER_X, y=FUEL_FILTER_BOTTOM_Y, x2=FUEL_AFTER_FILTER_X,
                 start_joint='right', thin=True, contour=(9,), arrows=(0.5,),
                 activate_flow=activate_flow),
            Pipe(x=FUEL_AFTER_FILTER_X, y=FUEL_FILTER_BOTTOM_Y, x2=CENTER_X + Settings.PIPE_THIN_WIDTH / 2,
                 start_joint='left', thin=True, contour=(8, 9), arrows=(0.5,),
                 activate_flow=activate_flow),
            Pipe(x=FUEL_AFTER_FILTER_X, y=FUEL_TOP_Y, y2=FUEL_FILTER_BOTTOM_Y,
                 start_joint='sharp', end_joint='sharp', thin=True, contour=(8,), arrows=(0.4, 0.8),
                 activate_flow=activate_flow),
            Pipe(x=FUEL_BEFORE_FILTER_X, y=FUEL_TOP_Y, y2=FUEL_FILTER_BOTTOM_Y,
                 start_joint='sharp', end_joint='right', thin=True, contour=(9,), arrows=(0.4, 0.8),
                 activate_flow=activate_flow),

            # тонкие трубы бок
            Pipe(x=FUEL_LEFT_X, y=FUEL_TANK_5_Y, x2=FUEL_TANK_4_LEFT_X,
                 start_joint='sharp', end_joint='right', thin=True, contour=(11,), arrows=(0.4, 0.8),
                 activate_flow=activate_flow),
            Pipe(x=FUEL_TANK_4_LEFT_X, y=FUEL_TANK_5_Y, y2=FUEL_TANK_4_TOP_Y,
                 start_joint='right', thin=True, contour=(11,),
                 activate_flow=activate_flow),

            Pipe(x=FUEL_TANK_4_RIGHT_X, y=FUEL_TANK_4_BOTTOM_Y, y2=FUEL_BOTTOM_Y,
                 end_joint='sharp', thin=True, contour=(12,), arrows=(0.48,),
                 activate_flow=activate_flow),

            Pipe(x=FUEL_TANK_4_LEFT_X, y=FUEL_TANK_4_TOP_Y,
                 y2=FUEL_TANK_4_BOTTOM_Y - Settings.PUMP_HEIGHT * Settings.SMALL_PUMP_QUOTIENT * 0.5,
                 end_joint='left', thin=True, contour=(10,), arrows=(0.8,),
                 activate_flow=activate_flow),
            Pipe(x=FUEL_TANK_4_LEFT_X, y=FUEL_TANK_4_BOTTOM_Y - Settings.PUMP_HEIGHT * Settings.SMALL_PUMP_QUOTIENT * 0.5,
                 x2=FUEL_SMALL_PUMP_X,
                 start_joint='left', thin=True, contour=(10,), arrows=(0.2,),
                 activate_flow=activate_flow),
            Pipe(x=FUEL_SMALL_PUMP_X, y=FUEL_TANK_4_BOTTOM_Y, x2=FUEL_TANK_4_RIGHT_X,
                 end_joint='sharp', thin=True, contour=(10,), arrows=(0.7,),
                 activate_flow=activate_flow),
            Pipe(x=FUEL_TANK_4_RIGHT_X, y=FUEL_TANK_4_BOTTOM_Y, y2=FUEL_TANK_4_TOP_Y,
                 start_joint='left', end_joint='left', thin=True, contour=(10,), arrows=(0.3, 0.7),
                 activate_flow=activate_flow),
            Pipe(x=FUEL_TANK_4_RIGHT_X, y=FUEL_TANK_4_TOP_Y, x2=FUEL_TANK_4_LEFT_X,
                 start_joint='left', end_joint='sharp', thin=True, contour=(10,), arrows=(0.5,),
                 activate_flow=activate_flow),

            Pipe(COUNTER_START_X, COUNTER_START_Y, COUNTER_X, COUNTER_Y,
                 start_joint='sharp', thin=True, contour=(2, 3, 8, 9), arrows=(0.35,),
                 activate_flow=activate_flow),

            # # топливный стенд
            #
            # # внешний контур
            # Pipe(FUEL_RIGHT_TOP_KNEE_X, FUEL_RIGHT_TOP_KNEE_Y, FUEL_LEFT_TOP_KNEE_X, FUEL_LEFT_TOP_KNEE_Y,
            #      horizontal=True,
            #      start_joint='left', end_joint='left', contour=(7,), arrow_rotation=180, activate_flow=activate_flow),
            # Pipe(FUEL_LEFT_TOP_KNEE_X, FUEL_LEFT_TOP_KNEE_Y, FUEL_LEFT_BOTTOM_KNEE_X, FUEL_LEFT_BOTTOM_KNEE_Y,
            #      horizontal=False, start_joint='left', end_joint='left', contour=(7,), arrow_rotation=90,
            #      activate_flow=activate_flow),
            # Pipe(FUEL_LEFT_BOTTOM_KNEE_X, FUEL_LEFT_BOTTOM_KNEE_Y, FUEL_PUMP_X, FUEL_LEFT_BOTTOM_KNEE_Y,
            #      horizontal=True, start_joint='left', contour=(7,), arrow_num=3, activate_flow=activate_flow),
            # Pipe(FUEL_PUMP_X, FUEL_RIGHT_BOTTOM_KNEE_Y, FUEL_RIGHT_BOTTOM_KNEE_X, FUEL_RIGHT_BOTTOM_KNEE_Y,
            #      horizontal=True, end_joint='left', contour=(7,), arrow_num=1, activate_flow=activate_flow),
            # Pipe(FUEL_RIGHT_BOTTOM_KNEE_X, FUEL_RIGHT_BOTTOM_KNEE_Y, FUEL_RIGHT_TOP_KNEE_X, FUEL_RIGHT_TOP_KNEE_Y,
            #      horizontal=False, start_joint='left', end_joint='left', contour=(7,), arrow_rotation=270, arrow_num=1,
            #      activate_flow=activate_flow),
            #
            # # тонкие трубы верх
            # Pipe(FUEL_BEFORE_FILTER_BOTTOM_X, FUEL_BEFORE_FILTER_BOTTOM_Y, FUEL_AFTER_FILTER_TOP_X,
            #      FUEL_AFTER_FILTER_BOTTOM_Y,
            #      horizontal=True, start_joint='right', thin=True, contour=(8,), arrow_num=3, arrow_rotation=180,
            #      activate_flow=activate_flow),
            # Pipe(FUEL_BEFORE_FILTER_TOP_X, FUEL_BEFORE_FILTER_TOP_Y, FUEL_BEFORE_FILTER_BOTTOM_X,
            #      FUEL_BEFORE_FILTER_BOTTOM_Y,
            #      horizontal=False, start_joint='sharp', end_joint='right', thin=True, contour=(8,), arrow_rotation=90,
            #      activate_flow=activate_flow),
            # Pipe(FUEL_AFTER_FILTER_TOP_X, FUEL_AFTER_FILTER_BOTTOM_Y, CENTER_X + Settings.PUMP_THIN_LINE_WIDTH / 2,
            #      FUEL_AFTER_FILTER_BOTTOM_Y,
            #      horizontal=True, start_joint='right', thin=True, contour=(8, 9), arrow_num=1, arrow_rotation=180,
            #      activate_flow=activate_flow),
            # Pipe(FUEL_AFTER_FILTER_TOP_X, FUEL_AFTER_FILTER_TOP_Y, FUEL_AFTER_FILTER_BOTTOM_X,
            #      OIL_AFTER_FILTER_BOTTOM_Y,
            #      horizontal=False, start_joint='sharp', end_joint='sharp', thin=True, contour=(9,), arrow_rotation=90,
            #      activate_flow=activate_flow),
            #
            # # тонкие трубы бок
            # Pipe(FUEL_TANK_1_START_X, FUEL_TANK_1_START_Y, FUEL_TANK_1_END_X,
            #      FUEL_TANK_1_END_Y,
            #      horizontal=True, start_joint='sharp', end_joint='right', thin=True, contour=(11,), arrow_num=3,
            #      activate_flow=activate_flow),
            # Pipe(FUEL_TANK_1_END_X, FUEL_TANK_1_END_Y, FUEL_TANK_3_END_X,
            #      FUEL_TANK_3_END_Y,
            #      horizontal=False, start_joint='right', thin=True, contour=(11,), arrow_num=0,
            #      activate_flow=activate_flow),
            # Pipe(FUEL_TANK_4_END_X, FUEL_TANK_4_END_Y, FUEL_TANK_5_END_X,
            #      FUEL_TANK_5_END_Y,
            #      horizontal=False, end_joint='sharp', thin=True, contour=(12,), arrow_rotation=90, arrow_num=1,
            #      activate_flow=activate_flow),
            #
            # Pipe(FUEL_TANK_3_END_X, FUEL_TANK_3_END_Y, FUEL_TANK_2_END_X,
            #      FUEL_TANK_2_END_Y,
            #      horizontal=False, start_joint='right', thin=True, contour=(10,), arrow_num=0,
            #      activate_flow=activate_flow),
            # Pipe(FUEL_TANK_2_END_X, FUEL_TANK_2_END_Y, FUEL_SMALL_PUMP_X,
            #      FUEL_TANK_2_END_Y,
            #      horizontal=True, start_joint='left', thin=True, contour=(10,), arrow_num=2,
            #      activate_flow=activate_flow),
            # Pipe(FUEL_SMALL_PUMP_X, FUEL_SMALL_PUMP_Y, FUEL_TANK_4_END_X,
            #      FUEL_TANK_4_END_Y,
            #      horizontal=True, end_joint='sharp', thin=True, contour=(10,), arrow_num=1,
            #      activate_flow=activate_flow),
            # Pipe(FUEL_TANK_4_END_X, FUEL_TANK_4_END_Y, FUEL_TANK_4_END_X,
            #      FUEL_TANK_3_END_Y,
            #      horizontal=False, start_joint='left', end_joint='left', thin=True, contour=(10,), arrow_rotation=270,
            #      activate_flow=activate_flow),
            # Pipe(FUEL_TANK_4_END_X, FUEL_TANK_3_END_Y, FUEL_TANK_1_END_X,
            #      FUEL_TANK_3_END_Y,
            #      horizontal=True, start_joint='left', end_joint='sharp', thin=True, contour=(10,), arrow_num=1,
            #      arrow_rotation=180, activate_flow=activate_flow),
            #
            # # счетчик частиц
            # Pipe(COUNTER_START_X, COUNTER_START_Y, COUNTER_X, COUNTER_Y,
            #      horizontal=False, start_joint='sharp', thin=True, contour=(2, 3, 8, 9), arrow_num=0,
            #      activate_flow=activate_flow),
        ]

        for pipe in self.pipes:
            self.set_active_contours.connect(pipe.handle_contour_change)
            self.scene.addItem(pipe)
