from models.device import Device
from models.equipment import Equipment
from signals.commands import CommandSignals


class EquipmentUnits:
    command_signals = CommandSignals()
    units = {
        'pump': Equipment(name='pump', device=Device.PLC1, set_status_signal=command_signals.pump_start_signal),
    }
