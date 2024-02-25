# Første program til at styre de programmerbare LEDs
#
# neopixel giver et array hvor hvert element repræsentrer en LED fra den, der er nærmest til den sidste i rækken.
#
# Vores knap har 3 LEDs.  Dataledningen forbindes til GPIO4
import time
import machine, neopixel

# Fortæl programmet hvor mange LED på strip:
NUM_PIXELS = 3
# Fortæl programmet hvilken GPIO data-pin er sat på:
PIN = 4

def on(np):
    n = np.n
    for i in range(n):
        np[i] = (64, 48, 255)
    np.write()

np = neopixel.NeoPixel(machine.Pin(PIN),NUM_PIXELS)

on(np)
