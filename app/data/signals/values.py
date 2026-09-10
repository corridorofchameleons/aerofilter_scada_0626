from PySide6.QtCore import QObject, Signal


class ValueSignals(QObject):
    oil_tank_temp = Signal(float)

    fuel_tank_temp = Signal(float)


value_signals = ValueSignals()
