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
        'oil_valve_2': BinaryTag(name='oil_valve_2', device=Device.PLC1,
                                 command_signal_fn=command_signals.oil_valve_2_command_signal),
        'oil_valve_3': BinaryTag(name='oil_valve_3', device=Device.PLC1,
                                 command_signal_fn=command_signals.oil_valve_3_command_signal),
        'oil_valve_5': BinaryTag(name='oil_valve_5', device=Device.PLC1,
                                 command_signal_fn=command_signals.oil_valve_5_command_signal),
        'oil_valve_6': BinaryTag(name='oil_valve_6', device=Device.PLC1,
                                 command_signal_fn=command_signals.oil_valve_6_command_signal),

        'fuel_valve_2': BinaryTag(name='fuel_valve_2', device=Device.PLC2,
                                  command_signal_fn=command_signals.fuel_valve_2_command_signal),
        'fuel_valve_3': BinaryTag(name='fuel_valve_3', device=Device.PLC2,
                                  command_signal_fn=command_signals.fuel_valve_3_command_signal),
        'fuel_valve_5': BinaryTag(name='fuel_valve_5', device=Device.PLC2,
                                  command_signal_fn=command_signals.fuel_valve_5_command_signal),
        'fuel_valve_6': BinaryTag(name='fuel_valve_6', device=Device.PLC2,
                                  command_signal_fn=command_signals.fuel_valve_6_command_signal),
    }
