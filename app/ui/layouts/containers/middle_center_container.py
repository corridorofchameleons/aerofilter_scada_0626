from PySide6.QtWidgets import QWidget, QHBoxLayout

from app.ui.layouts.scheme.scheme import Scheme


class MiddleCenterContainer(QWidget):
    def __init__(
            self,
            # set_active_stand: IntTag
    ):

        super().__init__()
        # self.set_active_stand = set_active_stand

        self.scene = QWidget(self)
        # self.scene.setStyleSheet('border: 1px solid green;')
        self.layout = QHBoxLayout(self.scene)
        self.layout.setContentsMargins(0,0,0,0)

        self.scheme = Scheme()
        self.layout.addWidget(self.scheme)
        self.setLayout(self.layout)
