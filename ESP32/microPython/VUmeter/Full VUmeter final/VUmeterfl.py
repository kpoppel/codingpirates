import machine, neopixel, time
from machine import Pin, ADC

# Mål strømforbrug på GPIO4
CURRENT = ADC(Pin(4))

# pin til mikrofon
Noice = ADC(Pin(32))

#GPIO til LedStrip
PinNr = 16

# Selve VU meter
def VUmeter(LedCount):
    LedStrip = neopixel.NeoPixel(machine.Pin(PinNr), LedCount)
    
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
        
    ## udskriv værdi af mic
    NoiceValue = Noice.read()
    #print (NoiceValue)
    LedsOn = (NoiceValue // (4095 // LedStrip.n))
#   print (LedsOn)
    
    LedStrip.fill(OFF)

    for i in range(LedsOn):
        LedStrip[i] = StripColor[i]
    
    LedStrip.write()



#while True:
#    VUmeter(10)
