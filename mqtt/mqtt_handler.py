from PySide6.QtCore import QObject, Slot

from models.tag import Tag, BinaryTag
from models.value_buffer import ValueBuffer
from objects.graph_data import GraphData
from objects.tags import Tags, BinaryTags


class MQTTHandler(QObject):
    def __init__(self):
        super().__init__()
        self.tags = Tags.units
        self.binary_tags = BinaryTags.units
        self.graph_units = GraphData.units

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

    @Slot(dict)
    def handle_status_message(self, data: dict):
        name = data.get('name')
        value = data.get('value')
        tag: BinaryTag = self.binary_tags.get(name)
        tag.status_signal.emit(value)



mqtt_handler = MQTTHandler()
