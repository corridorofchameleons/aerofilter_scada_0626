from PySide6.QtCore import QObject, Signal


class MQTTBus(QObject):
    mqtt_publish_signal = Signal(dict)
    mqtt_publish_multiple_signal = Signal(list)

bus = MQTTBus()
