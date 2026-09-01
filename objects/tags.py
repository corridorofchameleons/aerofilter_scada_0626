from models.device import Device
from models.tag import Tag, BinaryTag
from signals.commands import command_signals
from signals.telemetry import telemetry_signals

class Tags:
    units = {
        'oil_pressure_before': Tag(name='oil_pressure_before', device=Device.PLC1, signal_fn=telemetry_signals.oil_pressure_before_signal),
        'oil_pressure_after': Tag(name='oil_pressure_after', device=Device.PLC1, signal_fn=telemetry_signals.oil_pressure_after_signal),
        'oil_temperature_before': Tag(name='oil_temperature_before', device=Device.PLC1, signal_fn=telemetry_signals.oil_temperature_before_signal),
        'oil_temperature_after': Tag(name='oil_temperature_after', device=Device.PLC1, signal_fn=telemetry_signals.oil_temperature_after_signal),
        'oil_moisture_before': Tag(name='oil_moisture_before', device=Device.PLC1, signal_fn=telemetry_signals.oil_moisture_after_signal),
        'oil_moisture_after': Tag(name='oil_moisture_after', device=Device.PLC1, signal_fn=telemetry_signals.oil_moisture_after_signal),
        'oil_tank_temperature': Tag(name='oil_tank_temperature', device=Device.PLC1, signal_fn=telemetry_signals.oil_tank_temperature_signal),
        'oil_flow_meter': Tag(name='oil_flow_meter', device=Device.PLC1, signal_fn=telemetry_signals.oil_flow_meter_signal),
        'oil_main_pump_frequency': Tag(name='oil_main_pump_frequency', device=Device.PLC1, signal_fn=telemetry_signals.oil_main_pump_frequency_signal),

        'fuel_pressure_before': Tag(name='fuel_pressure_before', device=Device.PLC2, signal_fn=telemetry_signals.oil_pressure_before_signal),
        'fuel_pressure_after': Tag(name='fuel_pressure_after', device=Device.PLC2, signal_fn=telemetry_signals.oil_pressure_after_signal),
        'fuel_temperature_before': Tag(name='fuel_temperature_before', device=Device.PLC2, signal_fn=telemetry_signals.oil_temperature_before_signal),
        'fuel_temperature_after': Tag(name='fuel_temperature_after', device=Device.PLC2, signal_fn=telemetry_signals.oil_temperature_after_signal),
        'fuel_moisture_before': Tag(name='fuel_moisture_before', device=Device.PLC2, signal_fn=telemetry_signals.oil_moisture_after_signal),
        'fuel_moisture_after': Tag(name='fuel_moisture_after', device=Device.PLC2, signal_fn=telemetry_signals.oil_moisture_after_signal),
        'fuel_tank_temperature': Tag(name='fuel_tank_temperature', device=Device.PLC1, signal_fn=telemetry_signals.fuel_tank_temperature_signal),
        'fuel_flow_meter': Tag(name='fuel_flow_meter', device=Device.PLC1, signal_fn=telemetry_signals.fuel_flow_meter_signal),
        'fuel_main_pump_frequency': Tag(name='fuel_main_pump_frequency', device=Device.PLC1, signal_fn=telemetry_signals.fuel_main_pump_frequency_signal),
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

        'oil_pump_1': BinaryTag(name='oil_pump_1', device=Device.PLC1,
                                command_signal_fn=command_signals.oil_pump_1_command_signal),
        'oil_pump_2': BinaryTag(name='oil_pump_2', device=Device.PLC1,
                                command_signal_fn=command_signals.oil_pump_2_command_signal),
        'oil_tank_heater': BinaryTag(name='oil_tank_heater', device=Device.PLC1,
                                command_signal_fn=command_signals.oil_tank_heater_command_signal),

        'fuel_valve_2': BinaryTag(name='fuel_valve_2', device=Device.PLC2,
                                  command_signal_fn=command_signals.fuel_valve_2_command_signal),
        'fuel_valve_3': BinaryTag(name='fuel_valve_3', device=Device.PLC2,
                                  command_signal_fn=command_signals.fuel_valve_3_command_signal),
        'fuel_valve_5': BinaryTag(name='fuel_valve_5', device=Device.PLC2,
                                  command_signal_fn=command_signals.fuel_valve_5_command_signal),
        'fuel_valve_6': BinaryTag(name='fuel_valve_6', device=Device.PLC2,
                                  command_signal_fn=command_signals.fuel_valve_6_command_signal),

        'fuel_pump_1': BinaryTag(name='fuel_pump_1', device=Device.PLC2,
                                command_signal_fn=command_signals.fuel_pump_1_command_signal),
        'fuel_pump_2': BinaryTag(name='fuel_pump_2', device=Device.PLC2,
                                 command_signal_fn=command_signals.fuel_pump_2_command_signal),
        'fuel_tank_heater': BinaryTag(name='fuel_tank_heater', device=Device.PLC2,
                                     command_signal_fn=command_signals.oil_tank_heater_command_signal),
        }
