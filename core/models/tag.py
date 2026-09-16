from PySide6.QtCore import QObject, Signal, Slot

from app.data.topics import SET_TOPIC
from core.signals.mqtt import bus


class Tag(QObject):
    set_str_value = Signal(str)
    set_bool_value = Signal(bool)
    set_float_value = Signal(float)
    set_disabled = Signal(bool)

    def __set_name__(self, owner, name):
        self.name = name

    def __init__(
        self,
    ):
        super().__init__()
        self.value = None
        self.disabled = False

        self.bus = bus
        self.set_disabled.connect(self.set_disabled_value)

    def set_value(self, value=None):
        if value is None:
            value = not self.value
        self.bus.mqtt_publish_signal.emit(
            SET_TOPIC,
            {
                'name': self.name,
                'value': value
            }
        )

    @Slot(bool)
    def set_disabled_value(self, value: bool):
        self.disabled = value
