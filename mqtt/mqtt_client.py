import json
import paho.mqtt.client as mqtt
from PySide6.QtCore import QObject, Signal, Slot

from mqtt.mqtt_handler import mqtt_handler


class MQTTClient(QObject):
    finished = Signal()
    telemetry_message = Signal(dict)

    def __init__(self, host='localhost', port=1883):
        super().__init__()
        self.host = host
        self.port = port

        self.client = mqtt.Client(protocol=mqtt.MQTTv5)
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message

        self.handler = mqtt_handler
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
            client.subscribe("plc1/telemetry", qos=0)
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
