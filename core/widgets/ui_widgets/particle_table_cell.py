from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QWidget, QLineEdit, QHBoxLayout, QLabel

from core.models.tag import Tag
from core.settings import Settings


class Cell(QLabel):
    def __init__(
            self,
            tag: Tag | None = None,
            index: int | None = 0,
            highlight_tag: Tag=None,
            text: str | None = None
    ):
        super().__init__()
        self.text = text

        if self.text is not None:
            self.setText(self.text)

        self.tag = tag
        self.index = index
        if self.tag is not None:
            self.tag.update_ui.connect(self.update_ui)

        self.highlight_tag = highlight_tag
        if self.highlight_tag:
            self.highlight_tag.update_ui.connect(self.highlight)

        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        font = QFont()
        font.setBold(True)
        self.setFont(font)

        if self.text is None:
            self.update_ui()

    @Slot()
    def update_ui(self):
        if self.tag and self.tag.value is not None:
            self.setText(str(self.tag.value))
        else:
            self.setText(None)

        if self.highlight_tag is not None:
            if self.highlight_tag.value == self.index:
                self.__highlight_cell(True)
            else:
                self.__highlight_cell(False)

    def __highlight_cell(self, val: bool, bg_color: str = None):
        if val:
            bgc = 'white'
        else:
            bgc = '#E9E9E9'
        font = Settings.VALUE_BOX_VALUE_FONT_SIZE * 0.9
        bbc = 'silver'
        if bg_color is not None:
            bgc = bg_color
            bbc = 'dimgray'
            font = Settings.VALUE_BOX_VALUE_FONT_SIZE * 0.8
        self.setStyleSheet(f'''
            font-size: {font}px;
            border: none;
            border-left: 1px solid dimgray;
            border-bottom: 1px solid {bbc};
            background-color: {bgc};
        ''')

    @Slot(int)
    def highlight(self):
        if self.highlight_tag.value == self.index:
            self.__highlight_cell(True)
        else:
            self.__highlight_cell(False)

    def set_style(self, bgc: str):
        self.__highlight_cell(val=False, bg_color=bgc)

