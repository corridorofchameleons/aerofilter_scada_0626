from PySide6.QtCore import Qt, QObject, Slot, Signal
from PySide6.QtGui import QWheelEvent
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsProxyWidget, QLabel

from widgets.graphics.components.filter import Filter
from widgets.graphics.components.pipe import Pipe
from widgets.graphics.components.tank import Tank
from widgets.graphics.components.valve import Valve
from widgets.graphics.components.pump import Pump
from widgets.graphics.constants import PIPE_THICK_WIDTH, SCENE_SCALE, VALVE_HALF_HEIGHT, VALUE_BOX_HEIGHT, \
    VALUE_BOX_WIDTH
from widgets.ui_widgets.button import SCADAButton
from widgets.graphics.components.circle_label import CircleLabel
from widgets.ui_widgets.value_box import ValueBox


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
            Pipe(280, -225, 200, -225, horizontal=True, start_joint='sharp', end_joint='left', contour=(2,)),
            Pipe(200, -225, 200, -190, horizontal=False, start_joint='left', contour=(2,)),

            # тонкие трубы верхняя часть (контур 2)

            Pipe(-300, -260, -220, -260, horizontal=True, start_joint='sharp', end_joint='right',
                             thin=True, contour=(2,)),
            Pipe(-220, -260, -220, -90, horizontal=False, start_joint='right', end_joint='left',
                                         thin=True, contour=(2,)),
            Pipe(-220, -90, 280, -90, horizontal=True, start_joint='left', end_joint='sharp',
                                         thin=True, contour=(2,)),
            Pipe(280, -260, 130, -260, horizontal=True, start_joint='sharp', end_joint='left',
                                         thin=True, contour=(2,)),
            Pipe(130, -260, 130, -110, horizontal=False, start_joint='left', end_joint='left',
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
            Valve(-80, 0, text='Отбор проб'), # V3
            Valve(-250, -50, rotation_angle=90), #V2
            Valve(-300, -100), #V1
            Valve(200, -190, text='Отбор проб') #V6
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

        # лейблы

        self.counter_1_label = CircleLabel('Счетчик\nчастиц 4\nРС4')
        self.scene.addItem(self.counter_1_label)
        self.counter_1_label.setPos(-220 * SCENE_SCALE, -260 * SCENE_SCALE)

        self.counter_2_label = CircleLabel('Счетчик\nчастиц 3\nРС3')
        self.scene.addItem(self.counter_2_label)
        self.counter_2_label.setPos(130 * SCENE_SCALE, -260 * SCENE_SCALE)

        # кнопки

        self.switch_button_proxy = QGraphicsProxyWidget()
        self.switch_button = SCADAButton('Режим\nиспытания', self.switch_contour, -310, 340)
        self.switch_button_proxy.setWidget(self.switch_button)
        self.scene.addItem(self.switch_button_proxy)

        self.pump_button_proxy = QGraphicsProxyWidget()
        self.pump_button = SCADAButton('', self.switch_flow, 40, 200)
        self._set_flow_button_text()
        self.pump_button_proxy.setWidget(self.pump_button)
        self.scene.addItem(self.pump_button_proxy)

        self.heater_button_proxy = QGraphicsProxyWidget()
        self.heater_button = SCADAButton('', self.switch_heater, 60, 50)
        self._set_heater_button_text()
        self.heater_button_proxy.setWidget(self.heater_button)
        self.scene.addItem(self.heater_button_proxy)

        # показометры

        self.value_box_ths_1_proxy_temp = QGraphicsProxyWidget()
        self.value_box_ths_1_temp = ValueBox('Темп., С')
        self.value_box_ths_1_proxy_temp.setWidget(self.value_box_ths_1_temp)
        self.scene.addItem(self.value_box_ths_1_proxy_temp)
        self.value_box_ths_1_proxy_temp.setPos(-320 * SCENE_SCALE, -20)

        self.value_box_ths_1_proxy_humidity = QGraphicsProxyWidget()
        self.value_box_ths_1_humidity = ValueBox('Влаж., %')
        self.value_box_ths_1_proxy_humidity.setWidget(self.value_box_ths_1_humidity)
        self.scene.addItem(self.value_box_ths_1_proxy_humidity)
        self.value_box_ths_1_proxy_humidity.setPos(-320 * SCENE_SCALE, -20 + VALUE_BOX_HEIGHT)

        self.value_box_ths_2_proxy_temp = QGraphicsProxyWidget()
        self.value_box_ths_2_temp = ValueBox('Темп., С')
        self.value_box_ths_2_proxy_temp.setWidget(self.value_box_ths_2_temp)
        self.scene.addItem(self.value_box_ths_2_proxy_temp)
        self.value_box_ths_2_proxy_temp.setPos(230 * SCENE_SCALE, -290 * SCENE_SCALE)

        self.value_box_ths_2_proxy_humidity = QGraphicsProxyWidget()
        self.value_box_ths_2_humidity = ValueBox('Влаж., %')
        self.value_box_ths_2_proxy_humidity.setWidget(self.value_box_ths_2_humidity)
        self.scene.addItem(self.value_box_ths_2_proxy_humidity)
        self.value_box_ths_2_proxy_humidity.setPos(230 * SCENE_SCALE, -290 * SCENE_SCALE + VALUE_BOX_HEIGHT)

        self.value_box_ps_1_proxy_pressure = QGraphicsProxyWidget()
        self.value_box_ps_1_pressure = ValueBox('Давление\nдо, Па')
        self.value_box_ps_1_proxy_pressure.setWidget(self.value_box_ps_1_pressure)
        self.scene.addItem(self.value_box_ps_1_proxy_pressure)
        self.value_box_ps_1_proxy_pressure.setPos(-320 * SCENE_SCALE, -370 * SCENE_SCALE)

        self.value_box_ps_2_proxy_pressure = QGraphicsProxyWidget()
        self.value_box_ps_2_pressure = ValueBox('Давление\nдо, Па')
        self.value_box_ps_2_proxy_pressure.setWidget(self.value_box_ps_2_pressure)
        self.scene.addItem(self.value_box_ps_2_proxy_pressure)
        self.value_box_ps_2_proxy_pressure.setPos(230 * SCENE_SCALE, -370 * SCENE_SCALE)

        self.value_box_fm_1_proxy_consumption = QGraphicsProxyWidget()
        self.value_box_fm_1_consumption = ValueBox('Расход\nфакт., л3/ч')
        self.value_box_fm_1_proxy_consumption.setWidget(self.value_box_fm_1_consumption)
        self.scene.addItem(self.value_box_fm_1_proxy_consumption)
        self.value_box_fm_1_proxy_consumption.setPos(-320 * SCENE_SCALE, 260 * SCENE_SCALE)

        self.value_box_fm_11_proxy_consumption = QGraphicsProxyWidget()
        self.value_box_fm_11_consumption = ValueBox('Расход\nз-ный, л3/ч', editable=True)
        self.value_box_fm_11_proxy_consumption.setWidget(self.value_box_fm_11_consumption)
        self.scene.addItem(self.value_box_fm_11_proxy_consumption)
        self.value_box_fm_11_proxy_consumption.setPos(-320 * SCENE_SCALE + VALUE_BOX_WIDTH, 260 * SCENE_SCALE)

        self.value_box_p_11_proxy_freq = QGraphicsProxyWidget()
        self.value_box_p_11_freq = ValueBox('Частота\nнасоса, Гц', editable=True)
        self.value_box_p_11_proxy_freq.setWidget(self.value_box_p_11_freq)
        self.scene.addItem(self.value_box_p_11_proxy_freq)
        self.value_box_p_11_proxy_freq.setPos(-60 * SCENE_SCALE, 200 * SCENE_SCALE)

        self.value_box_t_11_proxy_temp = QGraphicsProxyWidget()
        self.value_box_t_11_temp = ValueBox('Темп.\nз-ная, С', editable=True)
        self.value_box_t_11_proxy_temp.setWidget(self.value_box_t_11_temp)
        self.scene.addItem(self.value_box_t_11_proxy_temp)
        self.value_box_t_11_proxy_temp.setPos(60 * SCENE_SCALE, 105 * SCENE_SCALE)

        self.value_box_t_1_proxy_temp = QGraphicsProxyWidget()
        self.value_box_t_1_temp = ValueBox('Темп.\nфакт., С')
        self.value_box_t_1_proxy_temp.setWidget(self.value_box_t_1_temp)
        self.scene.addItem(self.value_box_t_1_proxy_temp)
        self.value_box_t_1_proxy_temp.setPos(160 * SCENE_SCALE, 105 * SCENE_SCALE)

        self.value_box_c_1_proxy_vol = QGraphicsProxyWidget()
        self.value_box_c_1_vol = ValueBox('Объем, л')
        self.value_box_c_1_proxy_vol.setWidget(self.value_box_c_1_vol)
        self.scene.addItem(self.value_box_c_1_proxy_vol)
        self.value_box_c_1_proxy_vol.setPos(160 * SCENE_SCALE, -30 * SCENE_SCALE)

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
