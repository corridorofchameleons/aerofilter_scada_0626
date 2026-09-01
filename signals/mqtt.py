from PySide6.QtCore import QObject, Signal


class MQTTBus(QObject):
    mqtt_publish_signal = Signal(str, dict)

bus = MQTTBus()