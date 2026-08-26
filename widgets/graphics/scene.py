from PySide6.QtGui import QWheelEvent
from PySide6.QtWidgets import QWidget, QHBoxLayout

from widgets.graphics.layouts.scheme_layout import START_X, START_Y, WIDTH, HEIGHT
from widgets.graphics.schemes.fuel_scheme import FuelScheme
from widgets.graphics.schemes.oil_scheme import OilScheme
from widgets.graphics.schemes.scheme import Scheme
from widgets.settings import Settings


class Scene(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFixedSize(Settings.SCENE_SIZE[0] + 40, Settings.SCENE_SIZE[1] + 40)

        self.layout = QHBoxLayout(self)

        # self.fuel_scheme = FuelScheme()
        # self.fuel_scheme.setSceneRect(-WIDGET_SIZE[0] / 2, -WIDGET_SIZE[1] / 2, *WIDGET_SIZE)
        # self.fuel_scheme.setFixedSize(*WIDGET_SIZE)
        #
        # self.oil_scheme = OilScheme()
        # self.oil_scheme.setSceneRect(-WIDGET_SIZE[0] / 2, -WIDGET_SIZE[1] / 2, *WIDGET_SIZE)
        # self.oil_scheme.setFixedSize(*WIDGET_SIZE)

        # layout.addWidget(self.fuel_scheme)
        # layout.addWidget(self.oil_scheme)

        self.scheme = Scheme()

        self.layout.addWidget(self.scheme)
