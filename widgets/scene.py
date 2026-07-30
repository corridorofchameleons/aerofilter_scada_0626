from PySide6.QtWidgets import QWidget, QHBoxLayout

from widgets.graphics.schemes.fuel_scheme import FuelScheme
from widgets.graphics.schemes.oil_scheme import OilScheme

WIDGET_SIZE: tuple[int, int] = 700, 800

class Scene(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFixedSize(WIDGET_SIZE[0] * 2 + 15, WIDGET_SIZE[1] + 15)

        layout = QHBoxLayout(self)

        self.fuel_scheme = FuelScheme()
        self.fuel_scheme.setSceneRect(-WIDGET_SIZE[0] / 2, -WIDGET_SIZE[1] / 2, *WIDGET_SIZE)
        self.fuel_scheme.setFixedSize(*WIDGET_SIZE)

        self.oil_scheme = OilScheme()
        self.oil_scheme.setSceneRect(-WIDGET_SIZE[0] / 2, -WIDGET_SIZE[1] / 2, *WIDGET_SIZE)
        self.oil_scheme.setFixedSize(*WIDGET_SIZE)

        layout.addWidget(self.fuel_scheme)
        layout.addWidget(self.oil_scheme)
