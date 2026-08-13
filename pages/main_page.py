from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy, QLabel, QHBoxLayout

from widgets.graphics.scene import Scene
from widgets.ui_widgets.header import Header


class MainPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setObjectName('mainPage')

        self.header = Header()

        self.middle = QWidget()
        self.middle_layout = QHBoxLayout()
        self.scene = Scene()
        self.table_left = QLabel('left')
        self.table_right = QLabel('right')

        self.middle_layout.addWidget(self.table_left)
        self.middle_layout.addStretch()
        self.middle_layout.addWidget(self.scene)
        self.middle_layout.addStretch()
        self.middle_layout.addWidget(self.table_right)

        self.middle_layout.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        self.middle.setLayout(self.middle_layout)

        self.layout.addWidget(self.header)
        self.layout.addWidget(self.middle)
