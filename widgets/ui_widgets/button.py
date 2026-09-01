from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QPushButton, QSizePolicy

from models.tag import BinaryTag
from mqtt.topics import COMMAND_TOPIC
from signals.mqtt import bus
from widgets.settings import Settings


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

        self.setCursor(Qt.PointingHandCursor)

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
            tag: BinaryTag,
            text_active: str,
            text_inactive: str,
            x: int = 0,
            y: int = 0,
            size: int = 1,
    ):
        super().__init__(x, y, size)
        self.tag = tag
        if self.tag:
            self.tag.status_signal.connect(self.update_status)

        self.text_active = text_active
        self.text_inactive = text_inactive
        self.is_active = False
        self.is_pending = False

        self.setText(text_inactive)

        self.clicked.connect(self.set_new_status)

    @Slot(bool)
    def update_status(self, val: bool):
        self.is_active = val
        self.setText(self.text_active if val else self.text_inactive)
        self.is_pending = False
        print(val)

    @Slot()
    def set_new_status(self):
        if not self.is_pending:
            self.is_pending = True
            bus.mqtt_publish_signal.emit(
                COMMAND_TOPIC,
                {
                    'name': self.tag.name,
                    'value': not self.is_active
                }
            )