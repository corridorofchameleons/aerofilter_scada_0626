from dataclasses import dataclass

from PySide6.QtCore import QObject, Signal, Slot

from app.data.topics import SET_TOPIC
from core.signals.mqtt import bus


class ValueType:
    type_int = 'i'
    type_float = 'f'
    type_bool = 'b'
    type_str = 's'


class Tag(QObject):
    set_default_value = Signal(object)

    set_str_value = Signal(str)
    set_bool_value = Signal(bool)
    set_float_value = Signal(float)
    set_int_value = Signal(int)

    set_disabled = Signal(bool)
    set_force_disabled = Signal(bool)

    update_ui = Signal()
    disable_ui = Signal(bool)

    def __set_name__(self, owner, name):
        self.name = name

    def __init__(
        self,
        value_type=None
    ):
        super().__init__()
        self.value = None
        self.disabled = False

        self.update_value = self.set_default_value

        if value_type == ValueType.type_int:
            self.update_value = self.set_int_value
            self.update_value.connect(self.update_int_value)
        elif value_type == ValueType.type_float:
            self.update_value = self.set_float_value
            self.update_value.connect(self.update_float_value)
        elif value_type == ValueType.type_bool:
            self.update_value = self.set_bool_value
            self.update_value.connect(self.update_bool_value)
        elif value_type == ValueType.type_str:
            self.update_value = self.set_str_value
            self.update_value.connect(self.update_str_value)

        self.bus = bus
        self.set_disabled.connect(self.set_disabled_value)
        self.set_force_disabled.connect(self.set_force_disabled_value)

    def set_value(self, value):
        self.bus.mqtt_publish_signal.emit(
            SET_TOPIC,
            {
                'name': self.name,
                'value': value
            }
        )

    @Slot(int)
    def update_int_value(self, val: int):
        self.value = val
        self.update_ui.emit()

    @Slot(float)
    def update_float_value(self, val: int):
        self.value = val
        self.update_ui.emit()

    @Slot(bool)
    def update_bool_value(self, val: bool):
        self.value = val
        self.update_ui.emit()

    @Slot(str)
    def update_str_value(self, val: str):
        self.value = val
        self.update_ui.emit()

    @Slot(bool)
    def set_disabled_value(self, value: bool):
        self.disabled = value

    @Slot(bool)
    def set_force_disabled_value(self, value: bool):
        self.disabled = value
        self.disable_ui.emit(self.disabled)


class BoolTag(Tag):
    def __init__(self):
        super().__init__(ValueType.type_bool)


class IntTag(Tag):
    def __init__(self):
        super().__init__(ValueType.type_int)


class FloatTag(Tag):
    def __init__(self):
        super().__init__(ValueType.type_float)


class StrTag(Tag):
    def __init__(self):
        super().__init__(ValueType.type_str)
