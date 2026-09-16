import json

import paho.mqtt.client as mqtt
from PySide6.QtCore import QObject, Signal, Slot, QTimer
from paho.mqtt.enums import MQTTErrorCode

from app.data.topics import TELEMETRY_TOPIC, ACK_TOPIC
# from core.services.mqtt_handler import mqtt_handler
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

        # self.handler = mqtt_handler

        self.client = mqtt.Client(
            client_id=client_id,
            protocol=mqtt.MQTTv5,
            callback_api_version=mqtt.CallbackAPIVersion.VERSION2
        )


class MQTTReceiver(MQTTClient):
    telemetry_message = Signal(dict)
    ack_message = Signal(list)

    def __init__(
            self,
            host='localhost',
            port=1883,
            telemetry_topic=TELEMETRY_TOPIC,
            ack_topic=ACK_TOPIC
    ):
        super().__init__(host, port, 'receive_client')

        self.telemetry_topic = telemetry_topic
        self.ack_topic = ack_topic

        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message

        # self.telemetry_message.connect(self.handler.handle_telemetry_message)
        # self.ack_message.connect(self.handler.handle_ack_message)


    @Slot()
    def connect_and_run(self):
        print("[WORKER] Thread started")
        try:
            self.client.connect(self.host, self.port, 60)
            self.client.loop_start()
        except Exception as e:
            print(f"[WORKER] Network error: {e}")

    def _on_connect(self, client, userdata, flags, rc, props=None):
        if rc == 0:
            print("[WORKER] Connected to broker")
            client.subscribe(self.telemetry_topic, qos=0)
            client.subscribe(self.ack_topic, qos=0)
        else:
            print(f"[WORKER] Connect failed with code {rc}")

    @Slot()
    def stop_client(self):
        print("[RECEIVER] Stopping...")
        try:
            sock = self.client.socket()
            if sock:
                sock.close()
        except Exception:
            pass
        self.client.disconnect()


    def _on_message(self, client, userdata, msg):
        topic: str = msg.topic
        data = self._parse_payload(msg.payload)
        if topic == self.telemetry_topic:
            self.telemetry_message.emit(data)
        elif topic == self.ack_topic:
            self.ack_message.emit(data)

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
            self.client.disconnect()
        except Exception:
            pass


    @Slot(str, dict)
    def publish(self, topic: str, payload: dict):
        def send_status():
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
                if 'counter' in name and 'valve' in name and value:
                    if name.endswith('counter_before_valve'):
                        name = name.replace('before', 'after')
                    elif name.endswith('counter_after_valve'):
                        name = name.replace('after', 'before')
                    resp_payload.append({'name': name, 'value': not value})
            elif isinstance(val, int):
                send_topic = ACK_TOPIC

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
