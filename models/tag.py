from PySide6.QtCore import Slot, Signal, QObject


class Tag(QObject):
    def __init__(
        self,
        name: str,
        signal_fn
    ):
        super().__init__()
        self.name = name
        self.signal_fn = signal_fn


class BinaryTag(QObject):
    def __init__(
        self,
        name: str,
        status_signal
    ):
        super().__init__()
        self.name = name
        self.status_signal = status_signal
