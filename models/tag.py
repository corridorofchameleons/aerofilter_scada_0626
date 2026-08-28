from PySide6.QtCore import Slot, Signal, QObject


class Tag(QObject):
    update_value = Signal(str)

    def __init__(
        self,
        name: str,
        device: int,
        signal_fn
    ):
        super().__init__()
        self.name = name
        self.device = device
        self.signal_fn = signal_fn
        self.signal_fn.connect(self.set_val)

    #TODO убрать отсюда внутрь показометра
    @Slot(str)
    def set_val(self, val: str):
        self.update_value.emit(val)


class BinaryTag(QObject):
    set_new_status = Signal(bool)
    update_status = Signal(bool)

    def __init__(
        self,
        name: str,
        device: int,
        command_signal_fn
    ):
        super().__init__()
        self.name = name
        self.device = device
        self.command_signal_fn = command_signal_fn
