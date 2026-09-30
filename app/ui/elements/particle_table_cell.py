from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QWidget, QLineEdit, QHBoxLayout, QLabel

from core.models.tag import Tag


class Cell(QLineEdit):
    def __init__(
            self,
            tag: Tag | None = None,
    ):
        super().__init__()
        self.tag = tag
        if self.tag is not None:
            self.tag.update_ui.connect(self.update_ui)

        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        font = QFont()
        font.setBold(True)
        self.setFont(font)

    def update_ui(self):
        self.setText(str(self.tag.value))
