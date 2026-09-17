import json
from random import randint

from PySide6.QtCore import QObject, Slot, QThread, QTimer
from paho.mqtt.enums import MQTTErrorCode

from app.data.topics import ACK_TOPIC, TELEMETRY_TOPIC
from core.connectors.mqtt import MQTTReceiver, MQTTSender
from app.data.tag_data import TAG_DATA
from core.signals.mqtt import bus


class MQTTHandler(QObject):
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

        self.mqtt_receiver = MQTTReceiver(telemetry_topic=TELEMETRY_TOPIC, ack_topic=ACK_TOPIC)
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
        self.mqtt_sender.stop_client()
        self.mqtt_send_thread.quit()

        self.mqtt_receiver.stop_client()
        self.mqtt_receive_thread.quit()

    @Slot(str, dict)
    def handle_send_message(self, topic: str, payload: dict):
        def send_ack():
            val = payload.get('value')
            if isinstance(val, float):
                resp_payload = [payload]
                send_topic = ACK_TOPIC
                payload['value'] = float(f'{payload['value']:.2f}')
            elif isinstance(val, bool):
                resp_payload = [payload]
                send_topic = ACK_TOPIC
                name = payload['name']
                value = payload['value']
                if 'probe' in name and value:
                    if name.endswith('3'):
                        if name.startswith('fuel'):
                            name2 = 'fuel_probe_before_6ka4'
                        elif name.startswith('oil'):
                            name2 = 'oil_probe_before_6ka4'
                    if name.endswith('4'):
                        if name.startswith('fuel'):
                            name2 = 'fuel_probe_after_6ka3'
                        elif name.startswith('oil'):
                            name2 = 'oil_probe_after_6ka3'
                    resp_payload.append({'name': name2, 'value': not value})
            elif isinstance(val, int):
                send_topic = ACK_TOPIC

                if val == 1:
                    resp_payload = [
                        {'name': 'fuel_stand', 'value': False},
                        {'name': 'oil_stand', 'value': True},
                        {'name': 'fuel_probe_after_6ka3', 'value': False, 'disabled': True},
                        {'name': 'fuel_probe_before_6ka4', 'value': False, 'disabled': True},
                        {'name': 'oil_probe_after_6ka3', 'value': False, 'disabled': False},
                        {'name': 'oil_probe_before_6ka4', 'value': False, 'disabled': False},
                    ]
                elif val == 2:
                    resp_payload = [
                        {'name': 'fuel_stand', 'value': True},
                        {'name': 'oil_stand', 'value': False},
                        {'name': 'oil_probe_after_6ka3', 'value': False, 'disabled': True},
                        {'name': 'oil_probe_before_6ka4', 'value': False, 'disabled': True},
                        {'name': 'fuel_probe_after_6ka3', 'value': False, 'disabled': False},
                        {'name': 'fuel_probe_before_6ka4', 'value': False, 'disabled': False},
                    ]
            else:
                return
            try:
                self.mqtt_sender.publish(send_topic, resp_payload)
            finally:
                sender_timer.deleteLater()

        self.mqtt_sender.publish(topic, payload)

        sender_timer = QTimer(self)
        sender_timer.setSingleShot(True)

        sender_timer.timeout.connect(send_ack)
        # i = randint(0, 1)
        # if i:
        #     sender_timer.start(500)
        sender_timer.start(500)

    @Slot(dict)
    def handle_telemetry_message(self, data: dict):
        ts = data.get('timestamp')
        for d in data.get('data'):
            name = d.get('name')
            value = d.get('value')
            tag = self.tag_data.get(name)
            if tag:
                tag.update_value.emit(value)

    @Slot(list)
    def handle_ack_message(self, data: list):
        for d in data:
            name = d.get('name')
            value = d.get('value')
            disabled = d.get('disabled')
            tag = self.tag_data.get(name)
            if tag:
                tag.update_value.emit(value)
                if disabled is not None:
                    tag.set_force_disabled.emit(disabled)
