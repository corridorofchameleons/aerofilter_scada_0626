from PySide6.QtCore import Qt, QThread
from PySide6.QtWidgets import QWidget, QVBoxLayout

from mqtt.mqtt_client import MQTTClient, MQTTWorker
from widgets.scene import Scene


class MainPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setObjectName('mainPage')
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.scene = Scene()
        self.layout.addWidget(self.scene)

        # запуск брокера
        self.mqtt_thread = QThread()
        self.mqtt_client = MQTTClient()
        self.mqtt_worker = MQTTWorker(self.mqtt_client)
        self.mqtt_worker.moveToThread(self.mqtt_thread)
        self.mqtt_thread.started.connect(self.mqtt_worker.client.connect)
        self.mqtt_thread.start()
