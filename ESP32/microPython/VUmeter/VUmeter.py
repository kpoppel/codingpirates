import machine, neopixel, time
from machine import Pin, ADC

# Mål strømforbrug på GPIO4
CURRENT = ADC(Pin(4))

# pin til mikrofon
Noice = ADC(Pin(2))

#Antal leds
LedCount = 0

#GPIO til LedStrip
PinNr = 16

#Tæl antal af Leds
def LedCounter(LedCount):
    #Sæt farver
    WHITE = (255, 255, 255)
    OFF = (0, 0, 0)
    
    #Start værdi til første gennemgang
    CurrentValue = 40
    
    while CurrentValue > 20:
        # Initialiser LedStrip
        LedStrip = neopixel.NeoPixel(machine.Pin(PinNr), LedCount + 1)
        
        #Tænd en hvid led
        LedStrip[LedCount] = WHITE
        LedStrip.write()
        
        #Læs strømforbrug
        CurrentValue = CURRENT.read()
        
        #Sluk Alle
        LedStrip.fill(OFF)
        LedStrip.write()
        LedCount += 1
        
    print(LedCount - 1)
    return(LedCount -1)

# Selve VU meter
def VUmeter(LedCount):
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
    print (LedsOn)
    
    LedStrip.fill(OFF)

    for i in range(LedsOn):
        LedStrip[i] = StripColor[i]
    
    LedStrip.write()


LedCount=LedCounter(LedCount)

LedStrip = neopixel.NeoPixel(machine.Pin(PinNr), LedCount)

while True:
    VUmeter(LedCount)
