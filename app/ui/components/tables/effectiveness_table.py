from PySide6.QtCore import Qt
from PySide6.QtGui import QStandardItemModel
from PySide6.QtWidgets import QVBoxLayout, QSizePolicy, QWidget, QTableView, QLabel, QAbstractItemView, \
    QAbstractScrollArea

from app.instances.particles import PARTICLES, oil_effectiveness_dict_data
from core.widgets.ui_widgets.particle_table_cell import Cell
from core.settings import Settings


class EffTable(QWidget):
    def __init__(
            self,
            tags=oil_effectiveness_dict_data
    ):
        super().__init__()
        self.setContentsMargins(0,0,0,0)
        self.setStyleSheet('color: black; border: 1px solid red;')

        self.tags = tags

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
        self.setLayout(self.layout)

        self.cell_width = 70
        self.cell_height = 20

        self.table = self.compose_table()
        self.layout.addWidget(self.table)

    def compose_table(self):

        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        widget.setLayout(layout)

        table = QTableView()
        model = QStandardItemModel(len(PARTICLES) - 1, 2)
        table.setModel(model)

        table_label = QLabel()
        table_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        table_label.setText('Расчет эффективности, %')
        table_label.setStyleSheet(f'''
            border: 2px solid dimgray;
            border-bottom: none;
            font-size: {Settings.VALUE_BOX_VALUE_FONT_SIZE * 0.8}px;
            font-weight: bold;
            background-color: silver;
        ''')
        table_label.setFixedSize(self.cell_width * 2 + 4, int(self.cell_height * 1.2))

        layout.addWidget(table_label)
        layout.addWidget(table)

        for i, part in enumerate(self.tags.items()):
            val = part[0]
            tag = part[1]
            if not isinstance(val, int):
                continue
            title_label = QLabel(f'E(>{val})')
            title_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            title_label.setContentsMargins(10,0,0,0)
            title_label.setStyleSheet(f'''
                border: none;
                font-size: {Settings.VALUE_BOX_VALUE_FONT_SIZE * 0.8}px;
                font-weight: bold;
                background-color: silver;
            ''')

            index = model.index(i, 0)
            table.setIndexWidget(index, title_label)

            value_label = Cell(tag)
            value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            value_label.setStyleSheet(f'''
                font-size: {Settings.VALUE_BOX_VALUE_FONT_SIZE * 0.9}px;
                border: none;
                border-left: 1px solid dimgray;
                background-color: white;
            ''')
            index = model.index(i, 1)
            table.setIndexWidget(index, value_label)

        # for col in range(2):
        #     if col <= 0:
        #     table.horizontalHeader().resizeSection(col, 70)
        #     label = QLabel('Расчет эффективности')
        #     label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        #     label.setStyleSheet(f'''
        #         border: none;
        #         font-size: {Settings.VALUE_BOX_VALUE_FONT_SIZE * 0.8}px;
        #         font-weight: bold;
        #         background-color: silver;
        #     ''')
        #
        #     index = model.index(0, col)
        #     table.setIndexWidget(index, label)
        #
        #     for i, val in enumerate(PARTICLES):
        #         label_text = f'>{val} мкм' if isinstance(val, int) else 'Класс'
        #         label = QLabel(label_text)
        #         label.setContentsMargins(5, 0, 0, 0)
        #         label.setStyleSheet(f'''
        #             border: none;
        #             font-size: {Settings.VALUE_BOX_VALUE_FONT_SIZE * 0.8}px;
        #             background-color: silver;
        #         ''')
        #         index = model.index(i + 1, col)
        #         table.setIndexWidget(index, label)

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
        table.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        table.updateGeometry()

        return widget