import json

import paho.mqtt.client as mqtt
from PySide6.QtCore import QObject, Signal, QTimer
from paho.mqtt.enums import MQTTErrorCode


class MQTTClient(QObject):
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
    telemetry_message = Signal(dict)
    telemetry_timeout_error = Signal()
    ack_message = Signal(list)

    def __init__(
            self,
            host='localhost',
            port=1883,
            telemetry_topic=None,
            ack_topic=None
    ):
        super().__init__(host, port, 'receive_client')

        self.telemetry_topic = telemetry_topic
        self.ack_topic = ack_topic

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
            client.subscribe(self.telemetry_topic, qos=0)
            client.subscribe(self.ack_topic, qos=0)
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
        if topic == self.telemetry_topic:
            self.telemetry_message.emit(data)
        elif topic == self.ack_topic:
            print(f'[IN] Recieved from {topic}: {data}')
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

    def connect_and_run(self):
        print("[SENDER] Connecting...")
        self.client.connect(self.host, self.port, 60)
        self.client.loop_start()

    def stop_client(self):
        print("[SENDER] Stopping...")
        try:
            self.client.disconnect()
        except Exception:
            pass

    def publish(self, topic: str, payload: dict):
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
