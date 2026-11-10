from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QStandardItemModel
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableView, QLabel, QAbstractItemView, QAbstractScrollArea, \
    QSizePolicy, QHBoxLayout

from app.instances.stands import OilStand, FuelStand
from app.ui.components.tables.cells.table_cell import Cell
from core.settings import Settings
from core.widgets.ui_widgets.value_input import ValueInput


class TelemetryTable(QWidget):
    def __init__(
            self,
            stand_num: int,
            title: str
    ):
        super().__init__()
        self.setStyleSheet('color: black;')

        self.index = stand_num - 1

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.setLayout(self.layout)

        self.title = QLabel(title)
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.title)

        self.cell_width = 120
        self.cell_height = 40

        self.data = [
            ('Текущий расход\nжидкости, л³/мин', (OilStand.oil_flow_meter, FuelStand.fuel_flow_meter)),
            ('Перепад\nдавления, Па', (OilStand.oil_pressure_diff, FuelStand.fuel_pressure_diff)),
            ('Температура\nв баке, °C', (OilStand.oil_tank_temperature, FuelStand.fuel_tank_temperature)),
            # ('Темп. после, С', (OilStand.oil_temperature_after, FuelStand.fuel_temperature_after)),
        ]

        self.flow_tag = OilStand.oil_set_flow if stand_num == 1 else FuelStand.fuel_set_flow
        self.expected_flow_tag = OilStand.oil_set_expected_flow if stand_num == 1 else FuelStand.fuel_set_expected_flow

        self.table = self.compose_table()

        self.flow_value_input = ValueInput(
            tag = self.flow_tag,
            title = 'Заданный\nрасход',
            width=100,
            height=55,
            scada=False
        )
        self.expected_flow_value_input = ValueInput(
            tag = self.expected_flow_tag,
            title = 'Ожидаемый\nрасход',
            width=100,
            height=55,
            scada=False
        )

        self.container = QWidget()
        self.container_layout = QHBoxLayout()

        self.value_input_block = QWidget()
        self.value_input_block_layout = QVBoxLayout()
        self.value_input_block_layout.addWidget(self.flow_value_input)
        self.value_input_block_layout.setContentsMargins(0,0,0,0)
        self.value_input_block_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.value_input_block_layout.addWidget(self.expected_flow_value_input)
        self.value_input_block.setLayout(self.value_input_block_layout)

        self.container_layout.addWidget(self.table)
        self.container_layout.addWidget(self.value_input_block)
        self.container_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.container.setLayout(self.container_layout)

        self.layout.addWidget(self.container)


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
                            font-size: {Settings.VALUE_BOX_VALUE_FONT_SIZE}px;
                            font-weight: bold;
                            background-color: silver;
                        ''')

            index = model.index(i, 0)
            table.setIndexWidget(index, title_label)
            table.horizontalHeader().resizeSection(1, 70)

            value_label = Cell(el[1][self.index])

            value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            value_label.setStyleSheet(f'''
                            font-size: {Settings.VALUE_BOX_VALUE_FONT_SIZE}px;
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

    @Slot(bool)
    def switch_value_input(self, val: bool):
        if val:
            self.flow_value_input.hide()
            self.expected_flow_value_input.show()
        else:
            self.expected_flow_value_input.hide()
            self.flow_value_input.show()
