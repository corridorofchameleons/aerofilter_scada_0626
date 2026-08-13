from PySide6.QtCore import Signal, QObject


class TelemetrySignals(QObject):
    pressure1_signal = Signal(str)
    pressure2_signal = Signal(str)

    graph_pressure_diff_signal = Signal(object, float)

    def __init__(self):
        super().__init__()


telemetry_signals = TelemetrySignals()
