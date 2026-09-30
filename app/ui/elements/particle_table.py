from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QStandardItemModel
from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout, QSizePolicy, QTableView, QAbstractScrollArea, \
    QAbstractItemView, QVBoxLayout

from app.instances.particles import PARTICLES
from app.ui.elements.particle_table_cell import Cell
from core.models.tag import IntTag
from core.settings import Settings

class PartTable(QWidget):
    def __init__(
            self,
            num_tag: IntTag,
            tags: dict,
            index_before_tag: IntTag,
            index_after_tag: IntTag
    ):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        self.setContentsMargins(0,0,0,0)
        self.setStyleSheet('color: black;')

        self.tags = tags
        self.num_tag = num_tag
        if self.num_tag:
            self.num_tag.update_ui.connect(self.compose_table)

        self.index_before_tag = index_before_tag
        self.index_after_tag = index_after_tag

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.setLayout(self.layout)

        self.table = QWidget()
        self.compose_table()

    def compose_table(self):
        cols = self.num_tag.value
        if cols is None:
            cols = 0

        self.layout.removeWidget(self.table)
        self.table.deleteLater()

        table = QTableView()
        model = QStandardItemModel(len(PARTICLES) + 1, cols * 2 + 1)
        table.setModel(model)

        for col in range(cols + 1):
            if col <= 0:
                table.horizontalHeader().resizeSection(col, 70)
                label = QLabel('Диапазон')
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                label.setStyleSheet(f'''
                    border: none;
                    font-size: {Settings.VALUE_BOX_VALUE_FONT_SIZE * 0.8}px;
                    font-weight: bold;
                    background-color: silver;
                ''')

                index = model.index(0, col)
                table.setIndexWidget(index, label)

                for i, val in enumerate(PARTICLES):
                    label_text = f'>{val} мкм' if isinstance(val, int) else 'Класс'
                    label = QLabel(label_text)
                    label.setContentsMargins(5, 0, 0, 0)
                    label.setStyleSheet(f'''
                        border: none;
                        font-size: {Settings.VALUE_BOX_VALUE_FONT_SIZE * 0.8}px;
                        background-color: silver;
                    ''')
                    index = model.index(i + 1, col)
                    table.setIndexWidget(index, label)

            else:
                before_label = QLabel(f'ДО {col}')
                before_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                before_label.setStyleSheet(f'''
                       font-size: {Settings.VALUE_BOX_VALUE_FONT_SIZE * 0.8}px;
                       font-weight: bold;
                       font-style: italic;
                       background-color: silver;
                       border: none;
                       border-left: 1px solid dimgray;
                    ''')
                after_label = QLabel(f'ПОСЛЕ {col}')
                after_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                after_label.setStyleSheet(f'''
                       font-size: {Settings.VALUE_BOX_VALUE_FONT_SIZE * 0.8}px;
                       font-weight: bold;
                       font-style: italic;
                       background-color: silver;
                       border: none;
                    ''')

                index_before = model.index(0, col * 2 - 1)
                table.setIndexWidget(index_before, before_label)
                index_after = model.index(0, col * 2)
                table.setIndexWidget(index_after, after_label)

                col_tags = self.tags.get(col)
                for i, val in enumerate(PARTICLES):
                    tag_couple = col_tags.get(val)
                    tag_couple_list = list(tag_couple.values())

                    before_value_label = Cell(tag_couple_list[0])
                    before_value_label.setStyleSheet(f'''
                        font-size: {Settings.VALUE_BOX_VALUE_FONT_SIZE * 0.9}px;
                        border: none;
                        border-left: 1px solid dimgray;
                        background-color: white;
                    ''')

                    after_value_label = Cell(tag_couple_list[1])
                    after_value_label.setStyleSheet(f'''
                        font-size: {Settings.VALUE_BOX_VALUE_FONT_SIZE * 0.9}px;
                        border: none;
                        background-color: white;
                    ''')

                    index_before = model.index(i + 1, col * 2 - 1)
                    table.setIndexWidget(index_before, before_value_label)
                    index_after = model.index(i + 1, col * 2)
                    table.setIndexWidget(index_after, after_value_label)

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
        table.verticalHeader().setDefaultSectionSize(16)
        table.verticalHeader().setStretchLastSection(False)
        table.horizontalHeader().setDefaultSectionSize(55)
        table.horizontalHeader().setStretchLastSection(False)

        table.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        table.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        table.updateGeometry()
        self.table = table
        self.layout.addWidget(self.table)
