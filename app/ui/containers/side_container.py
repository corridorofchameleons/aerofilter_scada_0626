from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

from app.ui.elements.select_button import SideButton

class SideContainer(QWidget):
    def __init__(
            self,
            stand,
            parent=None,
    ):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.stand = stand

        self.side_button = SideButton(self.stand)
        self.table = QLabel('table')

        self.layout.addWidget(self.side_button)
        self.layout.addWidget(self.table)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)

        self.setLayout(self.layout)
