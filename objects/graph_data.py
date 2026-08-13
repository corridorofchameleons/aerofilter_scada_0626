from models.device import Device
from models.value_buffer import ValueBuffer
from signals.telemetry import telemetry_signals


class GraphData:
    units = {
        'pressure_diff_1': ValueBuffer(name='pressure_diff_1', device=Device.PLC1, signal_fn=telemetry_signals.graph_pressure_diff_signal),
    }
