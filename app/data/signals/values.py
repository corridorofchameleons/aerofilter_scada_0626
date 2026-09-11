from PySide6.QtCore import QObject, Signal


class ValueSignals(QObject):
    oil_tank_temp = Signal(float)
    oil_pump_freq = Signal(float)
    oil_flow = Signal(float)

    fuel_tank_temp = Signal(float)
    fuel_pump_freq = Signal(float)
    fuel_flow = Signal(float)


value_signals = ValueSignals()
