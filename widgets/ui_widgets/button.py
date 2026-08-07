from PySide6.QtWidgets import QPushButton

from widgets.settings import Settings


class SCADAButton(QPushButton):
    class Size:
        _size = Settings.SCENE_BUTTON_WIDTH
        NORMAL = _size
        BIG = _size * 1.5

    def __init__(
            self,
            text: str,
            slot_function,
            x: int,
            y: int,
            size: int = 1
    ):
        super().__init__(text)

        match size:
            case 1:
                self.size = SCADAButton.Size.NORMAL
            case 2:
                self.size = SCADAButton.Size.BIG
            case _:
                self.size = SCADAButton.Size.NORMAL

        self.move(int(x * Settings.SCENE_SCALE), int(y * Settings.SCENE_SCALE))

        self.pressed.connect(slot_function)

        self.setStyleSheet(f"""
            QPushButton {{
                width: {self.size}px;
                border: 3px solid {Settings.BORDER_COLOR};
                padding: 5px;
                background-color: {Settings.BUTTON_BACKGROUND_COLOR};
                color: {Settings.TEXT_COLOR};
                font-size: {Settings.SCENE_BUTTON_FONT_SIZE}px;
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
