from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QStackedWidget

from app.instances.particles import oil_effectiveness_dict_data, fuel_effectiveness_dict_data
from app.ui.components.tables.effectiveness_table import EffTable


class RightMiddleContainer(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)

        self.side_table_stack = QStackedWidget()

        self.oil_eff_table = EffTable(
            tags=oil_effectiveness_dict_data
        )

        self.fuel_eff_table = EffTable(
            tags=fuel_effectiveness_dict_data
        )

        self.side_table_stack.addWidget(self.oil_eff_table)
        self.side_table_stack.addWidget(self.fuel_eff_table)
        self.side_table_stack.addWidget(QWidget())

        self.layout.addWidget(self.side_table_stack)
        self.setLayout(self.layout)
