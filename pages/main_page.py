from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout

from widgets.graphics.scene import Scene


class MainPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setObjectName('mainPage')
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.scene = Scene()
        self.layout.addWidget(self.scene)
