from PySide6.QtCore import QObject, Slot

from models.device import Device
from models.tag import Tag
from signals.telemetry import TelemetrySignals

class Tags:
    telemetry_signals = TelemetrySignals()
    tags = {
        'pressure1': Tag(name='pressure1', device=Device.PLC1, signal_fn=telemetry_signals.pressure1_signal),
        'pressure2': Tag(name='pressure1', device=Device.PLC1, signal_fn=telemetry_signals.pressure2_signal),
    }
