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
        ns_name: str,
        value_type: str,
        telemetry_timeout: int,
        ack_timeout: int,
    ):
        super().__init__()
        self.value = None
        self.disabled = False
        self.ns_name = ns_name

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

        self.ack_timeout = ack_timeout
        self.ack_timer = None
        self._ack_timer_active = False

        self.telemetry_timeout = telemetry_timeout
        self.telemetry_timer = None
        if self.telemetry_timeout > 0:
            self.telemetry_timer = QTimer()
            self.telemetry_timer.setSingleShot(True)
            self.telemetry_timer.timeout.connect(self._throw_telemetry_timeout)

    def set_value(self, value):
        self._set_ack_timer()

        self.bus.mqtt_publish_signal.emit(
            self.ns_name, self.name, value
        )

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

    def _set_ack_timer(self):
        if self._ack_timer_active:
            return
        self._ack_timer_active = True
        self.ack_timer = self._set_timer(
            self.ack_timer,
            self.ack_timeout,
            self._throw_ack_timeout,
        )

    def set_telemetry_timer(self):
        if self.telemetry_timer is not None:
            self.telemetry_timer.start(self.telemetry_timeout)

    def _throw_ack_timeout(self):
        self._ack_timer_active = False
        self.error_signal.emit('Ярик спит')

    def _throw_telemetry_timeout(self):
        self._telemetry_timer_active = False
        self.error_signal.emit('timeout')

    def handle_value(self, val):
        if self.ack_timer is not None:
            self.ack_timer.deleteLater()
            self.ack_timer = None

        self.value = val
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

    def set_disabled_value(self, value: bool):
        self.disabled = value

    @Slot(bool)
    def set_force_disabled_value(self, value: bool):
        self.disabled = value
        self.disable_ui.emit()


class BoolTag(Tag):
    def __init__(self,
                 ns_name,
                 telemetry_timeout=0,
                 ack_timeout=3000
    ):
        super().__init__(
            ns_name,
            ValueType.type_bool,
            telemetry_timeout,
            ack_timeout
        )


class IntTag(Tag):
    def __init__(self,
                 ns_name,
                 telemetry_timeout=2000,
                 ack_timeout=3000
    ):
        super().__init__(
            ns_name,
            ValueType.type_int,
            telemetry_timeout,
            ack_timeout
        )


class FloatTag(Tag):
    def __init__(self,
                 ns_name,
                 telemetry_timeout=2000,
                 ack_timeout=3000
    ):
        super().__init__(
            ns_name,
            ValueType.type_float,
            telemetry_timeout,
            ack_timeout
        )


class StrTag(Tag):
    def __init__(self,
                 ns_name,
                 telemetry_timeout=2000,
                 ack_timeout=3000
    ):
        super().__init__(
            ns_name,
            ValueType.type_str,
            telemetry_timeout,
            ack_timeout
        )
