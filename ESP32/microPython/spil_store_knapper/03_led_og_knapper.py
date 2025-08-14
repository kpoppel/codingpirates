# Programmet udvides med at kunne reagere på om knappen er trykket ned.
# Knappens input forbindes til GPIO 13
# LED data forbindes til GPIO4 som før.
#
# Programmet ændres også lidt, så vi sætter en tilfældig farve til at starte på.
# Kun for at prøve noget nyt.
import time
import machine, neopixel
import random

button_1 = machine.Pin(13, machine.Pin.IN, machine.Pin.PULL_UP)

# 13, 16, 17, 18

# Fortæl programmet hvor mange LED på strip:
NUM_PIXELS = 3
# Fortæl programmet hvilken GPIO data-pin er sat på:
PIN = 4

def on(np):
    n = np.n
    for i in range(n):
        np[i] = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
    np.write()

np = neopixel.NeoPixel(machine.Pin(PIN),NUM_PIXELS)

# Tænd for LEDs til at starte med.
on(np)

# Funktion til at skifte farve. Den skal vi bruge når knappen trykkes ned.
def change_color(np, add):
    n = np.n
    for i in range(n):
        np[i] = (np[i][0] + add, np[i][1] + add, np[i][2] + add)
    np.write()

# Vores hoved-løkke til at registrere knaptryk.
while True:
    if not button_1():
        change_color(np, 32)
    # Det er vigtigt at vente lidt, så processoren gives fri til andre tråde (her kun en tråd)
    time.sleep_ms(100)
