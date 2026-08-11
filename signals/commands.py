from PySide6.QtCore import Signal, QObject


class CommandSignals(QObject):
    pump_start_signal = Signal(bool)
    heater_start_signal = Signal(bool)

    def __init__(self):
        super().__init__()
