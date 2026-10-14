import time

from PySide6.QtCore import QObject, Slot, QThread
from loguru import logger

from app.data.topics import ACK_TOPIC, TELEMETRY_TOPIC, SET_TOPIC, SQL_TOPIC
from core.connectors.mqtt import MQTTReceiver, MQTTSender
from app.data.tag_data import TAG_DATA
from core.models.tag import Tag
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
        self.bus.mqtt_publish_multiple_signal.connect(self.handle_send_message)

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
        # logger.info("RECEIVER CONNECTED")
        if self.sender_connected:
            self.init_data()

    @Slot()
    def _set_sender_connected(self):
        self.sender_connected = True
        # logger.info("SENDER CONNECTED")
        if self.receiver_connected:
            self.init_data()

    @Slot(dict, str)
    def handle_send_message(self, data: dict | None, topic: str):
        ts = int(time.time() * 1000)
        payload = {
            'timestamp': ts,
            'data': data
        }

        try:
            logger.info(f'Sending message to {topic} at int-ts: {ts}')
            self.mqtt_sender.publish(topic, payload)
        except Exception as e:
            logger.error(f'FAILED TO PROCESS MESSAGE DATA AT int-ts: {ts}, error: {e}')

    def init_data(self):
        logger.success('MQTT CONNECTED SUCCESSFULLY')

        self.handle_send_message(None, SQL_TOPIC)

    @Slot(str, dict)
    def handle_message(self, topic: str, data: dict):
        items_data = data.get('data')
        ts = data.get('timestamp')

        if topic != TELEMETRY_TOPIC:
            logger.info(f'Got message from topic: {topic} at int-ts: {ts}')

        for d in items_data:
            name = d.get('name')

            if '.' in name:
                name = name.replace('.', '_')
            value = d.get('value')
            disabled = d.get('disabled')
            tag: Tag = self.tag_data.get(name)

            if tag:
                if disabled is not None:
                    tag.set_disabled.emit(disabled)

                if value is not None:
                    tag.update_value.emit(value)
                else:
                    tag.set_none_value.emit()
