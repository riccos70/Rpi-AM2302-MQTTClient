# AM2302 sending data into MQTT broker on Rpi device

import random
import time
import json
import Adafruit_DHT
from paho.mqtt import client as mqtt_client

with open('config.json', 'r') as f:
    config = json.load(f)

# Fill in MQTT Broker details
mqtt_host = config['MQTT']['HOST']
mqtt_username = config['MQTT']['USERNAME']
mqtt_port = config['MQTT']['PORT']
mqtt_password = config['MQTT']['PASSWORD']
mqtt_publish_topic_01 = "casagrotti/sala/temperatura/sens01"  # The MQTT topic
mqtt_publish_topic_02 = "casagrotti/sala/umidita/sens01"  # The MQTT topic
# Generate a Client ID with the publish prefix.
mqtt_client_id = f'publish-{random.randint(0, 1000)}'

# Fill in DHT sensor details
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = config['DHT']['PIN_NUMBER']

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

def readDHT():
    try:        
        hum, temp = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
#        print(f'Temperature= {temp:.1f} C')
#        print(f'Humidity= {hum:.1f} %')
        return temp, hum
    except OSError as e:
        print('Failed to read data from DHT sensor')

def publish(client):
    while True:
        time.sleep(30)
        t,u = readDHT() 
        result1 = client.publish(mqtt_publish_topic_01, t)
        result2 = client.publish(mqtt_publish_topic_02, u)
        # result: [0, 1]
        status1 = result1[0]
        if status1 == 0:
            print(f"Send `{t}` to topic `{mqtt_publish_topic_01}`")
        else:
            print(f"Failed to send message to topic {mqtt_publish_topic_01}")
        status2 = result2[0]
        if status2 == 0:
            print(f"Send `{u}` to topic `{mqtt_publish_topic_02}`")
        else:
            print(f"Failed to send message to topic {mqtt_publish_topic_02}")


def run():
    client = connect_mqtt()
    publish(client)


if __name__ == '__main__':
    run()
