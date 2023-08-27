from machine import Pin
import time
Knap1 = Pin(32, Pin.IN, Pin.PULL_UP)
Knap2 = Pin(33, Pin.IN, Pin.PULL_UP)

while True:
    if not Knap1():
        print ("Knap 1 er trykket")
        time.sleep_ms(250)

    if not Knap2():
        print ("Knap 2 er trykket")
        time.sleep_ms(250)
        
    time.sleep_ms(100)
    print ("ingen tryk")
    
