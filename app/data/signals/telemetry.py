from PySide6.QtCore import Signal, QObject


class TelemetrySignals(QObject):
    oil_pressure_before_signal = Signal(str)
    oil_pressure_after_signal = Signal(str)
    oil_temperature_before_signal = Signal(str)
    oil_temperature_after_signal = Signal(str)
    oil_moisture_before_signal = Signal(str)
    oil_moisture_after_signal = Signal(str)
    oil_tank_temperature_signal = Signal(str)
    oil_main_pump_frequency_signal = Signal(str)
    oil_flow_meter_signal = Signal(str)

    fuel_pressure_before_signal = Signal(str)
    fuel_pressure_after_signal = Signal(str)
    fuel_temperature_before_signal = Signal(str)
    fuel_temperature_after_signal = Signal(str)
    fuel_moisture_before_signal = Signal(str)
    fuel_moisture_after_signal = Signal(str)
    fuel_tank_temperature_signal = Signal(str)
    fuel_main_pump_frequency_signal = Signal(str)
    fuel_flow_meter_signal = Signal(str)

    graph_pressure_diff_signal = Signal(object, float)
    graph_fuel_consumption_signal = Signal(object, float)

    def __init__(self):
        super().__init__()


telemetry_signals = TelemetrySignals()
