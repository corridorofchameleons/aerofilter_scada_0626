from PySide6.QtCore import QObject, Signal, Slot, QTimer

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

    set_force_disabled = Signal(bool)

    update_ui = Signal()
    disable_ui = Signal()

    error_signal = Signal(str)

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

        self.set_force_disabled.connect(self.set_force_disabled_value)

        self.timer = None

    def set_value(self, value):
        if self.timer is not None and self.timer.isActive():
            self.timer.stop()
            self.timer.deleteLater()

        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.setInterval(1000)

        self.timer.timeout.connect(self.throw_timeout)
        self.timer.start()

        self.bus.mqtt_publish_signal.emit(
            SET_TOPIC,
            {
                'name': self.name,
                'value': value
            }
        )

    def throw_timeout(self):
        self.error_signal.emit('Ярик спит')

    def handle_value(self, val):
        if self.timer is not None:
            self.timer.deleteLater()
            self.timer = None

        self.value = val
        self.update_ui.emit()

    @Slot(int)
    def update_int_value(self, val: int):
        self.handle_value(val)

    @Slot(float)
    def update_float_value(self, val: int):
        self.handle_value(val)

    @Slot(bool)
    def update_bool_value(self, val: bool):
        self.handle_value(val)

    @Slot(str)
    def update_str_value(self, val: str):
        self.handle_value(val)

    def set_disabled_value(self, value: bool):
        self.disabled = value

    @Slot(bool)
    def set_force_disabled_value(self, value: bool):
        self.disabled = value
        self.disable_ui.emit()


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
