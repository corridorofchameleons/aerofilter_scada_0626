from PySide6.QtWidgets import QPushButton, QSizePolicy

from widgets.settings import Settings


class SCADAButton(QPushButton):
    class Size:
        _size = Settings.SCENE_BUTTON_WIDTH
        NORMAL = _size
        BIG = _size * 1.5
        MENU = _size * 1.8

    class FontSize:
        NORMAL = 1
        MENU = 1.2

    def __init__(
            self,
            text: str,
            slot_function,
            x: int = 0,
            y: int = 0,
            size: int = 1
    ):
        super().__init__(text)

        match size:
            case 1:
                self.size = SCADAButton.Size.NORMAL
                self.font_size = Settings.SCENE_BUTTON_FONT_SIZE * SCADAButton.FontSize.NORMAL
            case 2:
                self.size = SCADAButton.Size.BIG
                self.font_size = Settings.SCENE_BUTTON_FONT_SIZE * SCADAButton.FontSize.NORMAL
            case 3:
                self.size = SCADAButton.Size.MENU
                self.font_size = Settings.SCENE_BUTTON_FONT_SIZE * SCADAButton.FontSize.MENU
            case _:
                self.size = SCADAButton.Size.NORMAL
                self.font_size = Settings.SCENE_BUTTON_FONT_SIZE * SCADAButton.FontSize.NORMAL

        if x and y:
            self.move(int(x * Settings.SCENE_SCALE), int(y * Settings.SCENE_SCALE))

        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.pressed.connect(slot_function)

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
