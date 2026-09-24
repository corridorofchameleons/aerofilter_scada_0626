import orjson
import paho.mqtt.client as mqtt
from PySide6.QtCore import QObject, Signal
from paho.mqtt.enums import MQTTErrorCode

from app.data.topics import TELEMETRY_TOPIC


class MQTTClient(QObject):
    receiver_connected = Signal()
    sender_connected = Signal()

    def __init__(
            self,
            host,
            port,
            client_id,
    ):
        super().__init__()
        self.host = host
        self.port = port

        self.client = mqtt.Client(
            client_id=client_id,
            protocol=mqtt.MQTTv5,
            callback_api_version=mqtt.CallbackAPIVersion.VERSION2
        )

class MQTTReceiver(MQTTClient):
    message = Signal(str, dict)

    def __init__(
            self,
            host='localhost',
            port=1883,
            topics: tuple[str, ...] = None,
    ):
        super().__init__(host, port, 'receive_client')

        self.topics = topics

        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message

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
            for topic in self.topics:
                client.subscribe(topic, qos=0)
            self.receiver_connected.emit()
        else:
            print(f"[WORKER] Connect failed with code {rc}")

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
        self.message.emit(topic, data)

    def publish(self, topic: str, payload: dict | None):
        if payload is not None:
            payload = orjson.dumps(payload)
        try:
            result = self.client.publish(
                topic=topic,
                payload=payload,
                qos=1,
                retain=False
            )
            success = True if result.rc == MQTTErrorCode.MQTT_ERR_SUCCESS else False
            if success:
                print(f"[OUT] Sent to {topic}: {payload}")
            else:
                print(f"FAILED TO SEND {result.rc}")

        except Exception as e:
            print(f"[WORKER] Publish error: {e}")

    @staticmethod
    def _parse_payload(payload_bytes):
        try:
            return orjson.loads(payload_bytes.decode('utf-8'))
        except Exception:
            return None

class MQTTSender(MQTTClient):
    def __init__(self,
            host='localhost',
            port=1883,
    ):
        super().__init__(host, port, 'send_client')
        self.client.on_connect = self._on_connect

    def connect_and_run(self):
        print("[SENDER] Connecting...")
        self.client.connect(self.host, self.port, 60)
        self.client.loop_start()

    def _on_connect(self, client, userdata, flags, rc, props=None):
        print('[SENDER] connected')
        self.sender_connected.emit()

    def stop_client(self):
        print("[SENDER] Stopping...")
        try:
            self.client.disconnect()
        except Exception:
            pass

    def publish(self, topic: str, payload: dict | None):
        if payload is not None:
            payload = orjson.dumps(payload)
        try:
            result = self.client.publish(
                topic=topic,
                payload=payload,
                qos=1,
                retain=False
            )
            success = True if result.rc == MQTTErrorCode.MQTT_ERR_SUCCESS else False
            if success:
                print(f"[OUT] Sent to {topic}: {payload}")
            else:
                print(f"FAILED TO SEND {result.rc}")

        except Exception as e:
            print(f"[WORKER] Publish error: {e}")
