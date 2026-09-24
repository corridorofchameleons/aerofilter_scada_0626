from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QPushButton, QSizePolicy

from core.models.tag import Tag
from core.settings import Settings
from core.widgets.ui_widgets.error_widget import ErrorWidget


class BaseButton(QPushButton):
    class Size:
        _size = Settings.SCENE_BUTTON_WIDTH
        NORMAL = _size
        BIG = _size * 1.5
        MENU = _size * 1.8

    class FontSize:
        SMALL = 0.8
        NORMAL = 1
        MENU = 1.2

    def __init__(
            self,
            x: int = 0,
            y: int = 0,
            size: int = 1,
    ):
        super().__init__()

        self.setCursor(Qt.CursorShape.PointingHandCursor)

        match size:
            case 1:
                self.size = SCADAButton.Size.NORMAL
                self.font_size = Settings.SCENE_BUTTON_FONT_SIZE * SCADAButton.FontSize.SMALL
            case 2:
                self.size = SCADAButton.Size.BIG
                self.font_size = Settings.SCENE_BUTTON_FONT_SIZE * SCADAButton.FontSize.SMALL
            case 3:
                self.size = SCADAButton.Size.MENU
                self.font_size = Settings.SCENE_BUTTON_FONT_SIZE * SCADAButton.FontSize.MENU
            case _:
                self.size = SCADAButton.Size.NORMAL
                self.font_size = Settings.SCENE_BUTTON_FONT_SIZE * SCADAButton.FontSize.NORMAL

        if x and y:
            self.move(int(x * Settings.SCENE_SCALE), int(y * Settings.SCENE_SCALE))

        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.setFixedWidth(self.size)
        self.setFixedHeight(40)

        self.__set_style()

    def __set_style(self):
        self.setStyleSheet(f"""
            QPushButton {{
                width: {self.size}px;
                border: 3px solid {Settings.BORDER_COLOR};
                padding: 5px;
                background-color: {Settings.BUTTON_BACKGROUND_COLOR};
                color: {Settings.TEXT_COLOR};
                font-size: {self.font_size}px;
                font-style: italic;
            }}

            QPushButton:pressed {{
                background-color: {Settings.BUTTON_BACKGROUND_PRESSED_COLOR};
                padding-top: 6px;
                padding-left: 6px;
                padding-bottom: 4px;
                padding-right: 4px;
            }}

            QPushButton:disabled {{
                background-color: #B0BEC5;
                color: #78909C;
            }}
        """)


class MenuButton(BaseButton):
    def __init__(
            self,
            text: str,
            slot_function=None,
            x: int = 0,
            y: int = 0,
            size: int = 1,
    ):
        super().__init__(x, y, size)
        if slot_function:
            self.pressed.connect(slot_function)
        self.setText(text)


class SCADAButton(BaseButton):
    def __init__(
            self,
            tag: Tag,
            text_active: str,
            text_inactive: str,
            x: int = 0,
            y: int = 0,
            size: int = 1,
            height: int=40
    ):
        super().__init__(x, y, size)
        self.tag = tag
        self.tag.update_value.connect(self.update_ui)
        self.tag.timeout_error_signal.connect(self.handle_error)

        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.text_active = text_active
        self.text_inactive = text_inactive

        self.__set_text()
        if height:
            self.setFixedHeight(height)

        self.clicked.connect(self.set_new_status)

    def __set_text(self):
        if self.tag.value:
            self.setText(self.text_active)
        else:
            self.setText(self.text_inactive)

    @Slot()
    def update_ui(self):
        self.setDisabled(False)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setText(self.text_active if self.tag.value else self.text_inactive)

    @Slot(str)
    def handle_error(self, text: str):
        self.setDisabled(False)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    @Slot()
    def set_new_status(self):
        self.setDisabled(True)
        self.unsetCursor()
        self.tag.set_value(not self.tag.value)
