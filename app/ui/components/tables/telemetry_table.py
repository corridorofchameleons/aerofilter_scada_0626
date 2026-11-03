from PySide6.QtCore import Qt
from PySide6.QtGui import QStandardItemModel
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableView, QLabel, QAbstractItemView, QAbstractScrollArea, \
    QSizePolicy

from app.instances.stands import OilStand, FuelStand
from app.ui.components.tables.cells.table_cell import Cell
from core.settings import Settings


class TelemetryTable(QWidget):
    def __init__(
            self,
            stand_num
    ):
        super().__init__()
        self.setStyleSheet('color: black; border: 1px solid red;')

        self.index = stand_num - 1

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.setLayout(self.layout)

        self.cell_width = 120
        self.cell_height = 20

        self.data = [
            ('Давление до, МПа', (OilStand.oil_pressure_before, FuelStand.fuel_pressure_before)),
            ('Давление после, МПа', (OilStand.oil_pressure_after, FuelStand.fuel_pressure_after)),
            ('Темп. до, С', (OilStand.oil_temperature_before, FuelStand.fuel_temperature_before)),
            ('Темп. после, С', (OilStand.oil_temperature_after, FuelStand.fuel_temperature_after)),
        ]

        self.table = self.compose_table()
        self.layout.addWidget(self.table)

    def compose_table(self):

        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        widget.setLayout(layout)

        table = QTableView()
        model = QStandardItemModel(len(self.data), 2)
        table.setModel(model)

        layout.addWidget(table)

        for i, el in enumerate(self.data):

            title_label = QLabel(el[0])
            title_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            title_label.setContentsMargins(5, 0, 0, 0)
            title_label.setStyleSheet(f'''
                            border: none;
                            font-size: {Settings.VALUE_BOX_VALUE_FONT_SIZE * 0.8}px;
                            font-weight: bold;
                            background-color: silver;
                        ''')

            index = model.index(i, 0)
            table.setIndexWidget(index, title_label)
            table.horizontalHeader().resizeSection(1, 70)

            value_label = Cell(el[1][self.index])

            value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            value_label.setStyleSheet(f'''
                            font-size: {Settings.VALUE_BOX_VALUE_FONT_SIZE * 0.9}px;
                            border: none;
                            border-left: 1px solid dimgray;
                            background-color: white;
                        ''')
            index = model.index(i, 1)
            table.setIndexWidget(index, value_label)

        table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        table.setStyleSheet('''
            background-color: lightgray; 
            border: 2px solid dimgray;
        ''')
        table.verticalHeader().setVisible(False)
        table.horizontalHeader().setVisible(False)
        table.verticalHeader().setDefaultSectionSize(self.cell_height)
        table.verticalHeader().setStretchLastSection(False)
        table.horizontalHeader().setDefaultSectionSize(self.cell_width)
        table.horizontalHeader().setStretchLastSection(False)

        table.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        table.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        table.updateGeometry()

        return widget
