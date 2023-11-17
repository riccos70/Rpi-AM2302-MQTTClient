# AM2302 with display and MQTT on PICO W device

import ujson
import dht 
import network
import time
from ssd1306 import SSD1306_I2C
from machine import Pin, I2C
from umqtt.simple import MQTTClient

with open('config.json', 'r') as f:
    config = ujson.load(f)

# Fill in your WiFi network name (ssid) and password here:
wifi_ssid = config['WIFI']['SSID']
wifi_password = config['WIFI']['PASSWORD']

# Connect to WiFi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(wifi_ssid, wifi_password)
while wlan.isconnected() == False:
    print('Waiting for connection...')
    time.sleep(1)
print("Connected to WiFi")

# Fill in your MQTT Broker details
mqtt_host = config['MQTT']['HOST']
mqtt_username = config['MQTT']['USERNAME']  
mqtt_password = config['MQTT']['PASSWORD']
mqtt_publish_temp_topic = "casagrotti/sala/temperatura/sens01"  # The MQTT topic
mqtt_publish_hum_topic = "casagrotti/sala/umidita/sens01"  # The MQTT topic
# Enter a random ID for this MQTT Client
mqtt_client_id = "00000002"

# Initialize our MQTTClient and connect to the MQTT server
mqtt_client = MQTTClient(
        client_id=mqtt_client_id,
        server=mqtt_host,
        user=mqtt_username,
        password=mqtt_password)

mqtt_client.connect()

dSensor = dht.DHT22(Pin(2))

WIDTH =128 
HEIGHT= 64
i2c=I2C(0,scl=Pin(1),sda=Pin(0),freq=200000)
oled = SSD1306_I2C(WIDTH,HEIGHT,i2c)

def readDHT():
    try:
        dSensor.measure()
        temp = dSensor.temperature()
        temp_f = (temp * (9/5)) + 32.0
        hum = dSensor.humidity()
        print('Temperature= {} C, {} F'.format(temp, temp_f))
        print('Humidity= {} '.format(hum))
        return temp, hum
    except OSError as e:
        print('Failed to read data from DHT sensor')

def printDhtData(t,h):
    oled.fill(0)
    oled.text("Temp:", 0, 10)
    oled.text(str(t), 80, 10)
    oled.text("C", 120, 10)
    oled.text("Humidity:", 0, 30)
    oled.text(str(h), 80, 30)
    oled.text("%", 120, 30)
    oled.show()
    
def publishData(t,h):
    try:
        mqtt_client.publish(mqtt_publish_temp_topic, str(t))
        mqtt_client.publish(mqtt_publish_hum_topic, str(h))
        print(f'Publish {t:.1f}')
        print(f'Publish {h:.1f}')
    except Exception as e:
        print(f'Failed to publish message: {e}')
#    finally:
#        mqtt_client.disconnect()

while True:
    # Read the data from sensor
    temp, hum= readDHT()
    # Display the data on OLED
    printDhtData(temp, hum)
    # Publish the data to the topic
    publishData(temp, hum)
    time.sleep(3)
