import gc
import network
import lib.gate as gate
import time
from micropython import const
from ubluetooth import BLE
import lib.webserver as webserver

bt = BLE()
bt.active(True)

_IRQ_SCAN_RESULT = const(5)
_IRQ_SCAN_DONE = const(6)

def byteToMac(addr):
    m = memoryview(addr)
    a = "{:0>2X}:{:0>2X}:{:0>2X}:{:0>2X}:{:0>2X}:{:0>2X}".format(m[0],m[1],m[2],m[3],m[4],m[5])
    return a   

def handler(event, data):
    if event == _IRQ_SCAN_RESULT:
        # A single scan result.
        addr_type, addr, adv_type, rssi, adv_data = data
        print(addr_type,memoryview(addr) , adv_type, rssi,memoryview( adv_data))
        for i in addr:
            print("{0:x}".format(i))
        
        print(byteToMac(addr))
        if addr == memoryview(bytearray(b'\x40\xe8\xe7\x85\x3d\xed')):
            print("device found")
    elif event == _IRQ_SCAN_DONE:
        # Scan duration finished or manually stopped.
        print("scan complete")
        pass

def onAdd(addBT):
    memoryview(addBT)

def onDelete(delBT):
    print("onDelete")

bt.irq(handler)

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid="Test", password="1234",authmode= 0)

s = webserver.webserverstart()

lastscan = 0
while True:
    webserver.webserver(s, onAdd, onDelete)
    print("scanning soon")
    if time.time() - lastscan > 10:
        print("scanning now...")
        bt.gap_scan(10000) 
        lastscan = time.time()
    

    
