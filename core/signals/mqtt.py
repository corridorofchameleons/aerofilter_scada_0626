from PySide6.QtCore import QObject, Signal


class MQTTBus(QObject):
    mqtt_publish_signal = Signal(str, str, object)

bus = MQTTBus()
