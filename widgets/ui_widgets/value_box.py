from PySide6.QtCore import Signal
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit

from widgets.settings import Settings


class ValueBox(QWidget):
    class Size:
        _width = Settings.VALUE_BOX_WIDTH
        _height = Settings.VALUE_BOX_HEIGHT
        SMALL = (_width * 0.75, _height)
        NORMAL = (_width, _height)
        BIG = (_width * 1.5, _height)

    def __init__(
            self,
            title: str,
            size: int = 2,
            post_fn = None # функция отправки пост запроса в очередь
    ):
        super().__init__()
        self.title = title
        self.value = '73.95'

        match size:
            case 1:
                self.width, self.height = ValueBox.Size.SMALL
            case 2:
                self.width, self.height = ValueBox.Size.NORMAL
            case 3:
                self.width, self.height = ValueBox.Size.BIG
            case _:
                self.width, self.height = ValueBox.Size.NORMAL

        self.post_fn = post_fn

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setSpacing(0)

        # self.setFixedSize(self.width, self.height)

        self.title_label = QLabel(self.title)
        self.title_label.setStyleSheet(f"""
            border: 3px solid {Settings.VALUE_BOX_BORDER_COLOR};
            color: {Settings.TEXT_COLOR};
            background-color: {Settings.VALUE_BOX_TITLE_BACKGROUND_COLOR};
            font-style: italic;
            border-bottom: none;
            font-size: {Settings.VALUE_BOX_TITLE_FONT_SIZE}px;
        """)

        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.value_label = QLineEdit(self.value)
        self.value_label.setReadOnly(True)
        self.value_label.setStyleSheet(f"""
            border: 3px solid {Settings.VALUE_BOX_BORDER_COLOR};
            color: {Settings.TEXT_COLOR};
            background-color: {Settings.VALUE_BOX_VALUE_BACKGROUND_COLOR};
            font-weight: bold;
            font-size: {Settings.VALUE_BOX_VALUE_FONT_SIZE}px;
        """)
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout.addWidget(self.title_label)
        self.layout.addWidget(self.value_label)

        self.setFixedSize(self.width, self.height)