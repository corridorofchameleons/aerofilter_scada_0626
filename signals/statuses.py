from PySide6.QtCore import QObject, Signal


class StatusSignals(QObject):
    oil_valve_5_status_signal = Signal(bool)

    def __init__(self):
        super().__init__()


status_signals = StatusSignals()