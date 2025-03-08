import epics
import numpy as np
import paho.mqtt.client as mqtt
import json
import time
import queue

## create queue for event handling
eventqueue = queue.Queue(100)

## functions
def load_config_json(filepath):
    """Loads configuration from a JSON file."""
    with open(filepath, 'r') as f:
        config = json.load(f)
    return config

## load configuration
config = load_config_json('config.json')
mqttconfig = config['mqtt']
mqtttopics = mqttconfig['topics']

## setup epics
pvdic = {}
print("Connecting to EPICS PVs...")
for topic in mqtttopics:
    pvdic[topic] = epics.PV(topic)
time.sleep(2)

## setup MQTT client
## runs on mqtt connection
def on_connect(client, userdata, flags, rc, properties):
    print("Connected with result code " + str(rc))
    for topic in mqtttopics:
        client.subscribe(topic)

def on_message(client, userdata, message):
    payload = message.payload.decode()  # Decode the message payload
    topic = message.topic
    if not eventqueue.full():
        eventqueue.put([topic, payload])

## client setup
print('Attempting to connect to MQTT server ...')
mqclient = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=mqttconfig['client_id'], clean_session=True, transport=mqttconfig['transport'])
mqclient.username_pw_set(mqttconfig['username'], password=mqttconfig['password'])
mqclient.on_connect = on_connect
mqclient.on_message = on_message
mqclient.connect(mqttconfig['host'], port=mqttconfig['port'], keepalive=60)
mqclient.loop_start()
time.sleep(2)

print("Listening... ")
while True:
    q = eventqueue.get()
    try:    
        qpv = pvdic[q[0]]
        qpv.put(q[1])
        # print(q)
    except Exception as err:
        print(err)


print("OK")