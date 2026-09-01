from models.value_buffer import ValueBuffer
from signals.telemetry import telemetry_signals


class GraphData:
    units = {
        'pressure_diff_1': ValueBuffer(name='pressure_diff_1',
                                       signal_fn=telemetry_signals.graph_pressure_diff_signal),
        'fuel_consumption_1': ValueBuffer(name='fuel_consumption_1',
                                          signal_fn=telemetry_signals.graph_fuel_consumption_signal),
    }
