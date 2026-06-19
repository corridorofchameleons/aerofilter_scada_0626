from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout

WIDGET_SIZE = 1000, 600

class Scheme(QWidget):
    def __init__(self, parent=None, ratio=1):
        super().__init__(parent)
        self.ratio = ratio
        self.setFixedSize(ratio * WIDGET_SIZE[0], ratio * WIDGET_SIZE[1])
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.layout = QVBoxLayout(self)
        self.setObjectName('scheme')
