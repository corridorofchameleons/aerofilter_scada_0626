from PySide6.QtWidgets import QPushButton

from widgets.settings import Settings


class SCADAButton(QPushButton):

    def __init__(
            self,
            text: str,
            slot_function,
            x: int,
            y: int
    ):
        super().__init__(text)

        self.move(int(x * Settings.SCENE_SCALE), int(y * Settings.SCENE_SCALE))

        self.pressed.connect(slot_function)
