from PySide6.QtCore import Slot
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit

from core.models.items import Stateful
from core.models.tag import Tag
from core.settings import Settings


class ValueBox(QWidget, Stateful):
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
            error_widget: bool = False,
    ):
        super().__init__()
        Stateful.__init__(self, tag, error_widget=error_widget)
        self.title = title

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

        self.tag.set_timeout_timer()

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

    @Slot()
    def update_ui(self):
        self.close_error()
        if self.tag.value is not None:
            self.value_label.setText(str(self.tag.value))
        self.tag.set_timeout_timer()

    @Slot(str)
    def handle_error(self, text: str):
        self._set_error_stylesheet()

    @Slot()
    def close_error(self):
        self._set_normal_stylesheet()
