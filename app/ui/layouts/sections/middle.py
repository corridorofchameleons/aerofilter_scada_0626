from PySide6.QtWidgets import QWidget, QHBoxLayout

from app.ui.layouts.containers.middle_center_container import MiddleCenterContainer
from app.ui.layouts.containers.middle_right_container import RightMiddleContainer


class MiddleSection(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)

        self.scheme_box = MiddleCenterContainer()
        self.right_box = RightMiddleContainer()

        self.layout.addStretch(stretch=1)
        self.layout.addWidget(self.scheme_box, stretch=4)
        self.layout.addWidget(self.right_box, stretch=1)

        self.setLayout(self.layout)