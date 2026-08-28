from PySide6.QtCore import Signal, QObject


class CommandSignals(QObject):
    pump_command_signal = Signal(bool)
    heater_command_signal = Signal(bool)

    oil_valve_5_command_signal = Signal(bool)

    def __init__(self):
        super().__init__()

command_signals = CommandSignals()
