from machine import Pin
import time, machine

machine.lightsleep(1)
machine.idle()
RadarONOFF = Pin(16, Pin.OUT)
RadarSIG = Pin(17, Pin.IN)

RadarONOFF.on()

while True:
    if RadarSIG():
        print (str(time.localtime()) + "Der sker noget")
        time.sleep(5)
        
    time.sleep_ms(500)
    #print ("Der sker ikke noget")
    
    