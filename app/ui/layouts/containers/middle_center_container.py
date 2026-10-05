from PySide6.QtWidgets import QWidget, QHBoxLayout

from app.ui.layouts.scheme.scheme import Scheme
from core.settings import Settings


class MiddleCenterContainer(QWidget):
    def __init__(
            self
    ):

        super().__init__()
        self.scene = QWidget(self)
        self.layout = QHBoxLayout(self.scene)
        self.layout.setContentsMargins(0,0,0,0)

        self.scheme = Scheme()
        self.scheme.setMinimumHeight(Settings.SCENE_SIZE[1])
        self.layout.addWidget(self.scheme)
        self.setLayout(self.layout)
