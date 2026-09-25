from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QSizePolicy

from app.instances.particles import PARTICLES, TEST_NUM
from app.ui.elements.particle_table_cell import Cell
from core.settings import Settings


class ParticleTable(QWidget):
    def __init__(
            self,
            tags: dict,
            test_num: int = TEST_NUM
    ):
        super().__init__()

        self.tags = tags
        self.layout = QHBoxLayout()
        self.setStyleSheet('''
            color: black;
        ''')
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0,0,0,0)
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.cell_width = 55
        self.test_num = test_num

        for i in range(self.test_num + 1):
            col_widget = QWidget()
            col_widget.setObjectName('columnWidget')
            col_layout = QVBoxLayout()
            col_layout.setSpacing(0)
            col_layout.setContentsMargins(1, 1, 0, 1)
            col_widget.setStyleSheet('''
                border: 1px solid dimgray;
            ''')
            col_widget.setLayout(col_layout)

            if i <= 0:
                label = QLabel('Диапазон')
                label.setFixedHeight(20)
                label.setStyleSheet(f'''
                   border: 1px solid dimgray;
                   font-size: {Settings.VALUE_BOX_VALUE_FONT_SIZE * 0.8}px;
                   font-weight: bold;
                   background-color: silver;
                   border-right: none;
                ''')
                col_layout.addWidget(label, stretch=1)

                for val in PARTICLES:
                    label_text = f'>{val} мкм' if isinstance(val, int) else 'Класс'
                    label = QLabel(label_text)
                    label.setStyleSheet(f'''
                       border: 1px solid dimgray;
                       font-size: {Settings.VALUE_BOX_VALUE_FONT_SIZE * 0.8}px;
                       background-color: silver;
                       border-right: none;
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
                       {'border-right: none;' if i < self.test_num else 'border-right: 2px solid dimgray;'}
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
                            {'border-right: none;' if (j < 1 or i < self.test_num) else 'border-right: 2px solid dimgray;'}
                            border-top: none;
                        ''')
                        layout.addWidget(value_label, stretch=1)
                    col_layout.addWidget(couple_widget, stretch=1)
            self.layout.addWidget(col_widget, stretch=1)

        self.setLayout(self.layout)
