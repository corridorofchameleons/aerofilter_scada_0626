from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout

from app.ui.elements.particle_table_cell import Cell
from core.settings import Settings


class ParticleTable(QWidget):
    def __init__(
            self,
            tags: dict,
    ):
        super().__init__()

        self.tags = tags
        self.layout = QVBoxLayout()
        self.setStyleSheet('''
            color: black;
        ''')
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0,0,0,0)

        self.title_width = 70
        self.value_width = 60

        row = QWidget()

        layout = QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        row.setLayout(layout)

        label = QLabel()
        label.setStyleSheet(f'''
            background-color: none;
            border: none;
        ''')
        label.setFixedWidth(self.title_width)

        value_label_before = QLabel('Частицы\nдо')
        value_label_before.setStyleSheet(f'''
            font-style: italic;
            font-size: 10px;
            border: 2px solid dimgray;
            background-color: silver;
            border-bottom: none;
            border-right: none;
        ''')
        value_label_before.setFixedWidth(self.value_width)
        value_label_before.setAlignment(Qt.AlignmentFlag.AlignCenter)

        value_label_after = QLabel('Частицы\nпосле')
        value_label_after.setStyleSheet(f'''
            font-style: italic;
            font-size: 10px;
            border: 2px solid dimgray;
            background-color: silver;
            border-bottom: none;
        ''')
        value_label_after.setFixedWidth(self.value_width)
        value_label_after.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(label)
        layout.addWidget(value_label_before)
        layout.addWidget(value_label_after)

        self.layout.addWidget(row)

        for i, (sign, tag) in enumerate(self.tags.items()):
            row = QWidget()

            layout = QHBoxLayout()
            layout.setSpacing(0)
            layout.setContentsMargins(0, 0, 0, 0)
            row.setLayout(layout)

            label = QLabel(f'{sign} мкм')
            label.setStyleSheet(f'''
                border: 2px solid dimgray;
                font-size: {Settings.VALUE_BOX_VALUE_FONT_SIZE}px;
                background-color: silver;
                border-right: none;
                {"border-top: none;" if i != 0 else ''}
            ''')
            label.setFixedWidth(self.title_width)

            value_label_before = Cell(tag[0])
            value_label_before.setReadOnly(True)
            value_label_before.setStyleSheet(f'''
                font-size: {Settings.VALUE_BOX_VALUE_FONT_SIZE * 0.9}px;
                border: 2px solid dimgray;
                background-color: white;
                border-right: none;
                {"border-top: none;" if i != 0 else ''}
            ''')
            value_label_before.setFixedWidth(self.value_width)
            value_label_before.setAlignment(Qt.AlignmentFlag.AlignCenter)

            value_label_after = Cell(tag[1])
            value_label_after.setReadOnly(True)
            value_label_after.setStyleSheet(f'''
                font-size: {Settings.VALUE_BOX_VALUE_FONT_SIZE * 0.9}px;
                border: 2px solid dimgray;
                background-color: white;
                {"border-top: none;" if i != 0 else ''}
            ''')
            value_label_after.setFixedWidth(self.value_width)
            value_label_after.setAlignment(Qt.AlignmentFlag.AlignCenter)

            layout.addWidget(label)
            layout.addWidget(value_label_before)
            layout.addWidget(value_label_after)

            self.layout.addWidget(row)


        self.setLayout(self.layout)
