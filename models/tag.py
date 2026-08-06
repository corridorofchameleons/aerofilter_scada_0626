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


# name = "pressure1"
# address = 101
# data_type = "word"           # 16-bit unsigned
# register = "input"
# unit = "Pa"
# scale = 1.0
# access = "ro"