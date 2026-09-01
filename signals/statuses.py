from PySide6.QtCore import QObject, Signal


class StatusSignals(QObject):
    oil_main_pump_signal = Signal(bool)
    oil_mixing_pump_signal = Signal(bool)
    oil_tank_heater_signal = Signal(bool)
    oil_counter_before_valve_signal = Signal(bool)
    oil_counter_after_valve_signal = Signal(bool)
    oil_mixer_input_valve_signal = Signal(bool)
    oil_mixer_output_valve_signal = Signal(bool)
    oil_light = Signal(bool)

    fuel_main_pump_signal = Signal(bool)
    fuel_mixing_pump_signal = Signal(bool)
    fuel_tank_heater_signal = Signal(bool)
    fuel_counter_before_valve_signal = Signal(bool)
    fuel_counter_after_valve_signal = Signal(bool)
    fuel_mixer_input_valve_signal = Signal(bool)
    fuel_mixer_output_valve_signal = Signal(bool)
    fuel_light = Signal(bool)

    def __init__(self):
        super().__init__()

status_signals = StatusSignals()