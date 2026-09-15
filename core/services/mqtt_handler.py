from PySide6.QtCore import QObject, Slot

from core.models.tag import Tag
from core.utils.tag_data import TAG_DATA


class MQTTHandler(QObject):
    def __init__(
            self,
    ):
        super().__init__()
        self.tag_data = TAG_DATA

    @Slot(dict)
    def handle_telemetry_message(self, data: dict):
        ts = data.get('timestamp')
        for d in data.get('data'):
            name = d.get('name')
            value = d.get('value')
            tag: Tag = self.tag_data.get(name)
            if tag:
                tag.set_str_value.emit(str(value))

    @Slot(list)
    def handle_status_message(self, data: list):
        for d in data:
            name = d.get('name')
            value = d.get('value')
            disabled = d.get('disabled')
            tag: Tag = self.tag_data.get(name)
            if tag:
                tag.set_bool_value.emit(value)
                if disabled is not None:
                    tag.set_disabled.emit(disabled)

    @Slot(dict)
    def handle_value_message(self, data: dict):
        name = data.get('name')
        value = data.get('value')
        tag: Tag = self.tag_data.get(name)
        if tag:
            tag.set_float_value.emit(value)


mqtt_handler = MQTTHandler()
