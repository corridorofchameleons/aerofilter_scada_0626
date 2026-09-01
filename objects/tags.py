from models.stand import OilStand, FuelStand
from models.tag import Tag, BinaryTag
from signals.statuses import status_signals
from signals.telemetry import telemetry_signals


class Tags:
    units = {
        OilStand.pressure_before: Tag(name=OilStand.pressure_before,
                                      signal_fn=telemetry_signals.oil_pressure_before_signal),
        OilStand.pressure_after: Tag(name=OilStand.pressure_after,
                                     signal_fn=telemetry_signals.oil_pressure_after_signal),
        OilStand.temperature_before: Tag(name=OilStand.temperature_before,
                                         signal_fn=telemetry_signals.oil_temperature_before_signal),
        OilStand.temperature_after: Tag(name=OilStand.temperature_after,
                                        signal_fn=telemetry_signals.oil_temperature_after_signal),
        OilStand.moisture_before: Tag(name=OilStand.moisture_before,
                                      signal_fn=telemetry_signals.oil_moisture_after_signal),
        OilStand.moisture_after: Tag(name=OilStand.moisture_after,
                                     signal_fn=telemetry_signals.oil_moisture_after_signal),
        OilStand.tank_temperature: Tag(name=OilStand.tank_temperature,
                                       signal_fn=telemetry_signals.oil_tank_temperature_signal),
        OilStand.flow_meter: Tag(name=OilStand.flow_meter,
                                 signal_fn=telemetry_signals.oil_flow_meter_signal),
        OilStand.main_pump_frequency: Tag(name=OilStand.main_pump_frequency,
                                          signal_fn=telemetry_signals.oil_main_pump_frequency_signal),

        FuelStand.pressure_before: Tag(name=FuelStand.pressure_before,
                                       signal_fn=telemetry_signals.oil_pressure_before_signal),
        FuelStand.pressure_after: Tag(name=FuelStand.pressure_after,
                                      signal_fn=telemetry_signals.oil_pressure_after_signal),
        FuelStand.temperature_before: Tag(name=FuelStand.temperature_before,
                                          signal_fn=telemetry_signals.oil_temperature_before_signal),
        FuelStand.temperature_after: Tag(name=FuelStand.temperature_after,
                                         signal_fn=telemetry_signals.oil_temperature_after_signal),
        FuelStand.moisture_before: Tag(name=FuelStand.moisture_before,
                                       signal_fn=telemetry_signals.oil_moisture_after_signal),
        FuelStand.moisture_after: Tag(name=FuelStand.moisture_after,
                                      signal_fn=telemetry_signals.oil_moisture_after_signal),
        FuelStand.tank_temperature: Tag(name=FuelStand.tank_temperature,
                                        signal_fn=telemetry_signals.fuel_tank_temperature_signal),
        FuelStand.flow_meter: Tag(name=FuelStand.flow_meter,
                                  signal_fn=telemetry_signals.fuel_flow_meter_signal),
        FuelStand.main_pump_frequency: Tag(name=FuelStand.main_pump_frequency,
                                           signal_fn=telemetry_signals.fuel_main_pump_frequency_signal),
    }


class BinaryTags:
    units = {
        OilStand.counter_after_valve: BinaryTag(name=OilStand.counter_after_valve,
                                                status_signal=status_signals.oil_counter_after_valve_signal),
        OilStand.counter_before_valve: BinaryTag(name=OilStand.counter_before_valve,
                                                 status_signal=status_signals.oil_counter_before_valve_signal),
        OilStand.mixer_input_valve: BinaryTag(name=OilStand.mixer_input_valve,
                                              status_signal=status_signals.oil_mixer_input_valve_signal),
        OilStand.mixer_output_valve: BinaryTag(name=OilStand.mixer_output_valve,
                                               status_signal=status_signals.oil_mixer_output_valve_signal),
        OilStand.main_pump: BinaryTag(name=OilStand.main_pump,
                                      status_signal=status_signals.oil_main_pump_signal),
        OilStand.mixing_pump: BinaryTag(name=OilStand.mixing_pump,
                                        status_signal=status_signals.oil_mixing_pump_signal),
        OilStand.tank_heater: BinaryTag(name=OilStand.tank_heater,
                                        status_signal=status_signals.oil_tank_heater_signal),
        OilStand.light: BinaryTag(name=OilStand.light,
                                  status_signal=status_signals.oil_light),

        FuelStand.counter_after_valve: BinaryTag(name=FuelStand.counter_after_valve,
                                                 status_signal=status_signals.fuel_counter_after_valve_signal),
        FuelStand.counter_before_valve: BinaryTag(name=FuelStand.counter_before_valve,
                                                  status_signal=status_signals.fuel_counter_before_valve_signal),
        FuelStand.mixer_input_valve: BinaryTag(name=FuelStand.mixer_input_valve,
                                               status_signal=status_signals.fuel_mixer_input_valve_signal),
        FuelStand.mixer_output_valve: BinaryTag(name=FuelStand.mixer_output_valve,
                                                status_signal=status_signals.fuel_mixer_output_valve_signal),
        FuelStand.main_pump: BinaryTag(name=FuelStand.main_pump,
                                       status_signal=status_signals.fuel_main_pump_signal),
        FuelStand.mixing_pump: BinaryTag(name=FuelStand.mixing_pump,
                                         status_signal=status_signals.fuel_mixing_pump_signal),
        FuelStand.tank_heater: BinaryTag(name=FuelStand.tank_heater,
                                         status_signal=status_signals.fuel_tank_heater_signal),
        FuelStand.light: BinaryTag(name=FuelStand.light,
                                  status_signal=status_signals.fuel_light),
    }
