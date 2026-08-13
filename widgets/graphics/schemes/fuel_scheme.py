from PySide6.QtCore import Qt, QObject, Slot, Signal, QPointF, QEvent
from PySide6.QtGui import QWheelEvent
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsProxyWidget, QLabel, QApplication

from mqtt.topics import COMMAND_TOPIC
from signals.signal_bus import bus
from objects.equipment import EquipmentUnits
from objects.tags import Tags
from widgets.graphics.components.filter import Filter
from widgets.graphics.components.pipe import Pipe
from widgets.graphics.components.tank import Tank
from widgets.graphics.components.valve import Valve
from widgets.graphics.components.pump import Pump
from widgets.graphics.layouts.fuel_layout import RIGHT, LEFT, TOP, BOTTOM, HIGHER_BOTTOM, PUMP_X, PUMP_Y, \
    RIGHT_KNEE_Y, RIGHT_KNEE_X, KNEE_END_X, KNEE_END_Y, LEFT_THIN_KNEE_X, LEFT_THIN_KNEE_Y, RIGHT_THIN_KNEE_Y, \
    RIGHT_THIN_KNEE_X, LEFT_THIN_KNEE_LOWER_X, LEFT_THIN_KNEE_LOWER_Y, RIGHT_THIN_KNEE_LOWER_X, RIGHT_THIN_KNEE_LOWER_Y, \
    MIDDLE_VALVE_PIPE_X, MIDDLE_VALVE_PIPE_Y, VALVE_V1_X, VALVE_V1_Y, VALVE_V2_X, VALVE_V2_Y, VALVE_V3_X, VALVE_V3_Y, \
    VALVE_V5_X, VALVE_V5_Y, VALVE_V6_X, VALVE_V6_Y, MIDDLE_PIPE_Y, FILTER_X, FILTER_Y, TANK_X, TANK_Y
from widgets.settings import Settings
from widgets.ui_widgets.button import SCADAButton
from widgets.graphics.components.circle_label import CircleLabel
from widgets.ui_widgets.value_box import ValueBox


class _PipeSystem(QObject):
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

            Pipe(RIGHT, MIDDLE_PIPE_Y, RIGHT, HIGHER_BOTTOM, horizontal=False, end_joint='right', contour=(1, 2)),
            Pipe(RIGHT, HIGHER_BOTTOM, PUMP_X, HIGHER_BOTTOM, horizontal=True, start_joint='right', contour=(1, 2)),
            Pipe(PUMP_X, BOTTOM, LEFT, BOTTOM, horizontal=True, end_joint='right', contour=(1, 2)),
            Pipe(LEFT, BOTTOM, LEFT, MIDDLE_PIPE_Y, horizontal=False, start_joint='right', contour=(1, 2)),

            # толстые трубы верхняя часть (контур 2)

            Pipe(LEFT, MIDDLE_PIPE_Y - Settings.PIPE_THICK_WIDTH, LEFT, TOP, horizontal=False, end_joint='right', contour=(2,)),
            Pipe(LEFT, TOP, RIGHT, TOP, horizontal=True, start_joint='right', end_joint='right', contour=(2,)),
            Pipe(RIGHT, TOP, RIGHT, MIDDLE_PIPE_Y - Settings.PIPE_THICK_WIDTH, horizontal=False, start_joint='right', contour=(2,)),
            Pipe(RIGHT, RIGHT_KNEE_Y, RIGHT_KNEE_X, RIGHT_KNEE_Y, horizontal=True, start_joint='sharp', end_joint='left', contour=(2,)),
            Pipe(RIGHT_KNEE_X, RIGHT_KNEE_Y, KNEE_END_X, KNEE_END_Y, horizontal=False, start_joint='left', contour=(2,)),

            # тонкие трубы верхняя часть (контур 2)

            Pipe(LEFT, LEFT_THIN_KNEE_Y, LEFT_THIN_KNEE_X, LEFT_THIN_KNEE_Y, horizontal=True, start_joint='sharp', end_joint='right',
                             thin=True, contour=(2,)),
            Pipe(LEFT_THIN_KNEE_X, LEFT_THIN_KNEE_Y, LEFT_THIN_KNEE_LOWER_X, LEFT_THIN_KNEE_LOWER_Y, horizontal=False, start_joint='right', end_joint='left',
                                         thin=True, contour=(2,)),
            Pipe(LEFT_THIN_KNEE_LOWER_X, LEFT_THIN_KNEE_LOWER_Y, RIGHT, LEFT_THIN_KNEE_LOWER_Y, horizontal=True, start_joint='left', end_joint='sharp',
                                         thin=True, contour=(2,)),

            Pipe(RIGHT, RIGHT_THIN_KNEE_Y, RIGHT_THIN_KNEE_X, RIGHT_THIN_KNEE_Y, horizontal=True, start_joint='sharp', end_joint='left',
                                         thin=True, contour=(2,)),
            Pipe(RIGHT_THIN_KNEE_X, RIGHT_THIN_KNEE_Y, RIGHT_THIN_KNEE_LOWER_X, RIGHT_THIN_KNEE_LOWER_Y, horizontal=False, start_joint='left', end_joint='left',
                                         thin=True, contour=(2,)),
            Pipe(RIGHT_THIN_KNEE_LOWER_X, RIGHT_THIN_KNEE_LOWER_Y, RIGHT, RIGHT_THIN_KNEE_LOWER_Y, horizontal=True, start_joint='left', end_joint='sharp',
                                         thin=True, contour=(2,)),

            # толстые трубы средняя часть (контур 1)

            Pipe(LEFT, MIDDLE_PIPE_Y, RIGHT, MIDDLE_PIPE_Y, horizontal=True, start_joint='sharp', end_joint='sharp', contour=(1,)),
            Pipe(MIDDLE_VALVE_PIPE_X, MIDDLE_PIPE_Y, MIDDLE_VALVE_PIPE_X, MIDDLE_VALVE_PIPE_Y, horizontal=False, start_joint='sharp', contour=(1,)),
        ]

        for pipe in self.pipes:
            signal_fn_contour.connect(pipe.handle_contour_change)
            signal_fn_flow.connect(pipe.handle_flow_change)
            self.scene.addItem(pipe)


class _ValveSystem(QObject):
    def __init__(
            self,
            scene: QGraphicsScene,
    ):
        super().__init__()
        self.scene = scene

        self.valves = [
            (Valve(), (VALVE_V1_X, VALVE_V1_Y)),
            (Valve(rotation_angle=90), (VALVE_V2_X, VALVE_V2_Y)),
            (Valve(text='Отбор проб'), (VALVE_V3_X, VALVE_V3_Y)),
            (Valve(), (VALVE_V5_X, VALVE_V5_Y)),
            (Valve(text='Отбор проб'), (VALVE_V6_X, VALVE_V6_Y))
        ]

        for valve in self.valves:
            self.scene.addItem(valve[0])
            valve_point = QPointF(valve[1][0], valve[1][1])
            valve[0].setPos(valve_point)


class _ValueBoxSystem(QObject):
    def __init__(
            self,
            scene: QGraphicsScene,
    ):
        super().__init__()
        self.scene = scene

        self.value_box_ths_1_proxy_temp = QGraphicsProxyWidget()
        self.value_box_ths_1_temp = ValueBox('Темп., С')
        self.value_box_ths_1_proxy_temp.setWidget(self.value_box_ths_1_temp)
        self.scene.addItem(self.value_box_ths_1_proxy_temp)
        self.value_box_ths_1_proxy_temp.setPos(-320 * Settings.SCENE_SCALE, -20)

        self.value_box_ths_1_proxy_humidity = QGraphicsProxyWidget()
        self.value_box_ths_1_humidity = ValueBox('Влаж., %')
        self.value_box_ths_1_proxy_humidity.setWidget(self.value_box_ths_1_humidity)
        self.scene.addItem(self.value_box_ths_1_proxy_humidity)
        self.value_box_ths_1_proxy_humidity.setPos(-320 * Settings.SCENE_SCALE, -20 + Settings.VALUE_BOX_HEIGHT)

        self.value_box_ths_2_proxy_temp = QGraphicsProxyWidget()
        self.value_box_ths_2_temp = ValueBox('Темп., С')
        self.value_box_ths_2_proxy_temp.setWidget(self.value_box_ths_2_temp)
        self.scene.addItem(self.value_box_ths_2_proxy_temp)
        self.value_box_ths_2_proxy_temp.setPos(230 * Settings.SCENE_SCALE, -290 * Settings.SCENE_SCALE)

        self.value_box_ths_2_proxy_humidity = QGraphicsProxyWidget()
        self.value_box_ths_2_humidity = ValueBox('Влаж., %')
        self.value_box_ths_2_proxy_humidity.setWidget(self.value_box_ths_2_humidity)
        self.scene.addItem(self.value_box_ths_2_proxy_humidity)
        self.value_box_ths_2_proxy_humidity.setPos(230 * Settings.SCENE_SCALE, -290 * Settings.SCENE_SCALE + Settings.VALUE_BOX_HEIGHT)

        self.value_box_ps_1_proxy_pressure = QGraphicsProxyWidget()
        value_box_ps_1_tag = Tags.units.get('pressure1')
        self.value_box_ps_1_pressure = ValueBox('Давление\nдо, Па', value_box_ps_1_tag.update_value)
        self.value_box_ps_1_proxy_pressure.setWidget(self.value_box_ps_1_pressure)
        self.scene.addItem(self.value_box_ps_1_proxy_pressure)
        self.value_box_ps_1_proxy_pressure.setPos(-320 * Settings.SCENE_SCALE, -370 * Settings.SCENE_SCALE)

        self.value_box_ps_2_proxy_pressure = QGraphicsProxyWidget()
        value_box_ps_2_tag = Tags.units.get('pressure2')
        self.value_box_ps_2_pressure = ValueBox('Давление\nпосле, Па', value_box_ps_2_tag.update_value)
        self.value_box_ps_2_proxy_pressure.setWidget(self.value_box_ps_2_pressure)
        self.scene.addItem(self.value_box_ps_2_proxy_pressure)
        self.value_box_ps_2_proxy_pressure.setPos(230 * Settings.SCENE_SCALE, -370 * Settings.SCENE_SCALE)

        self.value_box_fm_1_proxy_consumption = QGraphicsProxyWidget()
        self.value_box_fm_1_consumption = ValueBox('Фактический\nрасход., л3/ч', size=3)
        self.value_box_fm_1_proxy_consumption.setWidget(self.value_box_fm_1_consumption)
        self.scene.addItem(self.value_box_fm_1_proxy_consumption)
        self.value_box_fm_1_proxy_consumption.setPos(-320 * Settings.SCENE_SCALE, 260 * Settings.SCENE_SCALE)

        self.value_box_fm_11_proxy_consumption = QGraphicsProxyWidget()
        self.value_box_fm_11_consumption = ValueBox('Заданный\nрасход л3/ч', size=3)
        self.value_box_fm_11_proxy_consumption.setWidget(self.value_box_fm_11_consumption)
        self.scene.addItem(self.value_box_fm_11_proxy_consumption)
        self.value_box_fm_11_proxy_consumption.setPos(-320 * Settings.SCENE_SCALE + Settings.VALUE_BOX_WIDTH * 1.5, 260 * Settings.SCENE_SCALE)

        self.value_box_p_11_proxy_freq = QGraphicsProxyWidget()
        self.value_box_p_11_freq = ValueBox('Частота\nнасоса, Гц')
        self.value_box_p_11_proxy_freq.setWidget(self.value_box_p_11_freq)
        self.scene.addItem(self.value_box_p_11_proxy_freq)
        self.value_box_p_11_proxy_freq.setPos(-60 * Settings.SCENE_SCALE, 200 * Settings.SCENE_SCALE)

        self.value_box_t_11_proxy_temp = QGraphicsProxyWidget()
        self.value_box_t_11_temp = ValueBox('Темп.\nз-ная, С')
        self.value_box_t_11_proxy_temp.setWidget(self.value_box_t_11_temp)
        self.scene.addItem(self.value_box_t_11_proxy_temp)
        self.value_box_t_11_proxy_temp.setPos(60 * Settings.SCENE_SCALE, 105 * Settings.SCENE_SCALE)

        self.value_box_t_1_proxy_temp = QGraphicsProxyWidget()
        self.value_box_t_1_temp = ValueBox('Темп.\nфакт., С')
        self.value_box_t_1_proxy_temp.setWidget(self.value_box_t_1_temp)
        self.scene.addItem(self.value_box_t_1_proxy_temp)
        self.value_box_t_1_proxy_temp.setPos(160 * Settings.SCENE_SCALE, 105 * Settings.SCENE_SCALE)

        self.value_box_c_1_proxy_vol = QGraphicsProxyWidget()
        self.value_box_c_1_vol = ValueBox('Объем, л')
        self.value_box_c_1_proxy_vol.setWidget(self.value_box_c_1_vol)
        self.scene.addItem(self.value_box_c_1_proxy_vol)
        self.value_box_c_1_proxy_vol.setPos(160 * Settings.SCENE_SCALE, -30 * Settings.SCENE_SCALE)


class _Pump(QObject):
    def __init__(
            self,
            scene: QGraphicsScene,
            flow_signal
    ):
        super().__init__()
        self.scene = scene

        self.pump = Pump(flow_signal)
        self.scene.addItem(self.pump)
        self.pump.setPos(PUMP_X, PUMP_Y)

        self.obj = EquipmentUnits.units.get('pump_1')

class _Tank(QObject):
    def __init__(
            self,
            scene: QGraphicsScene,
            heater_signal,
            alarm_max_signal,
            alarm_min_signal
    ):
        super().__init__()
        self.scene = scene

        self.heater_signal = heater_signal
        self.alarm_max_signal = alarm_max_signal
        self.alarm_min_signal = alarm_min_signal

        self.tank = Tank(self.heater_signal, self.alarm_max_signal, self.alarm_min_signal)
        self.scene.addItem(self.tank)
        self.tank.setPos(TANK_X, TANK_Y)

        self.obj = EquipmentUnits.units.get('heater_1')


class _Filter(QObject):
    def __init__(
            self,
            scene: QGraphicsScene,
    ):
        super().__init__()
        self.scene = scene

        self.filter = Filter()
        self.scene.addItem(self.filter)
        self.filter.setPos(FILTER_X, FILTER_Y)


class _ButtonSystem(QObject):
    def __init__(
            self,
            scene: QGraphicsScene,
            switch_contour,
            switch_flow,
            switch_heater,
    ):
        super().__init__()
        self.scene = scene

        # self.switch_contour = switch_contour
        # self.switch_flow = switch_flow
        # self.switch_heater = switch_heater

        self.switch_button_proxy = QGraphicsProxyWidget()
        self.switch_button = SCADAButton('Режим\nиспытания', switch_contour, -310, 340, size=2)
        self.switch_button_proxy.setWidget(self.switch_button)
        self.scene.addItem(self.switch_button_proxy)

        self.pump_button_proxy = QGraphicsProxyWidget()
        self.pump_button = SCADAButton('', switch_flow, 40, 200)
        self.pump_button_proxy.setWidget(self.pump_button)
        self.scene.addItem(self.pump_button_proxy)

        self.heater_button_proxy = QGraphicsProxyWidget()
        self.heater_button = SCADAButton('', switch_heater, 60, 50)
        self.heater_button_proxy.setWidget(self.heater_button)
        self.scene.addItem(self.heater_button_proxy)

    def set_flow_button_text(self, text: str, disabled: bool):
        self.pump_button.setDisabled(disabled)
        self.pump_button.setText(text)

    def set_heater_button_text(self, text: str, disabled: bool):
        self.heater_button.setDisabled(disabled)
        self.heater_button.setText(text)


class FuelScheme(QGraphicsView):
    contour_changed = Signal(int)
    flow_signal = Signal(bool)
    heater_signal = Signal(bool)
    alarm_max_signal = Signal(bool)
    alarm_min_signal = Signal(bool)
    liquid_level_signal = Signal(float)

    publish_signal = Signal(str, dict)

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

        self.equipment_units = EquipmentUnits.units

        self.pipes = _PipeSystem(self.scene, self.contour_changed, self.flow_signal)
        self.valves = _ValveSystem(self.scene)
        self.pump = _Pump(self.scene, self.flow_signal)
        self.pump.obj.set_status_signal.connect(self.repaint_flow)

        self.tank = _Tank(self.scene, self.heater_signal, self.alarm_max_signal, self.alarm_min_signal)
        self.tank.obj.set_status_signal.connect(self.repaint_heater)

        self.filter = _Filter(self.scene)

        # лейблы

        # self.counter_1_label = CircleLabel('Счетчик\nчастиц 4\nРС4')
        # self.scene.addItem(self.counter_1_label)
        # self.counter_1_label.setPos(-220 * Settings.SCENE_SCALE, -260 * Settings.SCENE_SCALE)
        #
        # self.counter_2_label = CircleLabel('Счетчик\nчастиц 3\nРС3')
        # self.scene.addItem(self.counter_2_label)
        # self.counter_2_label.setPos(130 * Settings.SCENE_SCALE, -260 * Settings.SCENE_SCALE)

        self.buttons = _ButtonSystem(
            self.scene,
            self.switch_contour,
            self.switch_flow,
            self.switch_heater,
        )
        self.repaint_flow(self.flow_active)
        self.repaint_heater(self.heater_active)

        # показометры

        self.value_boxes = _ValueBoxSystem(self.scene)
        self.set_selected_contour(2)


    def wheelEvent(self, event: QWheelEvent):
        pass

    @Slot()
    def set_selected_contour(self, new_id: int):
        self.selected_contour = new_id
        self.contour_changed.emit(new_id)

    @Slot()
    def switch_flow(self):
        new_status = not self.flow_active
        bus.mqtt_publish_signal.emit(
            COMMAND_TOPIC,
            {
                'name': 'pump_1',
                'value': new_status
            }
        )
        self.buttons.set_flow_button_text('Ждем...', True)

    @Slot(bool)
    def repaint_flow(self, val):
        button_text = 'Насос\nСТОП' if val else 'Насос\nСТАРТ'
        self.flow_active = val
        self.buttons.set_flow_button_text(button_text, False)
        self.flow_signal.emit(self.flow_active)

    @Slot()
    def switch_heater(self):
        new_status = not self.heater_active
        bus.mqtt_publish_signal.emit(
            COMMAND_TOPIC,
            {
                'name': 'heater_1',
                'value': new_status
            }
        )
        self.buttons.set_heater_button_text('Ждем...', True)

    @Slot(bool)
    def repaint_heater(self, val):
        button_text = 'Нагрев\nСТОП' if val else 'Нагрев\nСТАРТ'
        self.heater_active = val
        self.buttons.set_heater_button_text(button_text, False)
        self.heater_signal.emit(self.heater_active)

    @Slot()
    def switch_contour(self):
        if not self.selected_contour:
            new_id = 1
        else:
            new_id = 2 if self.selected_contour == 1 else 1

        self.selected_contour = new_id
        self.contour_changed.emit(new_id)