from PySide6.QtCore import Slot
from PySide6.QtWidgets import QWidget, QVBoxLayout, QGraphicsView, QSizePolicy
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from widgets.settings import Settings


class PressureDiffGraph(QWidget):
    def __init__(self):
        super().__init__()

        self.x_range = 60

        self.figure = Figure(facecolor=Settings.GRAPH_BACKGROUND_COLOR)
        self.figure.patch.set_alpha(1.0)
        self.canvas = FigureCanvas(self.figure)

        self.ax_left = self.figure.add_subplot(111)
        self.ax_left.spines['top'].set_visible(False)
        self.ax_left.set_ylabel('Расход топлива, л/мин')
        self.ax_left.grid(True, alpha=0.3)
        self.ax_left.set_facecolor('none')
        self.ax_left.set_ylim(bottom=0, top=10)
        self.ax_left.spines['left'].set_color(Settings.GRAPH_LINE_1_COLOR)
        self.ax_left.tick_params(axis='y', colors=Settings.GRAPH_LINE_1_COLOR)
        self.ax_left.yaxis.label.set_color(Settings.GRAPH_LINE_1_COLOR)

        self.ax_left.spines['bottom'].set_color(Settings.GRAPH_BOTTOM_LINE_COLOR)
        self.ax_left.tick_params(axis='x', colors=Settings.GRAPH_BOTTOM_LINE_COLOR)
        self.ax_left.set_xlabel('Время, с')
        self.ax_left.xaxis.label.set_color(Settings.GRAPH_BOTTOM_LINE_COLOR)

        self.ax_right = self.ax_left.twinx()
        self.ax_right.spines['left'].set_visible(False)
        self.ax_right.spines['bottom'].set_visible(False)
        self.ax_right.spines['top'].set_visible(False)
        self.ax_right.set_ylabel('Перепад давления, МПа')
        self.ax_right.set_facecolor('none')
        self.ax_right.set_ylim(bottom=0, top=10)
        self.ax_right.spines['right'].set_color(Settings.GRAPH_LINE_2_COLOR)
        self.ax_right.tick_params(axis='y', colors=Settings.GRAPH_LINE_2_COLOR)
        self.ax_right.yaxis.label.set_color(Settings.GRAPH_LINE_2_COLOR)

        self.ax_left.set_xlim(-self.x_range, 0)

        x_data = [-60, -50, -40, -30, -20, -10, 0]
        y1_data = [0, 1, 2, 3, 4, 5, 6]
        y2_data = [6, 5, 4, 3, 2, 1, 0]

        self.ax_left.plot(x_data, y1_data, color=Settings.GRAPH_LINE_1_COLOR, linewidth=2, antialiased=True)
        self.ax_right.plot(x_data, y2_data, color=Settings.GRAPH_LINE_2_COLOR, linewidth=2, antialiased=True)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.canvas)
        self.setLayout(self.layout)

    @Slot(int)
    def set_x_range(self, val):
        self.x_range = val
