from PySide6.QtCore import Slot
from PySide6.QtWidgets import QWidget, QVBoxLayout, QGraphicsView, QSizePolicy
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from objects.graph_data import GraphData
from widgets.settings import Settings


class PressureDiffGraph(QWidget):
    def __init__(self):
        super().__init__()
        self.pres_buffer = GraphData.units.get('pressure_diff_1')
        self.pres_diff_data = self.pres_buffer.buffer
        self.pres_buffer.update_graph_signal.connect(self.update_pres_diff_plot)

        self.fuel_buffer = GraphData.units.get('fuel_consumption_1')
        self.fuel_buffer_data = self.fuel_buffer.buffer
        self.fuel_buffer.update_graph_signal.connect(self.update_fuel_plot)

        self.x_range = 120

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

        self.ax_left.set_xlim(-int(self.x_range / 2), 0)
        # self.ax_right.set_xlim(-int(self.x_range / 2), 0)

        self.line_fuel, = self.ax_left.plot([], [], color=Settings.GRAPH_LINE_1_COLOR)
        self.line_pres, = self.ax_right.plot([], [], color=Settings.GRAPH_LINE_2_COLOR)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.canvas)
        self.setLayout(self.layout)

    @Slot(int)
    def set_x_range(self, val):
        self.x_range = val

    @Slot()
    def update_pres_diff_plot(self):
        x_data = [i for i in range(-self.x_range, 1)]
        y_data = [0 for _ in range(-self.x_range, 1)]
        data_range = len(self.pres_diff_data) if len(self.pres_diff_data) < len(y_data) else len(y_data) + 1
        for i in range(-1, -data_range, -1):
            y_data[i] = self.pres_diff_data[i].val

        self.ax_right.set_ylim(bottom=0, top=max(y_data))
        self.line_pres.set_data(x_data, y_data)
        self.canvas.draw_idle()

    @Slot()
    def update_fuel_plot(self):
        x_data = [i for i in range(-self.x_range, 1)]
        y_data = [0 for _ in range(-self.x_range, 1)]
        data_range = len(self.fuel_buffer_data) if len(self.fuel_buffer_data) < len(y_data) else len(y_data) + 1
        for i in range(-1, -data_range, -1):
            y_data[i] = self.fuel_buffer_data[i].val

        self.ax_left.set_ylim(bottom=0, top=max(y_data))
        self.line_fuel.set_data(x_data, y_data)
        self.canvas.draw_idle()
