from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QPushButton, QSizePolicy

from core.models.tag import Tag
from core.settings import Settings


class BaseButton(QPushButton):
    class Size:
        _size = Settings.SCENE_BUTTON_WIDTH
        NORMAL = _size * Settings.SCENE_SCALE
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
            width: int = None
    ):
        super().__init__()

        self.setCursor(Qt.CursorShape.PointingHandCursor)

        match size:
            case 1:
                self.size = SwitchButton.Size.NORMAL
                self.font_size = Settings.SCENE_BUTTON_FONT_SIZE * SwitchButton.FontSize.SMALL * Settings.SCENE_SCALE
            case 2:
                self.size = SwitchButton.Size.BIG
                self.font_size = Settings.SCENE_BUTTON_FONT_SIZE * SwitchButton.FontSize.SMALL
            case 3:
                self.size = SwitchButton.Size.MENU
                self.font_size = Settings.SCENE_BUTTON_FONT_SIZE * SwitchButton.FontSize.MENU
            case _:
                self.size = SwitchButton.Size.NORMAL
                self.font_size = Settings.SCENE_BUTTON_FONT_SIZE * SwitchButton.FontSize.NORMAL

        if width is not None:
            self.size = width

        if x and y:
            self.move(int(x * Settings.SCENE_SCALE), int(y * Settings.SCENE_SCALE))

        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.setFixedWidth(self.size)
        self.setFixedHeight(40)

        self.set_style()

    def set_style(self, inactive=True):
        bgc = Settings.BUTTON_BACKGROUND_COLOR if inactive else Settings.BUTTON_BACKGROUND_COLOR_ACTIVE
        self.setStyleSheet(f"""
            QPushButton {{
                width: {self.size}px;
                border: 3px solid {Settings.BORDER_COLOR};
                padding: 5px;
                background-color: {bgc};
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
            width: int = None,
    ):
        super().__init__(x, y, size, width)

        if slot_function:
            self.pressed.connect(slot_function)
        self.setText(text)

class SwitchButton(BaseButton):
    def __init__(
            self,
            tag: Tag | None,
            text_active: str,
            text_inactive: str,
            x: int = 0,
            y: int = 0,
            size: int = 1,
            height: int=40,
            width: int | None = None,
            extra_field: tuple[str, Tag] | None = None
    ):
        super().__init__(x, y, size, width)
        self.tag = tag
        if tag is not None:
            self.tag.update_value.connect(self.update_ui)
            self.tag.timeout_error_signal.connect(self.handle_error)

        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.text_active = text_active
        self.text_inactive = text_inactive
        self.extra_field = extra_field

        self.__set_text()
        if height:
            self.setFixedHeight(height)

        self.clicked.connect(self.set_new_status)

    def __set_text(self):
        if self.tag and self.tag.value:
            self.setText(self.text_active)
        else:
            self.setText(self.text_inactive)

    def connect_tag(self, tag):
        self.tag = tag
        self.tag.update_value.connect(self.update_ui)
        self.tag.timeout_error_signal.connect(self.handle_error)
        self.set_style(not self.tag.value)

    @Slot()
    def update_ui(self):
        self.setDisabled(False)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setText(self.text_active if self.tag.value else self.text_inactive)
        self.set_style(not self.tag.value)

    @Slot(str)
    def handle_error(self, text: str):
        self.setDisabled(False)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    @Slot()
    def set_new_status(self):
        if self.tag:
            self.setDisabled(True)
            self.unsetCursor()
            value = not self.tag.value
            extra_data = {}
            if self.extra_field is not None:
                extra_data[self.extra_field[0]] = self.extra_field[1].value + 1
            print('extra_data', extra_data)
            self.tag.set_value(value, **extra_data)
