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

    set_none_value = Signal()

    update_ui = Signal()
    disable_ui = Signal()

    timeout_error_signal = Signal(str)

    def __set_name__(self, owner, name):
        if self.name is None:
            self.name = name

    def __init__(
        self,
        ns_name: str,
        value_type: str,
        timeout: int = 3000,
        initial: bool | int | float | str | None = None,
        name: str | None = None,
    ):
        super().__init__()
        self.initial_value = initial
        self.value = initial
        self.disabled = False
        self.ns_name = ns_name
        self.name = name

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

        self.set_none_value.connect(self.set_none)

        self.bus = bus

        self.timeout = timeout
        self.timer = None
        if self.timeout > 0:
            self.timer = QTimer()
            self.timer.setSingleShot(True)
            self.timer.timeout.connect(self._throw_timeout)

        self._timer_active = False

    def set_value(self, value, **kwargs):
        self.set_timeout_timer()
        data = {
            'ns_name': self.ns_name,
            'name': self.name,
            'value': value
        }

        if kwargs:
            for n, v in kwargs.items():
                data[n] = v

        self.bus.mqtt_publish_signal.emit(data, SET_TOPIC)


    @staticmethod
    def _set_timer(timer, timeout, fn):
        if timer is not None:
            timer.timeout.disconnect(fn)
            timer.stop()
            timer.deleteLater()

        timer = None

        if timeout > 0:

            timer = QTimer()
            timer.setSingleShot(True)
            timer.setInterval(timeout)

            timer.timeout.connect(fn)
            timer.start()

        return timer

    def set_timeout_timer(self):
        if self._timer_active:
            return
        self._timer_active = True
        self.timer = self._set_timer(
            self.timer,
            self.timeout,
            self._throw_timeout,
        )

    def _throw_timeout(self):
        self._ack_timer_active = False
        self.timeout_error_signal.emit('Ярик спит')

    def handle_value(self, val):
        if self.timer is not None:
            self.timer.deleteLater()
            self.timer = None
        self.value = val
        self.update_ui.emit()

    @Slot()
    def set_none(self):
        if self.timer is not None:
            self.timer.deleteLater()
            self.timer = None
        if self.initial_value is not None:
            self.value = self.initial_value
        else:
            self.value = None
        self.update_ui.emit()

    @Slot(int)
    def update_int_value(self, val: int):
        self.handle_value(val)

    @Slot(float)
    def update_float_value(self, val: float):
        self.handle_value(val)

    @Slot(bool)
    def update_bool_value(self, val: bool):
        self.handle_value(val)

    @Slot(str)
    def update_str_value(self, val: str):
        self.handle_value(val)

    @Slot(bool)
    def set_disabled_value(self, value: bool):
        self.disabled = value
        self.disable_ui.emit()
