# AM2302 sending data into MQTT broker on Rpi device

import random
import time
import json
import adafruit_dht
import board
import sys

sys.path.append('libs/shared_lib')

from log_manager import printLog 
from paho.mqtt import client as mqtt_client

with open('config.json', 'r') as f:
    config = json.load(f)

# Fill in MQTT Broker details
mqtt_host = config['MQTT']['HOST']
mqtt_username = config['MQTT']['USERNAME']
mqtt_password = config['MQTT']['PASSWORD']
mqtt_port = config['MQTT']['PORT']
ttype = config['TOPIC']['TYPE']
tarea = config['TOPIC']['AREA']
# tzone = config['TOPIC']['ZONE']
tzone1 = 'torre'
tzone2 = 'giardino'
# sensor_pin = config['SENSOR']['PIN']
# sensor_pin = 'D10 giardino D4 torre'
# mqtt_publish_topic = ttype+"/"+tarea+"/"+tzone
mqtt_publish_topic1 = ttype+"/"+tarea+"/"+tzone1
mqtt_publish_topic2 = ttype+"/"+tarea+"/"+tzone2
mqtt_client_id = f'publish-{random.randint(0, 1000)}'


# Fill in DHT sensor details
# sensor = adafruit_dht.DHT22(board.D4)
sensor1 = adafruit_dht.DHT22(board.D4)
sensor2 = adafruit_dht.DHT22(board.D10)
mis01 = config['DATA']['MEAS01']
mis02 = config['DATA']['MEAS02']

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            printLog("INFO","Connected to MQTT Broker!")
        else:
            printLog("ERR","Connected to MQTT Broker!")

    client = mqtt_client.Client(mqtt_client_id)
    client.username_pw_set(mqtt_username, mqtt_password)
    client.on_connect = on_connect
    client.connect(mqtt_host, mqtt_port)
    return client

def readDHT(s):
    try:        
        h = s.humidity 
        t = s.temperature 
        temp = round(t,1)
        hum = round(h,1) 
        return temp, hum
    except OSError as e:
        printLog("ERR","Failed to read data from AM2302 sensor")

def publish(client):
    while True:
        time.sleep(30)
        # t,u = readDHT()
        t1,u1 = readDHT(sensor1)
        t2,u2 = readDHT(sensor2)
    #   msg = "{\"area\": \""+tarea+"\", \"zone\": \""+tzone+"\", \""+mis01+"\": " + str(t) + ", \""+mis02+"\": " + str(u) + "}"
        msg1 = "{\"area\": \""+tarea+"\", \"zone\": \""+tzone1+"\", \""+mis01+"\": " + str(t1) + ", \""+mis02+"\": " + str(u1) + "}"
        msg2 = "{\"area\": \""+tarea+"\", \"zone\": \""+tzone2+"\", \""+mis01+"\": " + str(t2) + ", \""+mis02+"\": " + str(u2) + "}"
        # result = client.publish(mqtt_publish_topic, msg)
        # status = result[0]
        # if status == 0:
        #     printLog("INFO","Sent "+msg+" to topic "+mqtt_publish_topic)
        # else:
        #     printLog("ERR","Failed to send message to topic "+mqtt_publish_topic)
        result1 = client.publish(mqtt_publish_topic1, msg1)
        status = result1[0]
        if status == 0:
            printLog("INFO","Sent "+msg1+" to topic "+mqtt_publish_topic1)
        else:
            printLog("ERR","Failed to send message to topic "+mqtt_publish_topic1)
        result2 = client.publish(mqtt_publish_topic2, msg2)
        status = result2[0]
        if status == 0:
            printLog("INFO","Sent "+msg2+" to topic "+mqtt_publish_topic2)
        else:
            printLog("ERR","Failed to send message to topic "+mqtt_publish_topic2)    


def run():
    client = connect_mqtt()
    publish(client)


if __name__ == '__main__':
    run()
