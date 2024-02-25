# Vi pakker knapper og LEDs ind i et HAL (Hardware Abstraction Layer) modul.
# Et HAL er en pæn måde at pakke elektronikken ind på, så man lige meget hvilket program
# altid har samme måde at bruge den samme elektronik på.
# Hvis knapperne er nogle andre, eller sættes i en anden rækkefølge, skal HAL laves om, ikke andet.
import time
import random
import HAL

hal = HAL.HAL()

def on():
    r = random.randint(0,255)
    g = random.randint(0,255)
    b = random.randint(0,255)
    for i in range(hal.led.n):
        hal.led[i] = (r,g,b)
    hal.led.write()

# Tænd for LEDs på alle knapperne
on()

# Skift farve på en bestemt knap "btn". "add" er bare et tal, der lægges til hver farve, så vi kan se noget skifte.
def change_color(btn, add):
    for i in range(3*btn,3*btn+3):
        hal.led[i] = (hal.led[i][0] + add, hal.led[i][1] + add, hal.led[i][2] + add)
    hal.led.write()

while True:
    if not hal.button[0]():
        change_color(np, 0, 32)
    if not hal.button[1]():
        change_color(np, 3, 64)
    if not hal.button[2]():
        change_color(np, 1, 128)
    if not hal.button[8]():
        change_color(np, 2, 8)
    time.sleep_ms(100)


