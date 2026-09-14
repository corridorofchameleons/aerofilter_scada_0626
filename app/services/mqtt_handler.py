from PySide6.QtCore import QObject, Slot

from app.data.tags.binary_tags import BinaryTags
from app.data.tags.telemetry_tags import Tags
from app.data.tags.graph_tags import GraphData
from app.data.tags.value_tags import ValueTags
from core.models.tag import Tag
from core.models.value_buffer import ValueBuffer


class MQTTHandler(QObject):
    def __init__(self):
        super().__init__()

    @Slot(dict)
    def handle_telemetry_message(self, data: dict):
        ts = data.get('timestamp')
        for d in data.get('data'):
            name = d.get('name')
            value = d.get('value')
            if name in Tags.units:
                tag: Tag = Tags.units.get(name)
                tag.signal_fn.emit(str(value))

            if name in GraphData.units:
                graph_unit: ValueBuffer = GraphData.units.get(name)
                graph_unit.signal_fn.emit(ts, value)

    @Slot(list)
    def handle_status_message(self, data: list):
        print(data)
        for d in data:
            name = d.get('name')
            value = d.get('value')
            disabled = d.get('disabled')
            tag: Tag = BinaryTags.units.get(name)
            if tag is not None:
                tag.signal_fn.emit(value)
                if tag.disable_fn and disabled is not None:
                    tag.disable_fn.emit(disabled)

    @Slot(dict)
    def handle_value_message(self, data: dict):
        name = data.get('name')
        value = data.get('value')
        tag: Tag = ValueTags.units.get(name)
        print(tag)
        tag.signal_fn.emit(value)


mqtt_handler = MQTTHandler()
