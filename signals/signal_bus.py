from PySide6.QtCore import QObject, Signal


class GlobalBus(QObject):
    mqtt_publish_signal = Signal(str, dict)

bus = GlobalBus()