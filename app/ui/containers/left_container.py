from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

from app.instances.particles import Particles
from app.ui.elements.particle_table import ParticleTable
from app.ui.elements.select_button import SideButton

class LeftContainer(QWidget):
    def __init__(
            self,
            parent=None,
    ):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.button_container = QWidget()
        self.button_container_layout = QVBoxLayout()
        self.button_container_layout.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        self.button_container.setLayout(self.button_container_layout)

        self.layout.addWidget(self.button_container)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)

        self.setLayout(self.layout)
