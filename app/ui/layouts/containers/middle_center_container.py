from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QHBoxLayout, QScrollArea, QVBoxLayout, QSizePolicy

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
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.scroll = QScrollArea()
        self.scroll.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        self.scroll.setStyleSheet('background-color: lightgrey; border: 1px solid dimgray;')
        self.scroll.setWidgetResizable(False)

        self.scheme = Scheme()
        self.scheme.setStyleSheet('border: none;')
        self.scheme_layout = QVBoxLayout()
        self.scheme_layout.setContentsMargins(0,0,0,0)
        self.scheme.setStyleSheet('background-color: lightgrey; border: 2px solid dimgray;')
        self.scheme.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.scheme_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.scheme_layout.addWidget(self.scheme)

        self.layout.addWidget(self.scheme)
        self.setLayout(self.layout)
