import tango
import time
import json
import paho.mqtt.client as mqtt
import queue

## create queue for event handling
eventqueue = queue.Queue(100)

## functions
def load_config_json(filepath):
    """Loads configuration from a JSON file."""
    with open(filepath, 'r') as f:
        config = json.load(f)
    return config

def get_attr_name(name):
    return '/'.join(name.split('/')[-4:])

def tangoUpdateEvent(event_data):
    if event_data.err == False:
        eventqueue.put([get_attr_name(event_data.attr_name), event_data.attr_value.value])
        #print(f"{get_attr_name(event_data.attr_name)} = {event_data.attr_value.value}")

## load configuration
config = load_config_json('config.json')
mqttconfig = config['mqtt']
tangoconfig = config['tango']

## create a new Tango client
labstatus = tango.DeviceProxy(tangoconfig['device'])
attributelist = labstatus.get_attribute_list()

## setup callback for Tango events
eventIDlist = []
for attr in attributelist:
    id = labstatus.subscribe_event(attr, tango.EventType.CHANGE_EVENT, tangoUpdateEvent)
    eventIDlist.append(id)

## setup MQTT client
## runs on mqtt connection
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

## client setup
print('Attempting to connect to MQTT server ...')
mqclient = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, client_id=mqttconfig['client_id'], clean_session=True, transport=mqttconfig['transport'])
mqclient.username_pw_set(mqttconfig['username'], password=mqttconfig['password'])
mqclient.on_connect = on_connect
mqclient.connect(mqttconfig['host'], port=mqttconfig['port'], keepalive=60)
mqclient.loop_start()
time.sleep(2)

## main loop
try:
    print(f"[{time.asctime()}] Listening to Tango device {tangoconfig['device']}...")
    while(True):
        eve = eventqueue.get()
        #print(eve)
        topic = eve[0]
        payload = eve[1]
        mqclient.publish(topic, payload=payload, qos=0, retain=False)
        
except KeyboardInterrupt:
    print("\nExiting...")
except Exception as e:
    print("Error: " + str(e))

print("OK")