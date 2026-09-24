from PySide6.QtCore import QObject, Slot, QThread

from app.data.topics import ACK_TOPIC, TELEMETRY_TOPIC, SET_TOPIC, INIT_TOPIC
from core.connectors.mqtt import MQTTReceiver, MQTTSender
from app.data.tag_data import TAG_DATA
from core.signals.mqtt import bus


class MainHandler(QObject):
    def __init__(
            self,
            parent
    ):
        super().__init__()
        self.tag_data = TAG_DATA
        self.bus = bus
        self.bus.mqtt_publish_signal.connect(self.handle_send_message)

        self.mqtt_receive_thread = QThread()
        self.mqtt_receive_thread.setParent(parent)
        self.mqtt_send_thread = QThread()
        self.mqtt_send_thread.setParent(parent)

        self.mqtt_receiver = MQTTReceiver(topics=(TELEMETRY_TOPIC, ACK_TOPIC))
        self.mqtt_receiver.receiver_connected.connect(self._set_receiver_connected)
        self.mqtt_sender = MQTTSender()
        self.mqtt_sender.sender_connected.connect(self._set_sender_connected)

        self.mqtt_receiver.message.connect(self.handle_message)

        self.mqtt_receiver.moveToThread(self.mqtt_receive_thread)
        self.mqtt_sender.moveToThread(self.mqtt_send_thread)

        self.mqtt_receive_thread.started.connect(self.mqtt_receiver.connect_and_run)
        self.mqtt_send_thread.started.connect(self.mqtt_sender.connect_and_run)
        self.mqtt_receive_thread.finished.connect(self.mqtt_receiver.deleteLater)
        self.mqtt_send_thread.finished.connect(self.mqtt_sender.deleteLater)

        self.mqtt_receive_thread.start()
        self.mqtt_send_thread.start()

        self.sender_connected = False
        self.receiver_connected = False

    def kill_mqtt(self):
        self.mqtt_sender.stop_client()
        self.mqtt_send_thread.quit()

        self.mqtt_receiver.stop_client()
        self.mqtt_receive_thread.quit()

    @Slot()
    def _set_receiver_connected(self):
        self.receiver_connected = True
        print("RECEIVER CONNECTED")
        if self.sender_connected:
            self.init_data()

    @Slot()
    def _set_sender_connected(self):
        self.sender_connected = True
        print("SENDER CONNECTED")
        if self.receiver_connected:
            self.init_data()

    @Slot(str, str, object)
    def handle_send_message(self, ns_name: str, name: str, value: object):
        payload = {
            'ns_name': ns_name,
            'name': name,
            'value': value
        }

        topic = SET_TOPIC
        try:
            self.mqtt_sender.publish(topic, payload)
        except Exception as e:
            pass

    def init_data(self):
        print('ALL CONNECTED')

        self.mqtt_sender.publish(
            topic=INIT_TOPIC,
            payload=None
        )

    @Slot(str, dict)
    def handle_message(self, topic: str, data: dict):
        if topic != TELEMETRY_TOPIC:
            print(data)
        # elif topic == ACK_TOPIC:
        #     self.handle_ack_message(data)
        items_data = data.get('data')
        ts = data.get('timestamp')

        for d in items_data:
            name = d.get('name')
            disabled = d.get('disabled')
            if '.' in name:
                name = name.replace('.', '_')
            value = d.get('value')
            tag = self.tag_data.get(name)
            if tag:
                tag.update_value.emit(value)
                if disabled is not None:
                    tag.set_force_disabled.emit(disabled)

    # def handle_telemetry_message(self, data: dict):
    #     ts = data.get('timestamp')
    #     for d in data.get('data'):
    #         name = d.get('name')
    #         if '.'in name:
    #             name = name.replace('.', '_')
    #         value = d.get('value')
    #         tag = self.tag_data.get(name)
    #         if tag:
    #             tag.update_value.emit(value)
    #
    #
    # def handle_ack_message(self, data: dict):
    #     for d in data:
    #         name = d.get('name')
    #         value = d.get('value')
    #         disabled = d.get('disabled')
    #         tag = self.tag_data.get(name)
    #         if tag:
    #             tag.update_value.emit(value)
    #             if disabled is not None:
    #                 tag.set_force_disabled.emit(disabled)
