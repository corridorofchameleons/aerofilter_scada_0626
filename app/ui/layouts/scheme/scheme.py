from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtGui import QWheelEvent
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsProxyWidget

from app.ui.layouts.scheme.systems.borders import BorderRectangles
from app.ui.layouts.scheme.systems.filters import FilterSystem
from app.ui.layouts.scheme.systems.headers import SchemeHeaders
from app.ui.layouts.scheme.systems.lamps import LampSystem
from app.ui.layouts.scheme.systems.pipes import PipeSystem
from app.ui.layouts.scheme.systems.pumps import PumpSystem
from app.ui.layouts.scheme.systems.rotameters import RotameterSystem
from app.ui.layouts.scheme.systems.tanks import TankSystem
from app.ui.layouts.scheme.systems.value_boxes import ValueBoxSystem
from app.ui.layouts.scheme.systems.value_inputs import ValueInputSystem
from app.ui.layouts.scheme.systems.valves import ValveSystem
from core.widgets.graphics.components.particle_counter import ParticleCounter
from app.ui.layouts.scheme.scheme_layout import START_X, START_Y, WIDTH, HEIGHT, COUNTER_X, COUNTER_Y, SWITCH_X, SWITCH_Y, \
    STAND_BORDER_HEIGHT
from core.widgets.ui_widgets.button import MenuButton, BaseButton


class Scheme(QGraphicsView):
    set_active_contours = Signal(set)
    handle_contour_status = Signal(int, bool)

    switch_flow_signal = Signal(set, bool)
    activate_flow = Signal(set, bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setObjectName('scheme')

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)

        self.scene = QGraphicsScene()
        self.scene.setSceneRect(START_X - 10, START_Y, WIDTH + 20, HEIGHT)
        self.setScene(self.scene)

        self.handle_contour_status.connect(self.change_contour_status)

        self.active_contours = {1, 4, 7, 10}
        self.flow_1_active = False
        self.flow_2_active = False

        self.scheme_borders = BorderRectangles(self.scene)
        self.scheme_headers = SchemeHeaders(self.scene)

        self.pipe_system = PipeSystem(self.scene, self.set_active_contours, self.activate_flow)
        self.valve_system = ValveSystem(
            self.scene,
            self.set_active_contours,
            handle_status_signal=self.handle_contour_status
        )

        self.pump_system = PumpSystem(self.scene, self.switch_flow_signal)
        self.tank_system = TankSystem(self.scene)
        self.filter_system = FilterSystem(self.scene)
        self.rotameter_system = RotameterSystem(self.scene)

        self.value_boxes = ValueBoxSystem(self.scene)
        self.value_inputs = ValueInputSystem(self.scene)

        self.lamps = LampSystem(self.scene)

        self.particle_counter = ParticleCounter()
        self.particle_counter.setPos(COUNTER_X, COUNTER_Y)
        self.scene.addItem(self.particle_counter)

        self.choose_button = MenuButton('Выбор\nстенда', size=1)
        self.choose_button_proxy = QGraphicsProxyWidget()
        self.choose_button_proxy.setWidget(self.choose_button)
        self.choose_button_proxy.setPos(SWITCH_X - BaseButton.Size.NORMAL * 0.5, SWITCH_Y + STAND_BORDER_HEIGHT * 0.5 - self.choose_button.height() * 0.22)
        self.scene.addItem(self.choose_button_proxy)

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
        if contour in self.active_contours:
            self.active_contours.remove(contour)
        self.set_active_contours.emit(self.active_contours)
