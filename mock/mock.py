import json
import random
import time
import threading
import paho.mqtt.client as mqtt

# --- НАСТРОЙКИ ---
BROKER_ADDRESS = "localhost"
BROKER_PORT = 1883
TELEMETRY_TOPIC = 'prism/telemetry'
SET_TOPIC = 'prism/command/set'
ACK_TOPIC = 'prism/command/ack'
SQL_WRITE = 'sql/write'
SQL_READ = 'sql/read'
SQL_DATA = 'sql/data'
INIT_TOPIC = 'prism/init'
PUBLISH_INTERVAL = 0.5


class Indexes:
    current_index = 1


# --- КЛИЕНТ ДЛЯ ОТПРАВКИ ТЕЛЕМЕТРИИ (Publisher) ---
def telemetry_thread_func():
    pub_client = mqtt.Client(
        client_id="telemetry-client",  # ваш уникальный ID
        protocol=mqtt.MQTTv5,  # протокол MQTT v5
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2  # версия колбэков
    )
    pub_client.connect(BROKER_ADDRESS, BROKER_PORT, 60)

    while True:
        current_timestamp = int(time.time() * 1000)
        # print(current_timestamp)

        payload = {
            "timestamp": current_timestamp,
            "data": [
                {"name": "oil_pressure_before", "value": round(random.uniform(20, 80), 1)},
                {"name": "oil_pressure_after", "value": round(random.uniform(20.0, 80.0), 1)},
                {"name": "oil_temperature_before", "value": round(random.uniform(20.0, 80.0), 1)},
                {"name": "oil_temperature_after", "value": round(random.uniform(20, 80), 1)},
                {"name": "oil_moisture_before", "value": round(random.uniform(20.0, 80.0), 1)},
                {"name": "oil_moisture_after", "value": round(random.uniform(20.0, 80.0), 1)},
                {"name": "oil_tank_temperature", "value": round(random.uniform(20, 80), 1)},
                {"name": "oil_main_pump_frequency", "value": round(random.uniform(20.0, 80.0), 1)},
                {"name": "oil_flow_meter", "value": round(random.uniform(20.0, 80.0), 1)},

                {"name": "fuel_pressure_before", "value": round(random.uniform(20, 80), 1)},
                {"name": "fuel_pressure_after", "value": round(random.uniform(20.0, 80.0), 1)},
                {"name": "fuel_temperature_before", "value": round(random.uniform(20.0, 80.0), 1)},
                {"name": "fuel_temperature_after", "value": round(random.uniform(20, 80), 1)},
                {"name": "fuel_moisture_before", "value": round(random.uniform(20.0, 80.0), 1)},
                {"name": "fuel_moisture_after", "value": round(random.uniform(20.0, 80.0), 1)},
                {"name": "fuel_tank_temperature", "value": round(random.uniform(20, 80), 1)},
                {"name": "fuel_main_pump_frequency", "value": round(random.uniform(20.0, 80.0), 1)},
                {"name": "fuel_flow_meter", "value": round(random.uniform(20.0, 80.0), 1)},

                {'name': 'pressure_diff_1', 'value': round(random.uniform(2, 10), 1)},
                {'name': 'fuel_consumption_1', 'value': round(random.uniform(20, 40), 1)},

                {'name': 'oil_effectiveness', 'value': random.randint(50, 99)},

                # {'name': f'oil_before.2um_2', 'value': random.randint(100000, 999999)},
                # {'name': f'oil_after.2um_2', 'value': random.randint(100000, 999999)},
                # {'name': f'oil_before.150um_3', 'value': random.randint(100000, 999999)},
                # {'name': f'oil_after.200um_3', 'value': random.randint(100000, 999999)},
                # {'name': f'oil_before.15um_5', 'value': random.randint(100000, 999999)},

                # {'name': f'oil_effectiveness_3', 'value': random.randint(70, 90)},
                # {'name': f'fuel_effectiveness_4', 'value': random.randint(40, 60)},
            ]
        }

        # pub_client.publish(TELEMETRY_TOPIC, json.dumps(payload), qos=0)
        # print(f"[OUT] Telemetry sent")
        time.sleep(PUBLISH_INTERVAL)


# --- КЛИЕНТ ДЛЯ ПРИЕМА КОМАНД И ОТВЕТА (Subscriber) ---
def command_thread_func():
    sub_client = mqtt.Client(
        client_id="command-client",  # ваш уникальный ID
        protocol=mqtt.MQTTv5,  # протокол MQTT v5
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2  # версия колбэков
    )
    sub_client.connect(BROKER_ADDRESS, BROKER_PORT, 60)

    def on_message(client, userdata, msg):
        topic = msg.topic
        if topic == SET_TOPIC:
            try:
                data = json.loads(msg.payload.decode())

                payload = data.get('data')

                if isinstance(payload, dict):

                    ns_name = payload.get('ns_name')
                    name = payload.get('name')
                    value = payload.get('value')

                    print('here with', payload)

                    send_topic = ACK_TOPIC
                    val = payload.get('value')
                    if isinstance(val, float):
                        resp_payload = [payload]
                        payload['value'] = float(f'{payload['value']:.2f}')
                    elif isinstance(val, bool):
                        resp_payload = [payload]
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
                        elif name in ('oil_select_before', 'fuel_select_before', 'fuel_select_after',
                                      'oil_select_after'):
                            stand_prefix, _, position = name.split('_')
                            index = payload.get('index')
                            if index is not None:
                                Indexes.current_index = int(index)
                            resp_payload = [
                                {'name': name, 'value': value}
                            ]
                            second_value = f'{stand_prefix}_select_{'before' if position == 'after' else 'after'}'
                            resp_payload.append({'name': second_value, 'value': False})

                            if position == 'before' and value:
                                add_data = [
                                    {'name': f'{stand_prefix}_probe_after_6ka3', 'value': value},
                                    {'name': f'{stand_prefix}_probe_before_6ka4', 'value': not value}
                                ]
                            elif position == 'after' and value:
                                add_data = [
                                    {'name': f'{stand_prefix}_probe_after_6ka3', 'value': not value},
                                    {'name': f'{stand_prefix}_probe_before_6ka4', 'value': value}
                                ]
                            elif not value:
                                add_data = [
                                    {'name': f'{stand_prefix}_probe_after_6ka3', 'value': value},
                                    {'name': f'{stand_prefix}_probe_before_6ka4', 'value': value}
                                ]

                            resp_payload.extend(add_data)


                    elif val is None:
                        if 'test' in name:
                            table_prefix = name.split('_')[0]
                            prefix = name.split('_')[2]
                            resp_payload = [
                                {'name': name, 'value': False}
                            ]
                            index = Indexes.current_index

                            resp_payload.extend([
                                {'name': f'{table_prefix}_{prefix}.2um_{index}',
                                 'value': random.randint(100000, 999999)},
                                {'name': f'{table_prefix}_{prefix}.3um_{index}',
                                 'value': random.randint(100000, 999999)},
                                {'name': f'{table_prefix}_{prefix}.4um_{index}',
                                 'value': random.randint(100000, 999999)},
                                {'name': f'{table_prefix}_{prefix}.5um_{index}',
                                 'value': random.randint(100000, 999999)},
                                {'name': f'{table_prefix}_{prefix}.6um_{index}',
                                 'value': random.randint(100000, 999999)},
                                {'name': f'{table_prefix}_{prefix}.7um_{index}',
                                 'value': random.randint(100000, 999999)},
                                {'name': f'{table_prefix}_{prefix}.8um_{index}',
                                 'value': random.randint(100000, 999999)},
                                {'name': f'{table_prefix}_{prefix}.10um_{index}',
                                 'value': random.randint(100000, 999999)},
                                {'name': f'{table_prefix}_{prefix}.15um_{index}',
                                 'value': random.randint(100000, 999999)},
                                {'name': f'{table_prefix}_{prefix}.20um_{index}',
                                 'value': random.randint(100000, 999999)},
                                {'name': f'{table_prefix}_{prefix}.25um_{index}',
                                 'value': random.randint(100000, 999999)},
                                {'name': f'{table_prefix}_{prefix}.30um_{index}',
                                 'value': random.randint(100000, 999999)},
                                {'name': f'{table_prefix}_{prefix}.50um_{index}',
                                 'value': random.randint(100000, 999999)},
                                {'name': f'{table_prefix}_{prefix}.100um_{index}',
                                 'value': random.randint(100000, 999999)},
                                {'name': f'{table_prefix}_{prefix}.150um_{index}',
                                 'value': random.randint(100000, 999999)},
                                {'name': f'{table_prefix}_{prefix}.200um_{index}',
                                 'value': random.randint(100000, 999999)},
                                {'name': f'{table_prefix}_{prefix}.class_{index}', 'value': 17},
                                {'name': f'{table_prefix}_{prefix}_index_{index}', 'value': 1}
                            ])
                            resp_payload.extend([{'name': f'{table_prefix}_{prefix}_index', 'value': index},
                                                 {'name': f'{table_prefix}_select_{prefix}', 'value': False}])

                    elif isinstance(val, int):
                        if 'index' in name:
                            if val != 3:
                                resp_payload = [
                                    {'name': name, 'value': val},
                                ]
                                current_timestamp = int(time.time() * 1000)
                                final_payload = {
                                    "timestamp": current_timestamp,
                                    "data": resp_payload
                                }
                            else:
                                stand_prefix, position, _, index = name.split('_')
                                val = 1
                                resp_payload = [
                                    {'name': name, 'value': val},
                                ]
                                current_timestamp = int(time.time() * 1000)
                                final_payload = {
                                    "timestamp": current_timestamp,
                                    "data": resp_payload
                                }
                                print(final_payload)

                                time.sleep(0.5)

                                client.publish(SQL_WRITE, json.dumps(final_payload), qos=1)

                                client.publish(
                                    topic=SQL_READ,
                                    payload=json.dumps({
                                        'includes': [stand_prefix, position],
                                        'excludes': None,
                                        'startswith': None,
                                        'endswith': f'_{index}'
                                    }),
                                    qos=1,
                                    retain=False
                                )
                                return
                        else:
                            if val == 1:
                                resp_payload = [
                                    {'name': 'stand_select', 'value': 1},
                                    {'name': 'fuel_probe_after_6ka3', 'value': False, 'disabled': True},
                                    {'name': 'fuel_probe_before_6ka4', 'value': False, 'disabled': True},
                                    {'name': 'fuel_probe_disabled', 'value': True},
                                    {'name': 'oil_probe_after_6ka3', 'value': False, 'disabled': False},
                                    {'name': 'oil_probe_before_6ka4', 'value': False, 'disabled': False},
                                    {'name': 'oil_probe_disabled', 'value': False},
                                ]
                            elif val == 2:
                                resp_payload = [
                                    {'name': 'stand_select', 'value': 2},
                                    {'name': 'oil_probe_after_6ka3', 'value': False, 'disabled': True},
                                    {'name': 'oil_probe_before_6ka4', 'value': False, 'disabled': True},
                                    {'name': 'oil_probe_disabled', 'value': True},
                                    {'name': 'fuel_probe_after_6ka3', 'value': False, 'disabled': False},
                                    {'name': 'fuel_probe_before_6ka4', 'value': False, 'disabled': False},
                                    {'name': 'fuel_probe_disabled', 'value': False},
                                ]
                    else:
                        return

                elif isinstance(payload, list):
                    resp_payload = payload

                time.sleep(0.5)

                current_timestamp = int(time.time() * 1000)
                final_payload = {
                    "timestamp": current_timestamp,
                    "data": resp_payload
                }

                # Отправка ответа
                client.publish(ACK_TOPIC, json.dumps(final_payload), qos=1)
                client.publish(SQL_WRITE, json.dumps(final_payload), qos=1)
                print(f"[OUT] Response sent : {final_payload}")

            except Exception as e:
                print(f"Error handling message: {e}")
        elif topic == INIT_TOPIC:
            print('GOT INIT, REQUESTING DB')
            client.publish(
                topic=SQL_READ,
                payload=None,
                qos=1,
                retain=False
            )
        elif topic == SQL_DATA:
            payload = msg.payload.decode()
            print(f"[IN ] SQL DATA received")
            result = client.publish(
                topic=ACK_TOPIC,
                payload=msg.payload
            )
            if result.rc == 0:
                print('SQL DATA SENDED TO FRONTEND')
            else:
                print(f'FAILED {result.rc}')

    sub_client.on_message = on_message
    sub_client.subscribe(SET_TOPIC, qos=1)
    sub_client.subscribe(SQL_DATA, qos=1)
    sub_client.subscribe(INIT_TOPIC, qos=1)

    sub_client.loop_start()


# --- ЗАПУСК ---
if __name__ == "__main__":
    t_telemetry = threading.Thread(target=telemetry_thread_func, daemon=True)
    t_commands = threading.Thread(target=command_thread_func, daemon=True)

    t_telemetry.start()
    t_commands.start()

    print("Mock Server running...")

    try:
        t_telemetry.join()
        t_commands.join()
    except KeyboardInterrupt:
        print("\nServer stopped by user.")