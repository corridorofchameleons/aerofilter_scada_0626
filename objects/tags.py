from models.device import Device
from models.tag import Tag, BinaryTag
from signals.commands import command_signals
from signals.telemetry import telemetry_signals

class Tags:
    units = {
        'pressure1': Tag(name='pressure1', device=Device.PLC1, signal_fn=telemetry_signals.pressure1_signal),
        'pressure2': Tag(name='pressure2', device=Device.PLC1, signal_fn=telemetry_signals.pressure2_signal),
    }


class BinaryTags:
    units = {
        'oil_valve_5': BinaryTag(name='oil_valve_5', device=Device.PLC1,
                                 command_signal_fn=command_signals.oil_valve_5_command_signal),
    }
