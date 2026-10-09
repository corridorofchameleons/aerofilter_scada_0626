from PySide6.QtCore import Slot
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit

from core.models.tag import Tag
from core.settings import Settings


class ValueBox(QWidget):
    class Size:
        _width = Settings.VALUE_BOX_WIDTH
        _height = Settings.VALUE_BOX_HEIGHT
        SMALL = (_width * 0.75, _height)
        NORMAL = (_width, _height)
        BIG = (_width * 1.5, _height)

    def __init__(
            self,
            tag: Tag | None,
            title: str,
            size: int = 2,
            width: int = None,
            error_indicator: bool = True
    ):
        super().__init__()
        self.tag = tag
        self.title = title

        self.error_indicator = error_indicator
        self.error = False

        match size:
            case 1:
                self.width, self.height = ValueBox.Size.SMALL
            case 2:
                self.width, self.height = ValueBox.Size.NORMAL
            case 3:
                self.width, self.height = ValueBox.Size.BIG
            case _:
                self.width, self.height = ValueBox.Size.NORMAL

        if width is not None:
            self.width = width

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setSpacing(0)

        self.value_label = QLineEdit()
        self.value_label.setReadOnly(True)

        self._set_normal_stylesheet()

        self.value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

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
        self.layout.addWidget(self.title_label)

        self.layout.addWidget(self.value_label)

        self.setFixedSize(self.width, self.height)
        self.value_label.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.connect_tag(self.tag)

    def _set_normal_stylesheet(self):
        self.value_label.setStyleSheet(f"""
            border: 3px solid {Settings.VALUE_BOX_BORDER_COLOR};
            color: {Settings.TEXT_COLOR};
            background-color: {Settings.VALUE_BOX_VALUE_BACKGROUND_COLOR};
            font-weight: bold;
            font-size: {Settings.VALUE_BOX_VALUE_FONT_SIZE}px;
        """)

    def _set_error_stylesheet(self):
        self.value_label.setStyleSheet(f"""
            border: 3px solid {Settings.VALUE_BOX_BORDER_COLOR};
            color: {Settings.TEXT_COLOR};
            background-color: {Settings.VALUE_BOX_ERROR_BACKGROUND_COLOR};
            font-weight: bold;
            font-size: {Settings.VALUE_BOX_VALUE_FONT_SIZE}px;
        """)

    def connect_tag(self, tag: Tag):
        self.tag = tag
        if self.tag is not None:
            self.tag.update_value.connect(self.set_value)
            if self.error_indicator:
                self.tag.set_timeout_timer()
                self.tag.timeout_error_signal.connect(self.timeout_handler)

    @Slot()
    def set_value(self):
        if self.error:
            self.error = False
            self._set_normal_stylesheet()
        if self.tag.value is not None:
            self.value_label.setText(str(self.tag.value))
        self.tag.set_timeout_timer()

    @Slot(str)
    def timeout_handler(self, text: str):
        self.error = True
        self._set_error_stylesheet()
