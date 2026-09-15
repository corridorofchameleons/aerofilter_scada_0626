import json

import paho.mqtt.client as mqtt
from PySide6.QtCore import QObject, Signal, Slot, QTimer
from paho.mqtt.enums import MQTTErrorCode

from core.connectors.topics import STATUS_TOPIC, VALUE_TOPIC, TELEMETRY_TOPIC
from core.services.mqtt_handler import mqtt_handler
from core.signals.mqtt import bus


class MQTTClient(QObject):
    def __init__(
            self,
            host,
            port,
            client_id
    ):
        super().__init__()
        self.host = host
        self.port = port

        self.handler = mqtt_handler

        self.client = mqtt.Client(
            client_id=client_id,
            protocol=mqtt.MQTTv5,
            callback_api_version=mqtt.CallbackAPIVersion.VERSION2
        )


class MQTTReceiver(MQTTClient):
    telemetry_message = Signal(dict)
    status_message = Signal(list)
    value_message = Signal(dict)

    def __init__(
            self,
            host='localhost',
            port=1883,
            telemetry_topic=TELEMETRY_TOPIC,
            status_topic=STATUS_TOPIC,
            value_topic=VALUE_TOPIC
    ):
        super().__init__(host, port, 'receive_client')

        self.telemetry_topic = telemetry_topic
        self.status_topic = status_topic
        self.value_topic = value_topic

        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message

        self.telemetry_message.connect(self.handler.handle_telemetry_message)
        self.status_message.connect(self.handler.handle_status_message)
        self.value_message.connect(self.handler.handle_value_message)


    @Slot()
    def connect_and_run(self):
        print("[WORKER] Thread started")
        try:
            self.client.connect(self.host, self.port, 60)
            self.client.loop_forever()
        except Exception as e:
            print(f"[WORKER] Network error: {e}")

    def _on_connect(self, client, userdata, flags, rc, props=None):
        if rc == 0:
            print("[WORKER] Connected to broker")
            client.subscribe(self.telemetry_topic, qos=0)
            client.subscribe(self.status_topic, qos=0)
            client.subscribe(self.value_topic, qos=0)
        else:
            print(f"[WORKER] Connect failed with code {rc}")

    @Slot()
    def stop_client(self):
        print("[WORKER] Stop signal received.")
        self.client.disconnect()

    def _on_message(self, client, userdata, msg):
        topic: str = msg.topic
        data = self._parse_payload(msg.payload)

        match topic:
            case self.telemetry_topic:
                self.telemetry_message.emit(data)
            case self.status_topic:
                self.status_message.emit(data)
            case self.value_topic:
                self.value_message.emit(data)

    @staticmethod
    def _parse_payload(payload_bytes):
        try:
            return json.loads(payload_bytes.decode('utf-8'))
        except Exception:
            return None


class MQTTSender(MQTTClient):
    on_off_signal = Signal(bool, dict)

    def __init__(self,
            host='localhost',
            port=1883
    ):
        super().__init__(host, port, 'send_client')

        bus.mqtt_publish_signal.connect(self.publish)

    @Slot()
    def connect_and_run(self):
        print("[SENDER] Connecting...")
        self.client.connect(self.host, self.port, 60)
        self.client.loop_start()

    @Slot()
    def stop_client(self):
        print("[SENDER] Stopping...")
        try:
            if self.client.is_connected():
                self.client.disconnect()  # Просим корректно завершить сессию
        except Exception as e:
            print(f"Disconnect error: {e}")
        self.client.loop_stop()

    @Slot(str, dict)
    def publish(self, topic: str, payload: dict):
        def send_status():
            val = payload.get('value')
            if isinstance(val, float):
                resp_payload = payload
                send_topic = VALUE_TOPIC
                payload['value'] = float(f'{payload['value']:.2f}')
            elif isinstance(val, bool):
                resp_payload = [payload]
                send_topic = STATUS_TOPIC
                name = payload['name']
                value = payload['value']
                if 'counter' in name and 'valve' in name and value:
                    if name.endswith('counter_before_valve'):
                        name = name.replace('before', 'after')
                    elif name.endswith('counter_after_valve'):
                        name = name.replace('after', 'before')
                    resp_payload.append({'name': name, 'value': not value})
            elif isinstance(val, int):
                send_topic = STATUS_TOPIC

                if val == 1:
                    resp_payload = [
                        {'name': 'fuel_stand', 'value': False},
                        {'name': 'oil_stand', 'value': True},
                        {'name': 'fuel_counter_after_valve', 'value': False, 'disabled': True},
                        {'name': 'fuel_counter_before_valve', 'value': False, 'disabled': True},
                        {'name': 'oil_counter_after_valve', 'value': False, 'disabled': False},
                        {'name': 'oil_counter_before_valve', 'value': False, 'disabled': False},
                    ]
                elif val == 2:
                    resp_payload = [
                        {'name': 'fuel_stand', 'value': True},
                        {'name': 'oil_stand', 'value': False},
                        {'name': 'fuel_counter_after_valve', 'value': True, 'disabled': False},
                        {'name': 'fuel_counter_before_valve', 'value': False, 'disabled': False},
                        {'name': 'oil_counter_after_valve', 'value': False, 'disabled': True},
                        {'name': 'oil_counter_before_valve', 'value': False, 'disabled': True},
                    ]
            else:
                return
            try:
                send_result = self.client.publish(
                    topic=send_topic,
                    payload=json.dumps(resp_payload),
                    qos=1,
                    retain=False
                )
                send_success = True if send_result.rc == MQTTErrorCode.MQTT_ERR_SUCCESS else False
                if send_success:
                    print(f"[OUT] Sent further to {send_topic}: {resp_payload}")
            finally:
                sender_timer.deleteLater()

        try:
            result = self.client.publish(
                topic=topic,
                payload=json.dumps(payload),
                qos=1,
                retain=False
            )
            success = True if result.rc == MQTTErrorCode.MQTT_ERR_SUCCESS else False
            if success:
                print(f"[OUT] Sent to {topic}: {payload}")

        except Exception as e:
            print(f"[WORKER] Publish error: {e}")

        sender_timer = QTimer(self)
        sender_timer.setSingleShot(True)

        sender_timer.timeout.connect(send_status)
        sender_timer.start(500)
