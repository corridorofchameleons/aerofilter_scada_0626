import json
import time

import paho.mqtt.client as mqtt
from PySide6.QtCore import QObject, Signal, Slot, QTimer
from paho.mqtt.enums import MQTTErrorCode

from mqtt.mqtt_handler import mqtt_handler
from mqtt.topics import TELEMETRY_TOPIC
from signals.signal_bus import bus


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

    def __init__(
            self,
            host='localhost',
            port=1883
    ):
        super().__init__(host, port, 'receive_client')

        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message

        self.telemetry_message.connect(self.handler.handle_telemetry_message)


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
            client.subscribe(TELEMETRY_TOPIC, qos=0)
        else:
            print(f"[WORKER] Connect failed with code {rc}")

    @Slot()
    def stop_client(self):
        print("[WORKER] Stop signal received.")
        self.client.disconnect()

    def _on_message(self, client, userdata, msg):
        topic = msg.topic
        topic_parts = topic.split('/')
        if topic_parts[1] == 'telemetry':
            data = self._parse_payload(msg.payload)
            self.telemetry_message.emit(data)

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
        self.on_off_signal.connect(self.handler.handle_on_off_command)

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
        def execute_publish():
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
                    self.on_off_signal.emit(success, payload)
            except Exception as e:
                print(f"[WORKER] Publish error: {e}")
            finally:
                sender_timer.deleteLater()

        sender_timer = QTimer(self)
        sender_timer.setSingleShot(True)

        sender_timer.timeout.connect(execute_publish)
        sender_timer.start(1000)
