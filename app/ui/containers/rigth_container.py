from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

from app.instances.particles import Particles
from app.ui.elements.particle_table import ParticleTable
from app.ui.elements.select_button import SideButton

class RightContainer(QWidget):
    def __init__(
            self,
            parent=None,
    ):
        super().__init__(parent)