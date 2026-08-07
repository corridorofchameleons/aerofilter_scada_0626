from PySide6.QtCore import QObject, Slot

from models.tag import Tag
from tags.tags import Tags

class MQTTHandler(QObject):
    def __init__(self):
        super().__init__()
        self.tags = Tags.tags

    @Slot(dict)
    def handle_telemetry_message(self, data: dict):
        for d in data.get('data'):
            name = d.get('name')
            value = d.get('value')
            tag: Tag = self.tags.get(name)
            tag.signal_fn.emit(str(value))

    @Slot(bool, dict)
    def handle_command(self, success: bool, data: dict):
        print(success, data)

mqtt_handler = MQTTHandler()