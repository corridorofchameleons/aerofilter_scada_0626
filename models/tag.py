from PySide6.QtCore import Slot


class Tag:
    def __init__(
        self,
        signal_fn,
        name: str,
        device: str,
        value: str = None
    ):
        self.name = name
        self.device = device
        self.value = value
        signal_fn.connect(self.set_val)

    @Slot(str)
    def set_val(self, val: str):
        self.value = val


# name = "pressure1"
# address = 101
# data_type = "word"           # 16-bit unsigned
# register = "input"
# unit = "Pa"
# scale = 1.0
# access = "ro"