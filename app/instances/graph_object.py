from PySide6.QtCore import Signal, QObject


class TelemetrySignals(QObject):

    graph_pressure_diff_signal = Signal(object, float)
    graph_fuel_consumption_signal = Signal(object, float)

    def __init__(self):
        super().__init__()


telemetry_signals = TelemetrySignals()

from core.models.value_buffer import ValueBuffer
from core.settings import Settings


class GraphData:
    units = {
        'pressure_diff_1': ValueBuffer(name='pressure_diff_1',
                                       signal_fn=telemetry_signals.graph_pressure_diff_signal, buffer_len=Settings.BUFFER_LEN),
        'fuel_consumption_1': ValueBuffer(name='fuel_consumption_1',
                                          signal_fn=telemetry_signals.graph_fuel_consumption_signal, buffer_len=Settings.BUFFER_LEN),
    }
