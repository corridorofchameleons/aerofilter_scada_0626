from PySide6.QtWidgets import QPushButton


class SCADAButton(QPushButton):

    def __init__(
            self,
            text: str,
            slot_function,
            x: int,
            y: int
    ):
        super().__init__(text)

        self.move(x, y)

        self.clicked.connect(slot_function)