from PySide6.QtCore import Qt
from PySide6.QtGui import QStandardItemModel
from PySide6.QtWidgets import QVBoxLayout, QSizePolicy, QWidget, QTableView, QLabel, QAbstractItemView, \
    QAbstractScrollArea

from app.instances.particles import PARTICLES, oil_effectiveness_dict_data
from app.ui.components.tables.cells.table_cell import Cell
from core.settings import Settings


class EffTable(QWidget):
    def __init__(
            self,
            tags=oil_effectiveness_dict_data
    ):
        super().__init__()
        self.setStyleSheet('color: black; border: 1px solid red;')

        self.tags = tags
        self.items = self.tags.get('items')

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
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
        model = QStandardItemModel(len(PARTICLES) - 2, 3)
        table.setModel(model)
        layout.addWidget(table)

        table_label = QLabel()
        table_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        table_label.setText('Диапазон')
        table_label.setStyleSheet(f'''
            border: none;
            font-size: {Settings.VALUE_BOX_VALUE_FONT_SIZE * 0.8}px;
            font-weight: bold;
            background-color: silver;
        ''')

        index = model.index(0, 0)
        table.setIndexWidget(index, table_label)

        E_label = QLabel()
        E_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        E_label.setText('E, %')
        E_label.setStyleSheet(f'''
            border: none;
            font-size: {Settings.VALUE_BOX_VALUE_FONT_SIZE * 0.8}px;
            font-weight: bold;
            background-color: silver;
            border-left: 1px solid dimgray;
        ''')

        index = model.index(0, 1)
        table.setIndexWidget(index, E_label)

        B_label = QLabel()
        B_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        B_label.setText('b')
        B_label.setStyleSheet(f'''
            border: none;
            font-size: {Settings.VALUE_BOX_VALUE_FONT_SIZE * 0.8}px;
            font-weight: bold;
            background-color: silver;
            border-left: 1px solid dimgray;
        ''')

        index = model.index(0, 2)
        table.setIndexWidget(index, B_label)

        for i, part in enumerate(self.items.items()):
            val = part[0]
            tag = part[1][0]
            tag_beta = part[1][1]

            title_label = QLabel(f'E(>{val})')
            title_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            title_label.setContentsMargins(10,0,0,0)
            title_label.setStyleSheet(f'''
                border: none;
                font-size: {Settings.VALUE_BOX_VALUE_FONT_SIZE * 0.8}px;
                font-weight: bold;
                background-color: silver;
            ''')

            index = model.index(i + 1, 0)
            table.setIndexWidget(index, title_label)

            value_label = Cell(tag)
            value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            value_label.setStyleSheet(f'''
                font-size: {Settings.VALUE_BOX_VALUE_FONT_SIZE * 0.9}px;
                border: none;
                border-left: 1px solid dimgray;
                background-color: white;
            ''')
            index = model.index(i + 1, 1)
            table.setIndexWidget(index, value_label)

            value_label_beta = Cell(tag_beta)
            # value_label_beta = QLabel(tag_beta.name)
            value_label_beta.setAlignment(Qt.AlignmentFlag.AlignCenter)
            value_label_beta.setStyleSheet(f'''
                font-size: {Settings.VALUE_BOX_VALUE_FONT_SIZE * 0.9}px;
                border: none;
                border-left: 1px solid dimgray;
                background-color: white;
            ''')
            index_beta = model.index(i + 1, 2)
            table.setIndexWidget(index_beta, value_label_beta)

        title_label = QLabel(f'Класс')
        title_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        title_label.setContentsMargins(10, 0, 0, 0)
        title_label.setStyleSheet(f'''
            border: none;
            font-size: {Settings.VALUE_BOX_VALUE_FONT_SIZE * 0.8}px;
            font-weight: bold;
            background-color: silver;
        ''')

        index = model.index(len(PARTICLES) - 3, 0)
        table.setSpan(len(PARTICLES) - 3, 1, 1, 2)
        table.setIndexWidget(index, title_label)

        value_label = Cell(self.tags.get('class').get('tag'))
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        value_label.setStyleSheet(f'''
            font-size: {Settings.VALUE_BOX_VALUE_FONT_SIZE * 0.9}px;
            border: none;
            border-left: 1px solid dimgray;
            background-color: white;
        ''')
        index = model.index(len(PARTICLES) - 3, 1)
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
        table.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        table.updateGeometry()

        return widget
