try:
  import usocket as socket
except:
  import socket

from machine import Pin
import network

import esp
esp.osdebug(None)

import gc
gc.collect()

station = network.WLAN(network.AP_IF)
station.active(True)
station.config(essid="Test", password="1234",authmode= 0)


print('Connection successful')
print(station.ifconfig())

led = Pin(2, Pin.OUT)