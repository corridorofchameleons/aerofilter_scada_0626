from PySide6.QtCore import Qt, QObject, Slot, Signal
from PySide6.QtGui import QWheelEvent
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QFrame, QGraphicsProxyWidget

from widgets.graphics.components.pipe import Pipe, THICK_WIDTH
from widgets.graphics.components.valve import Valve
from widgets.graphics.components.pump import Pump
from widgets.ui_widgets.button import SCADAButton


class PipeSystem(QObject):
    # contour_changed = Signal(int)

    def __init__(
            self,
            scene: QGraphicsScene,
            signal_fn_contour,
            signal_fn_flow,
            ratio: float
    ):
        super().__init__()
        self.scene = scene
        self.ratio = ratio

        self.pipes = [
            # толстые трубы нижняя часть

            Pipe(280, -50, 280, 290, horizontal=False, end_joint='right', ratio=ratio, contour=(1, 2)),
            Pipe(280, 288, -10, 288, horizontal=True, start_joint='right', ratio=ratio, contour=(1, 2)),
            Pipe(-10, 300, -300, 300, horizontal=True, end_joint='right', ratio=ratio, contour=(1, 2)),
            Pipe(-300, 300, -300, -50, horizontal=False, start_joint='right', ratio=ratio, contour=(1, 2)),

            # толстые трубы верхняя часть (контур 2)

            Pipe(-300, -50 - THICK_WIDTH, -300, -350, horizontal=False, end_joint='right', ratio=ratio, contour=(2,)),
            Pipe(-300, -350, 280, -350, horizontal=True, start_joint='right', end_joint='right', ratio=ratio, contour=(2,)),
            Pipe(280, -350, 280, -50 - THICK_WIDTH, horizontal=False, start_joint='right', ratio=ratio, contour=(2,)),
            Pipe(280, -210, 200, -210, horizontal=True, start_joint='sharp', end_joint='left', ratio=ratio, contour=(2,)),
            Pipe(200, -210, 200, -190, horizontal=False, start_joint='left', ratio=ratio, contour=(2,)),


            # тонкие трубы верхняя часть (контур 2)

            Pipe(-300, -250, -220, -250, horizontal=True, start_joint='sharp', end_joint='right',
                             ratio=ratio, thin=True, contour=(2,)),
            Pipe(-220, -250, -220, -90, horizontal=False, start_joint='right', end_joint='left',
                                         ratio=ratio, thin=True, contour=(2,)),
            Pipe(-220, -90, 280, -90, horizontal=True, start_joint='left', end_joint='sharp',
                                         ratio=ratio, thin=True, contour=(2,)),
            Pipe(280, -250, 130, -250, horizontal=True, start_joint='sharp', end_joint='left',
                                         ratio=ratio, thin=True, contour=(2,)),
            Pipe(130, -250, 130, -110, horizontal=False, start_joint='left', end_joint='left',
                                         ratio=ratio, thin=True, contour=(2,)),
            Pipe(130, -110, 280, -110, horizontal=True, start_joint='left', end_joint='sharp',
                                         ratio=ratio, thin=True, contour=(2,)),

            # толстые трубы средняя часть (контур 1)

            Pipe(-300, -50, 280, -50, horizontal=True, start_joint='sharp', end_joint='sharp', ratio=ratio, contour=(1,)),
            Pipe(-80, -50, -80, 0, horizontal=False, start_joint='sharp', ratio=ratio, contour=(1,)),
        ]

        for pipe in self.pipes:
            signal_fn_contour.connect(pipe.handle_contour_change)
            signal_fn_flow.connect(pipe.handle_flow_change)
            self.scene.addItem(pipe)

    # def set_selected_contour(self, val: int):
    #     self.selected_contour = val

    # @Slot()
    # def switch_contour(self):
    #     if not self.selected_contour:
    #         new_id = 1
    #     else:
    #         new_id = 2 if self.selected_contour == 1 else 1
    #
    #     self.selected_contour = new_id
    #     self.contour_changed.emit(new_id)


class FuelScheme(QGraphicsView):
    contour_changed = Signal(int)
    flow_signal = Signal(bool)

    def __init__(self, ratio: float, parent=None):
        super().__init__(parent)
        self.ratio = ratio

        self.selected_contour = None
        self.flow_active = False

        # конфига

        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setObjectName('fuelScheme')
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # Отключаем горизонтальный скролл
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setDragMode(QGraphicsView.NoDrag)

        self.scene = QGraphicsScene()
        self.setScene(self.scene)

        # сеть труб

        self.pipes = PipeSystem(self.scene, self.contour_changed, self.flow_signal, self.ratio)

        # помпа

        self.pump = Pump(self.ratio, self.flow_signal, -20, 300)
        self.scene.addItem(self.pump)

        # кнопки

        switch_button_proxy = QGraphicsProxyWidget()
        self.switch_button = SCADAButton('Режим\nиспытания', self.switch_contour, -310, 340)
        switch_button_proxy.setWidget(self.switch_button)
        self.scene.addItem(switch_button_proxy)

        pump_button_proxy = QGraphicsProxyWidget()
        self.pump_button = SCADAButton('', self.switch_flow, 40, 210)
        self._set_flow_button_text()
        pump_button_proxy.setWidget(self.pump_button)
        self.scene.addItem(pump_button_proxy)

        # self.valve = Valve(self.ratio, 100, 100)
        # self.pump = Pump(
        #     self.ratio, -150, 220
        # )
        # self.pipe1 = PipeBody(0, 0, 0, 200, horizontal=False)


        # self.scene.addItem(self.valve)

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
