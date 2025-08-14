import machine, neopixel, time


#Antal leds
LedCount = 10

#GPIO til LedStrip
PinNr = 16

LedStrip = neopixel.NeoPixel(machine.Pin(PinNr), LedCount)

def VUmeter(LedStrip):
    RED = (127, 0, 0)
    GREEN = (0, 127, 0)
    YELLOW = (127, 127, 0)
    OFF = (0, 0, 0)
    
    #Halvdelen skal være grøn // giver giver størst mulige heltal og runder ned
    GreenCount = (LedStrip.n // 2)
    RedCount = ((LedStrip.n - GreenCount) // 2)
    YellowCount = LedStrip.n - GreenCount - RedCount
    
    # fyld farver i array
    i = 0
    StripColor = [OFF]*LedStrip.n
    
    # Fyld StripColor med farver
    while i < GreenCount:
        StripColor[i] = GREEN
        i += 1
    while i < GreenCount+YellowCount:
        StripColor[i] = YELLOW
        i += 1
    while i < LedStrip.n:
        StripColor[i] = RED
        i += 1
    
    #Tænd alle
    for i in range(LedStrip.n):
        LedStrip[i] = StripColor[i]
    
    LedStrip.write()
    
    time.sleep(2)
    LedStrip.fill(OFF)
    LedStrip.write()
    time.sleep(2)
    
    

while True:
    VUmeter(LedStrip)
