from PySide6.QtCore import QObject


class Tag(QObject):
    def __init__(
        self,
        name: str,
        signal_fn,
        disable_fn = None
    ):
        super().__init__()
        self.name = name
        self.signal_fn = signal_fn
        self.disable_fn = disable_fn
