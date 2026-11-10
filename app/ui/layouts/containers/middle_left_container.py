from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QStackedWidget, QLabel

from app.instances.stands import OilStand, FuelStand
from app.ui.components.tables.telemetry_table import TelemetryTable


class LeftMiddleContainer(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

        self.side_table_stack = QStackedWidget()

        self.oil_telemetry_table = TelemetryTable(OilStand.num, 'Масляный стенд')
        self.fuel_telemetry_table = TelemetryTable(FuelStand.num, 'Топливный стенд')

        self.side_table_stack.addWidget(self.oil_telemetry_table)
        self.side_table_stack.addWidget(self.fuel_telemetry_table)
        self.side_table_stack.addWidget(QWidget())

        self.layout.addWidget(self.side_table_stack)
        self.setLayout(self.layout)