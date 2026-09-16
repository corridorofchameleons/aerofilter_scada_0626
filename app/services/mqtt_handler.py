from PySide6.QtCore import QObject, Slot, QThread

from core.connectors.mqtt import MQTTReceiver, MQTTSender
from app.data.tag_data import TAG_DATA


class MQTTHandler(QObject):
    def __init__(
            self,
            parent
    ):
        super().__init__()
        self.tag_data = TAG_DATA

        self.mqtt_receive_thread = QThread()
        self.mqtt_receive_thread.setParent(parent)
        self.mqtt_send_thread = QThread()
        self.mqtt_send_thread.setParent(parent)

        self.mqtt_receiver = MQTTReceiver()
        self.mqtt_sender = MQTTSender()

        self.mqtt_receiver.telemetry_message.connect(self.handle_telemetry_message)
        self.mqtt_receiver.ack_message.connect(self.handle_ack_message)

        self.mqtt_receiver.moveToThread(self.mqtt_receive_thread)
        self.mqtt_sender.moveToThread(self.mqtt_send_thread)

        self.mqtt_receive_thread.started.connect(self.mqtt_receiver.connect_and_run)
        self.mqtt_send_thread.started.connect(self.mqtt_sender.connect_and_run)
        self.mqtt_receive_thread.finished.connect(self.mqtt_receiver.deleteLater)
        self.mqtt_send_thread.finished.connect(self.mqtt_sender.deleteLater)

        self.mqtt_receive_thread.start()
        self.mqtt_send_thread.start()

    def kill_mqtt(self):
        print('killing sender...')
        self.mqtt_sender.stop_client()
        self.mqtt_send_thread.quit()
        print('sender dead')

        print('killing receiver...')
        self.mqtt_receiver.stop_client()
        self.mqtt_receive_thread.quit()
        print('receiver dead')

    @Slot(dict)
    def handle_telemetry_message(self, data: dict):
        ts = data.get('timestamp')
        for d in data.get('data'):
            name = d.get('name')
            value = d.get('value')
            tag = self.tag_data.get(name)
            if tag:
                tag.set_str_value.emit(str(value))

    @Slot(list)
    def handle_ack_message(self, data: list):
        print('here')
        for d in data:
            name = d.get('name')
            value = d.get('value')
            disabled = d.get('disabled')
            tag = self.tag_data.get(name)
            if tag:
                if isinstance(value, bool):
                    tag.set_bool_value.emit(value)
                elif isinstance(value, float):
                    tag.set_float_value.emit(value)
                if disabled is not None:
                    tag.set_disabled.emit(disabled)
