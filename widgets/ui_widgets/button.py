from PySide6.QtWidgets import QPushButton

from widgets.graphics.constants import SCENE_SCALE


class SCADAButton(QPushButton):

    def __init__(
            self,
            text: str,
            slot_function,
            x: int,
            y: int
    ):
        super().__init__(text)

        self.move(int(x * SCENE_SCALE), int(y * SCENE_SCALE))

        self.pressed.connect(slot_function)
