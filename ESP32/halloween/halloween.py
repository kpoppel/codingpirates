# MP3 player controllable via the buttons.
# Button 1 previous number
# Button 2 next number
from machine import Pin
from dfplayermini import Player
from machine import SoftI2C as I2C
import ssd1306

import time
import random

### Defaults
WAIT_TIME_MS = 200
vol = 25
playing = 5
detected = False
random_mode = True

# Setup oled display
# using default address 0x3C
i2c = I2C(sda=Pin(21), scl=Pin(22))
display = ssd1306.SSD1306_I2C(128, 32, i2c)

# Setup MP3 player
music = Player(pin_TX=25, pin_RX=26)
music.stop()
music.volume(vol)
ondisk = music.filesinfolder()
#music.play(1)

# Setup pins
button_volume = Pin(32, Pin.IN, Pin.PULL_UP)
button_track = Pin(33, Pin.IN, Pin.PULL_UP)
led = Pin(2, Pin.OUT)

# Setup Radar
radar = Pin(36, Pin.IN)

# https://github.com/kpoppel/codingpirates/
#   piratlille.py
PiratLille = [
    [0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0],
    [0,0,0,0,1,1,1,1,1,1,1,1,1,0,0,0],
    [0,0,0,1,1,1,1,1,1,1,1,1,1,0,0,0],
    [0,0,0,1,1,1,1,1,1,1,1,1,1,0,0,0],
    [0,0,0,1,1,1,1,1,1,1,1,1,1,0,0,0],
    [0,0,0,1,1,0,0,1,1,0,0,1,1,0,0,0],
    [0,0,0,1,0,0,0,1,1,0,0,0,1,0,0,0],
    [0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0],
    [0,0,0,0,1,1,1,0,0,1,1,1,0,0,0,0],
    [0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0],
    [0,0,0,0,0,1,0,1,1,0,1,0,0,0,0,0],
    [0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,1,1,0,0,0,0,0,1,0],
    [0,1,1,0,0,0,0,0,0,0,0,0,0,1,1,0],
    [1,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1],
    [0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0],
    [0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0],
    [0,0,0,0,1,1,1,0,0,1,1,1,0,0,0,0],
    [0,1,1,1,1,0,0,0,0,0,0,1,1,1,1,0],
    [1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1],
    [0,0,1,1,0,0,0,0,0,0,0,0,1,1,0,0],
]

# Sounds on SD card: (name, duration)
sounds = [
    ("", 0),
    ("Girl scream",2),
    ("Zombie moans",15),
    ("Boo and laugh",3),
    ("Monster Laugh",10),
    ("Welcome laugh",6),
    ("Evil Laughing",9),
    ]

def drawScreen(playing, ondisk, random_mode):
    display.fill(0) # Clear the display
    for y, row in enumerate(PiratLille):
        for x, c in enumerate(row):
            display.pixel(x, y, c)

    display.text(f'Volume: {music.volume()}', 17, 0, 1)
    display.text(f'{sounds[playing][0]}', 17, 12, 1)
    display.text(f'Spiller: {playing}/{ondisk}', 17, 24, 1)
    if random_mode:
        display.text("R", 0, 24, 1)    
    display.show()
    
drawScreen(playing, ondisk, random_mode)
while True:
    if not button_volume() and not button_track():
        # Switch random mode on/off
        if random_mode:
            random_mode = False
        else:
            random_mode = True
        drawScreen(playing, ondisk, random_mode)
            
    if not button_volume():
        if vol < 30:
            vol += 1
        else:
            vol = 5
        music.volume(vol)
        drawScreen(playing, ondisk, random_mode)

    if not button_track():
        if ondisk == -1:
            ondisk = music.filesinfolder()
        if playing < ondisk:
            playing += 1
        else:
            playing = 1
        music.play(playing)
        drawScreen(playing, ondisk, random_mode)

    if radar() and not detected:
        if random_mode:
            playing = random.randrange(1, len(sounds)-1)
            drawScreen(playing, ondisk, random_mode)
        music.play(playing)
        detected = True
        #print(f"Radar: #{playing} l{sounds[playing][1]}")
                                
    if detected:
        time.sleep(sounds[playing][1])
        detected = False
        
    #print(f"Radar: #{playing} l{sounds[playing][1]}")
    time.sleep_ms(WAIT_TIME_MS)
