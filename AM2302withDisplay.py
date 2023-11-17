#Code and circuit tutorial on Electrocredible.com

from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import time
import dht 



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

def printDhtData():
    oled.fill(0)
    temp, hum= readDHT()
    oled.text("Temp:", 0, 10)
    oled.text(str(temp), 80, 10)
    oled.text("C", 120, 10)
    oled.text("Humidity:", 0, 30)
    oled.text(str(hum), 80, 30)
    oled.text("%", 120, 30)
    oled.show()
    
while True:
    printDhtData()
    time.sleep(2)