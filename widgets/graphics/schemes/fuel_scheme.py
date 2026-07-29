from PySide6.QtCore import Qt, QObject, Slot, Signal
from PySide6.QtGui import QWheelEvent
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QFrame, QGraphicsProxyWidget

from widgets.graphics.components.pipe import Pipe, THICK_WIDTH
from widgets.graphics.components.valve import Valve
from widgets.graphics.components.pump import Pump
from widgets.ui_widgets.button import SCADAButton


class PipeSystem(QObject):
    contour_changed = Signal(int)

    def __init__(
            self,
            scene: QGraphicsScene,
            ratio: float
    ):
        super().__init__()
        self.scene = scene
        self.ratio = ratio

        self.pipes = [
            # толстые трубы нижняя часть

            Pipe(280, -50, 280, 280, horizontal=False, end_joint='right', ratio=ratio, contour=(1, 2)),
            Pipe(280, 280, -10, 280, horizontal=True, start_joint='right', ratio=ratio, contour=(1, 2)),
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
            self.contour_changed.connect(pipe.handle_contour_change)
            self.scene.addItem(pipe)

        self.selected_contour = None

    def set_selected_contour(self, val: int):
        self.selected_contour = val

    @Slot()
    def switch_contour(self):
        if not self.selected_contour:
            new_id = 1
        else:
            new_id = 2 if self.selected_contour == 1 else 1

        self.selected_contour = new_id
        self.contour_changed.emit(new_id)


class FuelScheme(QGraphicsView):
    def __init__(self, ratio: float, parent=None):
        super().__init__(parent)
        self.ratio = ratio
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setObjectName('fuelScheme')

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # Отключаем горизонтальный скролл
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setDragMode(QGraphicsView.NoDrag)

        self.scene = QGraphicsScene()
        self.setScene(self.scene)

        self.pipes = PipeSystem(self.scene, self.ratio)
        self.pipes.set_selected_contour(2)

        proxy = QGraphicsProxyWidget()
        self.switch_button = SCADAButton('Режим испытания', self.pipes.switch_contour, -310, 350)
        proxy.setWidget(self.switch_button)
        self.scene.addItem(proxy)

        # self.valve = Valve(self.ratio, 100, 100)
        # self.pump = Pump(
        #     self.ratio, -150, 220
        # )
        # self.pipe1 = PipeBody(0, 0, 0, 200, horizontal=False)


        # self.scene.addItem(self.valve)


    def wheelEvent(self, event: QWheelEvent):
        pass
