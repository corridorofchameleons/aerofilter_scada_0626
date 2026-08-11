from PySide6.QtCore import QObject, Slot

from models.equipment import Equipment
from models.tag import Tag
from tags.equipment import EquipmentUnits
from tags.tags import Tags

class MQTTHandler(QObject):
    def __init__(self):
        super().__init__()
        self.tags = Tags.tags
        self.equipment_units = EquipmentUnits.units

    @Slot(dict)
    def handle_telemetry_message(self, data: dict):
        for d in data.get('data'):
            name = d.get('name')
            value = d.get('value')
            tag: Tag = self.tags.get(name)
            if tag:
                tag.signal_fn.emit(str(value))

    @Slot(bool, dict)
    def handle_on_off_command(self, success: bool, data: dict):
        if success:
            name = data.get('name')
            value = data.get('value')
            eq: Equipment = self.equipment_units.get(name)
            eq.set_status_signal.emit(value)

mqtt_handler = MQTTHandler()