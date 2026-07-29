from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPainter, QPen, QColor, QWheelEvent
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QGraphicsView, QGraphicsScene

from widgets.scheme.components.pipe import PipeBody, Pipe
from widgets.scheme.components.valve import Valve
from widgets.scheme.components.pump import Pump

WIDGET_SIZE: tuple[int, int] = 1500, 800

class Scheme(QGraphicsView):
    def __init__(self, parent=None, ratio=1.2):
        super().__init__(parent)
        self.ratio = ratio
        self.setFixedSize(WIDGET_SIZE[0], WIDGET_SIZE[1])
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setObjectName('schemeView')

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # Отключаем горизонтальный скролл
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setDragMode(QGraphicsView.NoDrag)

        self.scene = QGraphicsScene()
        self.setScene(self.scene)

        self.valve = Valve(self.ratio, 100, 100)
        self.pump = Pump(
            self.ratio, -150, 220
        )
        # self.pipe1 = PipeBody(0, 0, 0, 200, horizontal=False)

        self.pipe2 = Pipe(0, 205, -150, 205, horizontal=True, start_joint='right')
        self.pipe2_1 = Pipe(-150, 220, -300, 220, horizontal=True, end_joint='right')
        self.pipe4 = Pipe(-300, 220, -300, 0, horizontal=False, start_joint='right', end_joint='right')
        self.pipe3 = Pipe(-300, 0, 0, 0, horizontal=True, start_joint='right', end_joint='right')
        self.pipe5 = Pipe(0, 0, 0, 205, horizontal=False, start_joint='right', end_joint='right')
        #
        # self.pipe6 = PipeBody(-300, 100, 0, 100, horizontal=True, start_joint='sharp', end_joint='sharp')


        # self.pipe4 = PipeBody(-300, 100, -200, 100, horizontal=True, start_joint = 'sharp')
        # self.pipe5 = PipeBody(-300, 0, -200, 0, horizontal=True, start_joint = 'right')
        # self.pipe_thin = PipeBody(-300, 50, -200, 50, horizontal=True, thin=True, start_joint='sharp')
        # self.pipe_thin_2 = PipeBody(-200, 50, -200, 30, horizontal=False, thin=True, start_joint='left')

        # self.pipe2.set_selected(True)
        # self.pipe2_1.set_selected(True)
        self.pipe3.set_selected(True)
        # self.pipe4.set_selected(True)
        # self.pipe5.set_selected(True)
        # self.pipe2.start_flow()
        # self.pipe2_1.start_flow()
        self.pipe3.start_flow()
        # self.pipe4.start_flow()
        # self.pipe5.start_flow()
        # self.pipe_thin_2.set_selected(True)


        # self.scene.addItem(self.valve)

        # self.scene.addItem(self.pipe1)

        self.scene.addItem(self.pipe2)
        self.scene.addItem(self.pipe2_1)
        self.scene.addItem(self.pipe3)
        self.scene.addItem(self.pipe4)
        self.scene.addItem(self.pipe5)
        # self.scene.addItem(self.pipe6)
        #
        # self.scene.addItem(self.pump)
        # self.pump.rotate()
        #
        # self.scene.addItem(self.pipe3)
        # self.scene.addItem(self.pipe4)
        # self.scene.addItem(self.pipe5)
        # self.scene.addItem(self.pipe_thin)
        # self.scene.addItem(self.pipe_thin_2)


    def wheelEvent(self, event: QWheelEvent):
        pass


