from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QWidget, QLineEdit, QHBoxLayout, QLabel


class Cell(QLineEdit):
    def __init__(
            self,
            tag,
    ):
        super().__init__()
        self.tag = tag
        self.tag.update_ui.connect(self.update_ui)

        font = QFont()
        font.setBold(True)
        self.setFont(font)

    def update_ui(self):
        self.setText(str(self.tag.value))
