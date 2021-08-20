from machine import Pin
import time
p5 = Pin(5, Pin.OUT)
p5.off()
def opengate():
    p5.on()
    time.sleep(1)
    p5.off()