from PySide6.QtCore import Signal, QObject


class TelemetrySignals(QObject):
    pressure1_signal = Signal(str)
    pressure2_signal = Signal(str)

    def __init__(self):
        super().__init__()
