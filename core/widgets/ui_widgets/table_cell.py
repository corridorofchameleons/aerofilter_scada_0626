from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QLabel

from core.models.items import Stateful
from core.models.tag import Tag
from core.settings import Settings


class Cell(QLabel, Stateful):
    def __init__(
            self,
            tag: Tag | None = None,
            text: str | None = None,
            error_widget: bool = False
    ):
        super().__init__()
        Stateful.__init__(self, tag, error_widget=error_widget)
        self.text = text

        if self.text is not None:
            self.setText(self.text)

        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        font = QFont()
        font.setBold(True)
        self.setFont(font)
        self.set_style(font_size=Settings.VALUE_BOX_VALUE_FONT_SIZE * 0.9)

    @Slot()
    def update_ui(self):
        if self.tag and self.tag.value is not None:
            self.setText(str(self.tag.value))
        else:
            self.setText('')

    def set_style(self, font_size: float, bg_color: str = None):
        bbc = 'silver'
        bgc = 'white'
        if bg_color is not None:
            bgc = bg_color
            bbc = 'dimgray'

        self.setStyleSheet(f'''
            font-size: {font_size}px;
            border: none;
            border-left: 1px solid dimgray;
            border-bottom: 1px solid {bbc};
            background-color: {bgc};
        ''')
