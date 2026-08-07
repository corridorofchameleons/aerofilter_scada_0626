from PySide6.QtCore import Slot, Signal, QObject


class Tag(QObject):
    update_value = Signal(str)

    def __init__(
        self,
        name: str,
        device: str,
        signal_fn
    ):
        super().__init__()
        self.name = name
        self.device = device
        self.signal_fn = signal_fn
        self.signal_fn.connect(self.set_val)

    @Slot(str)
    def set_val(self, val: str):
        self.update_value.emit(val)
