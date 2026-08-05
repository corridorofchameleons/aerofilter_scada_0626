import json
import paho.mqtt.client as mqtt
from PySide6.QtCore import QObject


class MQTTClient:
    def __init__(
            self,
            host='localhost',
            port=1883
    ):
        self.client = mqtt.Client(protocol=mqtt.MQTTv5)
        self.host = host
        self.port = port

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def connect(self):
        self.client.connect(self.host, self.port, 60)
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc, properties=None):
        if rc == 0:
            print("MQTT: Подключено")
            client.subscribe("plc1/telemetry", qos=0)
        else:
            print(f"MQTT: Ошибка {rc}")

    def on_message(self, client, userdata, msg):
        print(f"[{msg.topic}] {self._parse_payload(msg.payload)}")

    @staticmethod
    def _parse_payload(payload_bytes):
        try:
            return json.loads(payload_bytes.decode('utf-8'))
        except Exception:
            return None


class MQTTWorker(QObject):
    def __init__(
        self,
        client: MQTTClient
    ):
        super().__init__()
        self.client = client