# AM2302 sending data into MQTT broker on Rpi device

import json
import Adafruit_DHT
import time
from paho.mqtt import client as mqtt_client

with open('config.json', 'r') as f:
    config = json.load(f)

# Fill in MQTT Broker details
mqtt_host = config['MQTT']['HOST']
mqtt_username = config['MQTT']['USERNAME']
mqtt_port = config['MQTT']['PORT']
mqtt_password = config['MQTT']['PASSWORD']
mqtt_publish_temp_topic = "casagrotti/sala/temperatura/sens01"  # The MQTT topic
mqtt_publish_hum_topic = "casagrotti/sala/umidita/sens01"  # The MQTT topic
mqtt_client_id = "Rpi3-001"

# Initialize our MQTTClient and connect to the MQTT server
def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(mqtt_client_id)
    client.username_pw_set(mqtt_username, mqtt_password)
    client.on_connect = on_connect
    client.connect(mqtt_host, mqtt_port)
    return client

client = connect_mqtt()

# Fill in DHT sensor details
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = config['DHT']['PIN_NUMBER']

def readDHT():
    try:        
        hum, temp = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
#        print(f'Temperature= {temp:.1f} C')
#        print(f'Humidity= {hum:.1f} %')
        return temp, hum
    except OSError as e:
        print('Failed to read data from DHT sensor')
    
def publishData(t,h):
    try:
        client.publish(mqtt_publish_temp_topic, str(t))
        client.publish(mqtt_publish_hum_topic, str(h))
        print(f'Publish {t:.1f}')
        print(f'Publish {h:.1f}')
    except Exception as e:
        print(f'Failed to publish message: {e}')

while True:
    # Read the data from sensor
    temp, hum= readDHT()
    # Publish the data to the topic
    publishData(temp, hum)
    time.sleep(60)
