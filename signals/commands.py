from PySide6.QtCore import Signal, QObject


class CommandSignals(QObject):
    oil_pump_1_command_signal = Signal(bool)
    oil_pump_2_command_signal = Signal(bool)

    heater_command_signal = Signal(bool)

    oil_valve_2_command_signal = Signal(bool)
    oil_valve_3_command_signal = Signal(bool)
    oil_valve_5_command_signal = Signal(bool)
    oil_valve_6_command_signal = Signal(bool)

    fuel_pump_1_command_signal = Signal(bool)
    fuel_pump_2_command_signal = Signal(bool)

    fuel_valve_2_command_signal = Signal(bool)
    fuel_valve_3_command_signal = Signal(bool)
    fuel_valve_5_command_signal = Signal(bool)
    fuel_valve_6_command_signal = Signal(bool)

    def __init__(self):
        super().__init__()

command_signals = CommandSignals()
