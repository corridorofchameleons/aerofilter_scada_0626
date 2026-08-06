from PySide6.QtCore import QObject, Slot

from models.device import Device
from models.tag import Tag
from signals.telemetry import TelemetrySignals

class MQTTHandler(QObject):
    def __init__(self):
        super().__init__()
        self.telemetry_signals = TelemetrySignals()
        self.tags = {
            'pressure1': Tag(name='pressure1', device=Device.PLC1, signal_fn=self.telemetry_signals.pressure1_signal),
            'pressure2': Tag(name='pressure1', device=Device.PLC1, signal_fn=self.telemetry_signals.pressure2_signal),
        }

    @Slot(dict)
    def handle_message(self, data: dict):
        for d in data.get('data'):
            name = d.get('name')
            value = d.get('value')
            tag: Tag = self.tags.get(name)
            tag.signal_fn.emit(str(value))


mqtt_handler = MQTTHandler()