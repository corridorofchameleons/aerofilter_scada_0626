from app.data.stands.fuel_stand import FuelStand
from app.data.stands.oil_stand import OilStand
from app.data.signals.statuses import status_signals
from core.models.tag import Tag


class BinaryTags:
    units = {
        OilStand.name: Tag(name=OilStand.name, signal_fn=status_signals.oil_stand_active_signal),

        OilStand.counter_before_valve: Tag(name=OilStand.counter_before_valve,
                                           signal_fn=status_signals.oil_counter_before_valve_signal,
                                           disable_fn=status_signals.oil_counter_before_valve_disable_signal),
        OilStand.counter_after_valve: Tag(name=OilStand.counter_after_valve,
                                          signal_fn=status_signals.oil_counter_after_valve_signal,
                                          disable_fn=status_signals.oil_counter_after_valve_disable_signal),
        OilStand.mixer_input_valve: Tag(name=OilStand.mixer_input_valve,
                                              signal_fn=status_signals.oil_mixer_input_valve_signal),
        OilStand.mixer_output_valve: Tag(name=OilStand.mixer_output_valve,
                                               signal_fn=status_signals.oil_mixer_output_valve_signal),
        OilStand.main_pump: Tag(name=OilStand.main_pump,
                                      signal_fn=status_signals.oil_main_pump_signal),
        OilStand.mixing_pump: Tag(name=OilStand.mixing_pump,
                                        signal_fn=status_signals.oil_mixing_pump_signal),
        OilStand.tank_heater: Tag(name=OilStand.tank_heater,
                                        signal_fn=status_signals.oil_tank_heater_signal),
        OilStand.light: Tag(name=OilStand.light,
                                  signal_fn=status_signals.oil_light),

        FuelStand.name: Tag(name=FuelStand.name, signal_fn=status_signals.fuel_stand_active_signal),
        FuelStand.counter_before_valve: Tag(name=FuelStand.counter_before_valve,
                                            signal_fn=status_signals.fuel_counter_before_valve_signal,
                                            disable_fn=status_signals.fuel_counter_before_valve_disable_signal),
        FuelStand.counter_after_valve: Tag(name=FuelStand.counter_after_valve,
                                                 signal_fn=status_signals.fuel_counter_after_valve_signal,
                                                 disable_fn=status_signals.fuel_counter_after_valve_disable_signal),
        FuelStand.mixer_input_valve: Tag(name=FuelStand.mixer_input_valve,
                                               signal_fn=status_signals.fuel_mixer_input_valve_signal),
        FuelStand.mixer_output_valve: Tag(name=FuelStand.mixer_output_valve,
                                                signal_fn=status_signals.fuel_mixer_output_valve_signal),
        FuelStand.main_pump: Tag(name=FuelStand.main_pump,
                                       signal_fn=status_signals.fuel_main_pump_signal),
        FuelStand.mixing_pump: Tag(name=FuelStand.mixing_pump,
                                         signal_fn=status_signals.fuel_mixing_pump_signal),
        FuelStand.tank_heater: Tag(name=FuelStand.tank_heater,
                                         signal_fn=status_signals.fuel_tank_heater_signal),
        FuelStand.light: Tag(name=FuelStand.light,
                                  signal_fn=status_signals.fuel_light),
    }
