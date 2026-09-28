from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QSizePolicy

from app.instances.particles import PARTICLES, TEST_NUM
from app.ui.elements.particle_table_cell import Cell
from core.models.tag import IntTag
from core.settings import Settings


class ParticleTable(QWidget):
    def __init__(
            self,
            num_tag: IntTag,
            tags: dict,
    ):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.tags = tags
        self.num_tag = num_tag

        self.num_tag.update_value.connect(self.update_col_num)

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.setStyleSheet('''
            color: black;
        ''')
        self.layout.setSpacing(0)

        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.cell_width = 55
        self.setLayout(self.layout)

        self.table = QWidget()

    def compose_table(self):
        self.layout.removeWidget(self.table)
        self.table.deleteLater()
        table = QWidget()
        # table.setStyleSheet('border: 1px solid green;')
        table.setContentsMargins(0,0,0,0)
        table.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        table_layout = QHBoxLayout()
        table_layout.setSpacing(2)
        table_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        for i in range(self.num_tag.value + 1):
            col_widget = QWidget()
            col_widget.setFixedWidth(self.cell_width * 2)
            col_widget.setObjectName('columnWidget')
            col_layout = QVBoxLayout()
            col_layout.setSpacing(0)
            col_layout.setContentsMargins(0, 0, 0, 0)
            col_widget.setStyleSheet('''
                border: 1px solid dimgray;
            ''')
            col_widget.setLayout(col_layout)

            if i <= 0:
                label = QLabel('Диапазон')
                label.setFocusPolicy(Qt.FocusPolicy.NoFocus)
                label.setFixedHeight(20)
                label.setStyleSheet(f'''
                   border: 1px solid dimgray;
                   font-size: {Settings.VALUE_BOX_VALUE_FONT_SIZE * 0.8}px;
                   font-weight: bold;
                   background-color: silver;
                ''')
                col_layout.addWidget(label, stretch=1)

                for val in PARTICLES:
                    label_text = f'>{val} мкм' if isinstance(val, int) else 'Класс'
                    label = QLabel(label_text)
                    label.setStyleSheet(f'''
                       border: 1px solid dimgray;
                       font-size: {Settings.VALUE_BOX_VALUE_FONT_SIZE * 0.8}px;
                       background-color: silver;
                       border-top: none;
                    ''')
                    col_layout.addWidget(label, stretch=1)
            else:
                couple_widget = QWidget()
                couple_widget.setFixedHeight(20)
                layout = QHBoxLayout()
                layout.setSpacing(0)
                layout.setContentsMargins(0, 0, 0, 0)
                couple_widget.setLayout(layout)

                before_label = QLabel(f'ДО {i}')
                before_label.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignCenter)
                before_label.setStyleSheet(f'''
                       border: 1px solid dimgray;
                       font-size: {Settings.VALUE_BOX_VALUE_FONT_SIZE * 0.8}px;
                       font-weight: bold;
                       font-style: italic;
                       background-color: silver;
                       border-right: none;
                    ''')
                before_label.setFixedWidth(self.cell_width)
                layout.addWidget(before_label, stretch=1)
                after_label = QLabel(f'ПОСЛЕ {i}')
                after_label.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignCenter)
                after_label.setStyleSheet(f'''
                       border: 1px solid dimgray;
                       font-size: {Settings.VALUE_BOX_VALUE_FONT_SIZE * 0.8}px;
                       font-weight: bold;
                       font-style: italic;
                       background-color: silver;
                       border-right: 1px solid dimgray;
                    ''')
                after_label.setFixedWidth(self.cell_width)
                layout.addWidget(before_label, stretch=1)
                layout.addWidget(after_label, stretch=1)
                col_layout.addWidget(couple_widget, stretch=1)

                col_tags = self.tags.get(i)
                for val in PARTICLES:
                    couple_widget = QWidget()
                    layout = QHBoxLayout()
                    layout.setSpacing(0)
                    layout.setContentsMargins(0, 0, 0, 0)
                    couple_widget.setLayout(layout)
                    tag_couple = col_tags.get(val)
                    for j, tag in enumerate(tag_couple.values()):
                        value_label = Cell(tag)
                        value_label.setFixedWidth(self.cell_width)
                        value_label.setReadOnly(True)
                        value_label.setStyleSheet(f'''
                            font-size: {Settings.VALUE_BOX_VALUE_FONT_SIZE * 0.9}px;
                            border: 1px solid dimgray;
                            background-color: white;
                            border-top: none;
                           {'border-right: none;' if j < 1 else 'border-right: 1px solid dimgray;'}
                        ''')
                        layout.addWidget(value_label, stretch=1)
                    col_layout.addWidget(couple_widget, stretch=1)
            table_layout.addWidget(col_widget, stretch=1)
            table.setLayout(table_layout)
        self.table = table
        self.layout.addWidget(self.table)

    @Slot()
    def update_col_num(self):
        self.compose_table()
