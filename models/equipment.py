from PySide6.QtCore import Slot, Signal, QObject


class Equipment(QObject):
    update_status = Signal(bool)
    # update_value = Signal(str)

    def __init__(
        self,
        name: str,
        device: str,
        # set_val_signal,
        set_status_signal,
        on: bool = False
    ):
        super().__init__()
        self.name = name
        self.device = device
        self.on = on
        # self.set_val_signal = set_val_signal
        self.set_status_signal = set_status_signal

        # self.set_val_signal.connect(self.set_val)
        self.set_status_signal.connect(self.set_status)

    # @Slot(str)
    # def set_val(self, val: str):
    #     self.update_value.emit(val)

    def set_on(self, val: bool):
        self.on = val

    @Slot(bool)
    def set_status(self, on: bool):
        self.set_on(on)
