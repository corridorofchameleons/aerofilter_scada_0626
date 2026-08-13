from PySide6.QtCore import Qt
from PySide6.QtWidgets import QVBoxLayout, QLabel, QPushButton, QWidget

WIDTH, HEIGHT = 1280, 720

class GraphDialog(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle('Графики')
        self.setFixedSize(WIDTH, HEIGHT)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setObjectName('graphModal')
        self.setWindowFlags(
            Qt.WindowType.Dialog |
            Qt.WindowType.WindowCloseButtonHint
        )

        self.layout = QVBoxLayout(self)

        self.label = QLabel("Это содержимое модального окна")
        self.layout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignCenter)
