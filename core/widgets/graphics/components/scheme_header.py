from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout

from app.layouts.scheme_layout import HEADER_WIDTH, \
    HEADER_HEIGHT
from core.widgets.settings import Settings


class SchemeHeader(QWidget):
    def __init__(
            self,
            title: str,
            parent=None
    ):
        super().__init__(parent)
        self.title = title

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setFixedSize(HEADER_WIDTH, HEADER_HEIGHT)
        self.layout.setSpacing(0)
        self.setObjectName('schemeHeader')

        self.title_box = QWidget()
        self.title_box_layout = QHBoxLayout()
        self.title_label = QLabel(self.title)
        self.title_label.setStyleSheet(f'''
            color: {Settings.TEXT_COLOR};
            font-size: {Settings.HEADER_FONT_SIZE}px;
            font-style: italic;
        ''')
        self.title_label.setContentsMargins(5, 0, 5, 0)
        self.title_box_layout.addWidget(self.title_label)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_box.setLayout(self.title_box_layout)

        self.button_box = QWidget()
        self.button_box_layout = QHBoxLayout()

        self.button_box_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.button_box.setLayout(self.button_box_layout)

        self.layout.addWidget(self.title_label)
        self.layout.addWidget(self.button_box)

        self.setLayout(self.layout)
