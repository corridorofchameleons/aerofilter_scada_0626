from app.data.stands.fuel_stand import FuelStand
from app.data.stands.oil_stand import OilStand
from core.models.tag import Tag
from app.data.signals.telemetry import telemetry_signals


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
