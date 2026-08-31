from PySide6.QtWidgets import QWidget, QHBoxLayout

from widgets.graphics.schemes.scheme import Scheme
from widgets.settings import Settings


class Scene(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFixedSize(Settings.SCENE_SIZE[0] + 40, Settings.SCENE_SIZE[1] + 40)

        self.layout = QHBoxLayout(self)

        self.scheme = Scheme()

        self.layout.addWidget(self.scheme)
