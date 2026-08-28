from PySide6.QtCore import QObject, Slot

from models.equipment import Equipment
from models.tag import Tag, BinaryTag
from models.value_buffer import ValueBuffer
from objects.equipment import EquipmentUnits
from objects.graph_data import GraphData
from objects.tags import Tags, BinaryTags


class MQTTHandler(QObject):
    def __init__(self):
        super().__init__()
        self.tags = Tags.units
        self.binary_tags = BinaryTags.units
        self.graph_units = GraphData.units
        self.equipment_units = EquipmentUnits.units

    @Slot(dict)
    def handle_telemetry_message(self, data: dict):
        ts = data.get('timestamp')
        for d in data.get('data'):
            name = d.get('name')
            value = d.get('value')
            if name in self.tags:
                tag: Tag = self.tags.get(name)
                tag.signal_fn.emit(str(value))

            if name in self.graph_units:
                graph_unit: ValueBuffer = self.graph_units.get(name)
                graph_unit.signal_fn.emit(ts, value)


    @Slot(bool, dict)
    def handle_on_off_command(self, success: bool, data: dict):
        if success:
            name = data.get('name')
            value = data.get('value')
            eq: Equipment = self.equipment_units.get(name)
            eq.set_status_signal.emit(value)

    @Slot(dict)
    def handle_status_message(self, data: dict):
        name = data.get('name')
        value = data.get('value')
        tag: BinaryTag = self.binary_tags.get(name)
        tag.set_new_status.emit(value)



mqtt_handler = MQTTHandler()
