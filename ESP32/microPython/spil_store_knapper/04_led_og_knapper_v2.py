# Programmet udvides med at kunne reagere på 4 knapper.  Det er bare at gentage lidt.
# Udfordringen er at skifte de rigtige 3 LEDs as de 12 LEDs der nu er.
#
# Knapperne er i det her program:
# Nr.    1,    9,   2,    3
# GPIO: 13,   16,  17,   18
# LED:  0-2, 3-5, 6-8, 9-11
#
#  Hvis det er andre knapper, eller de sidder i en anden rækkefølge, skal programmet rettes til.
import time
import machine, neopixel
import random

button_1 = machine.Pin(13, machine.Pin.IN, machine.Pin.PULL_UP)
button_2 = machine.Pin(16, machine.Pin.IN, machine.Pin.PULL_UP)
button_3 = machine.Pin(17, machine.Pin.IN, machine.Pin.PULL_UP)
button_4 = machine.Pin(18, machine.Pin.IN, machine.Pin.PULL_UP)

# Fortæl programmet hvor mange LED på strip:
NUM_PIXELS = 12
# Fortæl programmet hvilken GPIO data-pin er sat på:
PIN = 4

def on(np):
    n = np.n
    r = random.randint(0,255)
    g = random.randint(0,255)
    b = random.randint(0,255)
    for i in range(n):
        np[i] = (r,g,b)
    np.write()

np = neopixel.NeoPixel(machine.Pin(PIN),NUM_PIXELS)

# Tænd for LEDs på alle knapperne
on(np)

# Skift farve på en bestemt knap "btn". "add" er bare et tal, der lægges til hver farve, så vi kan se noget skifte.
def change_color(np, btn, add):
    n = np.n
    for i in range(3*btn,3*btn+3):
        np[i] = (np[i][0] + add, np[i][1] + add, np[i][2] + add)
    np.write()

while True:
    if not button_1():
        change_color(np, 0, 32)
    if not button_2():
        change_color(np, 3, 64)
    if not button_3():
        change_color(np, 1, 128)
    if not button_9():
        change_color(np, 2, 8)
    time.sleep_ms(100)

