from models.device import Device
from models.equipment import Equipment
from signals.commands import command_signals


class EquipmentUnits:
    units = {
        'pump_1': Equipment(name='pump_1', device=Device.PLC1, set_status_signal=command_signals.pump_command_signal),
        'heater_1': Equipment(name='heater_1', device=Device.PLC1, set_status_signal=command_signals.heater_command_signal),
    }
