from PySide6.QtCore import Qt, QObject, Slot, Signal
from PySide6.QtGui import QWheelEvent
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QFrame, QGraphicsProxyWidget

from widgets.graphics.components.filter import Filter
from widgets.graphics.components.pipe import Pipe
from widgets.graphics.components.tank import TankBody, Tank
from widgets.graphics.components.valve import Valve
from widgets.graphics.components.pump import Pump
from widgets.graphics.constants import PIPE_THICK_WIDTH, SCENE_SCALE
from widgets.ui_widgets.button import SCADAButton


class PipeSystem(QObject):

    def __init__(
            self,
            scene: QGraphicsScene,
            signal_fn_contour,
            signal_fn_flow
    ):
        super().__init__()
        self.scene = scene

        self.pipes = [
            # толстые трубы нижняя часть

            Pipe(280, -50, 280, 288, horizontal=False, end_joint='right', contour=(1, 2)),
            Pipe(280, 288, -10, 288, horizontal=True, start_joint='right', contour=(1, 2)),
            Pipe(-10, 300, -300, 300, horizontal=True, end_joint='right', contour=(1, 2)),
            Pipe(-300, 300, -300, -50, horizontal=False, start_joint='right', contour=(1, 2)),

            # толстые трубы верхняя часть (контур 2)

            Pipe(-300, -50 - PIPE_THICK_WIDTH, -300, -350, horizontal=False, end_joint='right', contour=(2,)),
            Pipe(-300, -350, 280, -350, horizontal=True, start_joint='right', end_joint='right', contour=(2,)),
            Pipe(280, -350, 280, -50 - PIPE_THICK_WIDTH, horizontal=False, start_joint='right', contour=(2,)),
            Pipe(280, -210, 200, -210, horizontal=True, start_joint='sharp', end_joint='left', contour=(2,)),
            Pipe(200, -210, 200, -190, horizontal=False, start_joint='left', contour=(2,)),

            # тонкие трубы верхняя часть (контур 2)

            Pipe(-300, -250, -220, -250, horizontal=True, start_joint='sharp', end_joint='right',
                             thin=True, contour=(2,)),
            Pipe(-220, -250, -220, -90, horizontal=False, start_joint='right', end_joint='left',
                                         thin=True, contour=(2,)),
            Pipe(-220, -90, 280, -90, horizontal=True, start_joint='left', end_joint='sharp',
                                         thin=True, contour=(2,)),
            Pipe(280, -250, 130, -250, horizontal=True, start_joint='sharp', end_joint='left',
                                         thin=True, contour=(2,)),
            Pipe(130, -250, 130, -110, horizontal=False, start_joint='left', end_joint='left',
                                         thin=True, contour=(2,)),
            Pipe(130, -110, 280, -110, horizontal=True, start_joint='left', end_joint='sharp',
                                         thin=True, contour=(2,)),

            # толстые трубы средняя часть (контур 1)

            Pipe(-300, -50, 280, -50, horizontal=True, start_joint='sharp', end_joint='sharp', contour=(1,)),
            Pipe(-80, -50, -80, 0, horizontal=False, start_joint='sharp', contour=(1,)),
        ]

        for pipe in self.pipes:
            signal_fn_contour.connect(pipe.handle_contour_change)
            signal_fn_flow.connect(pipe.handle_flow_change)
            self.scene.addItem(pipe)


class ValveSystem(QObject):
    def __init__(
            self,
            scene: QGraphicsScene,
    ):
        super().__init__()
        self.scene = scene

        self.valves = [
            Valve(280, 240), # V5
            Valve(-80, 0), # V3
            Valve(-250, -50, rotation_angle=90), #V2
            Valve(-300, -100), #V1
            Valve(200, -175) #V6
        ]

        for valve in self.valves:
            self.scene.addItem(valve)


class FuelScheme(QGraphicsView):
    contour_changed = Signal(int)
    flow_signal = Signal(bool)
    heater_signal = Signal(bool)
    alarm_max_signal = Signal(bool)
    alarm_min_signal = Signal(bool)
    liquid_level_signal = Signal(float)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.selected_contour = None
        self.flow_active = False
        self.heater_active = False

        # конфига

        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setObjectName('fuelScheme')
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # Отключаем горизонтальный скролл
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setDragMode(QGraphicsView.NoDrag)

        self.scene = QGraphicsScene()
        self.setScene(self.scene)

        # сеть труб

        self.pipes = PipeSystem(self.scene, self.contour_changed, self.flow_signal)

        # сеть клапанов

        self.valves = ValveSystem(self.scene)

        # помпа

        self.pump = Pump(self.flow_signal)
        self.scene.addItem(self.pump)
        self.pump.setPos(-20 * SCENE_SCALE, 300 * SCENE_SCALE)

        # аэрофильтер

        self.filter = Filter()
        self.scene.addItem(self.filter)
        self.filter.setPos(-40 * SCENE_SCALE, -270 * SCENE_SCALE)

        # бак
        self.tank = Tank(self.heater_signal, self.alarm_max_signal, self.alarm_min_signal)
        self.scene.addItem(self.tank)
        self.tank.setPos(240 * SCENE_SCALE, 25 * SCENE_SCALE)

        # кнопки

        self.switch_button_proxy = QGraphicsProxyWidget()
        self.switch_button = SCADAButton('Режим\nиспытания', self.switch_contour, -310, 340)
        self.switch_button_proxy.setWidget(self.switch_button)
        self.scene.addItem(self.switch_button_proxy)

        self.pump_button_proxy = QGraphicsProxyWidget()
        self.pump_button = SCADAButton('', self.switch_flow, 40, 210)
        self._set_flow_button_text()
        self.pump_button_proxy.setWidget(self.pump_button)
        self.scene.addItem(self.pump_button_proxy)

        self.heater_button_proxy = QGraphicsProxyWidget()
        self.heater_button = SCADAButton('', self.switch_heater, 160, 210)
        self._set_heater_button_text()
        self.heater_button_proxy.setWidget(self.heater_button)
        self.scene.addItem(self.heater_button_proxy)

        if self.flow_active:
            self.pump.start_rotation(self.flow_active)
        else:
            self.pump.stop_rotation()
        self.set_selected_contour(2)


    def wheelEvent(self, event: QWheelEvent):
        pass

    @Slot()
    def set_selected_contour(self, new_id: int):
        self.selected_contour = new_id
        self.contour_changed.emit(new_id)


    @Slot()
    def switch_contour(self):
        if not self.selected_contour:
            new_id = 1
        else:
            new_id = 2 if self.selected_contour == 1 else 1

        self.selected_contour = new_id
        self.contour_changed.emit(new_id)

    def _set_flow_button_text(self):
        if self.flow_active:
            self.pump_button.setText('Насос\nСТОП')
        else:
            self.pump_button.setText('Насос\nСТАРТ')

    @Slot()
    def switch_flow(self):
        self.flow_active = not self.flow_active
        self._set_flow_button_text()
        self.flow_signal.emit(self.flow_active)

    def _set_heater_button_text(self):
        if self.heater_active:
            self.heater_button.setText('Нагрев\nСТОП')
        else:
            self.heater_button.setText('Нагрев\nСТАРТ')

    @Slot()
    def switch_heater(self):
        self.heater_active = not self.heater_active
        self._set_heater_button_text()
        self.heater_signal.emit(self.heater_active)
