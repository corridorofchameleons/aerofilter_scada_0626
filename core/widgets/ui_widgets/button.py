from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QPushButton, QSizePolicy

from core.models.items import Stateful
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
            size: int = 2,
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

class Button(BaseButton, Stateful):
    def __init__(
            self,
            text: str = None,
            slot_function=None,
            tag: Tag = None,
            x: int = 0,
            y: int = 0,
            size: int = 2,
            width: int = None,
            height: int = None,
            error_widget: bool = False,
            custom: bool = False
    ):
        super().__init__(x, y, size)
        self.custom = custom
        if text:
            self.setText(text)

        Stateful.__init__(self, tag, error_widget=error_widget)

        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.update_ui()
        if height:
            self.setFixedHeight(height)
        if width:
            self.setFixedWidth(width)

        self.pressed.connect(self.set_new_status)
        if slot_function:
            self.pressed.connect(slot_function)

    @Slot()
    def update_ui(self):
        if self.tag:
            if not self.tag.disabled and not self.tag.pending:
                self.setDisabled(False)
                self.setCursor(Qt.CursorShape.PointingHandCursor)
            else:
                self.setDisabled(True)
                self.unsetCursor()

    @Slot()
    def set_new_status(self, val: bool | int=None):
        if not self.custom and not (self.tag and self.tag.disabled and not self.tag.pending):
            self.setDisabled(True)
            super().set_new_status(val)

    @Slot(str)
    def handle_error(self, text: str):
        self.setDisabled(False)

class SwitchButton(Button):
    def __init__(
            self,
            text_active: str,
            text_inactive: str,
            tag: Tag | None = None,
            x: int = 0,
            y: int = 0,
            size: int = 2,
            height: int=40,
            width: int | None = None,
            error_widget: bool = False,
            custom: bool = False
    ):
        self.text_active = text_active
        self.text_inactive = text_inactive

        super().__init__(tag=tag, x=x, y=y, size=size, height=height, width=width, error_widget=error_widget, custom=custom)

        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.update_ui()

    def __set_text(self):
        if self.tag:
            if self.tag.value:
                self.setText(self.text_active)
            else:
                self.setText(self.text_inactive)

    @Slot()
    def update_ui(self):
        super().update_ui()
        if self.tag:
            self.set_style(not self.tag.value)
        self.__set_text()

    # def set_disabled(self, val: bool):
    #     self.tag.set_disabled_value(val)
    #
    # def disable_ui(self):
    #     self.setDisabled(self.tag.disabled)

    @Slot()
    def set_new_status(self, val=None):
        if self.tag:
            super().set_new_status(not self.tag.value)
