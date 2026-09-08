from app.data.stands.fuel_stand import FuelStand
from app.data.stands.oil_stand import OilStand
from app.data.signals.statuses import status_signals
from core.models.tag import BinaryTag


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
