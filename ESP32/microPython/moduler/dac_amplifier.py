import math
from machine import Pin
from machine import DAC # 8bit DAC parameter range:0-255，output voltage range:0-3.3V
from machine import PWM # 1Hz-40MHz hardware square wave generator
import time

DAC_PIN = 25

do_pwm1 = False
do_pwm2 = False
do_pwm3 = False
do_pwm4 = False
do_tri1 = False
do_sin1 = True

# Firkantgenerator med indbygget PWM (Puls-bredde-modulator)
#   |---|   |---|     |--|
#   |   |   |   |     |  |
# __|   |___|   |_____|  |____
#   <------->   <-----><->
#    frekvens    duty cycle
# Frekvensen er hvor mange gange signalet gentager sig selv (høj->lav) per sekund (1Hz-40MHz)
# Duty cycle er hvor stor en del af en hel svingning signalet er høj. (0-1024)
#
# Lyd ligger i området 20-20kHz.  Vores højttaler ikke mere end 10kHz i praksis.
# Firkantlyd har en masse 'artifakter' og man kan køre en masse andre frekvenser end den man spiller
# Typisk skal firkantsignalet labpasfiltreres gennem en RC-kobling (modstand og kondensator)

# Sæt PWM på vores DAC pin.
pwm_pin = PWM(Pin(DAC_PIN, mode=Pin.OUT))
if do_pwm1:
    # Indstil til 200 Hz, 50% duty cycle (50/100*1024)
    pwm_pin.freq(200)
    pwm_pin.duty(512)

# Sweep på duty cycle
if do_pwm2:
    for n in range(3):
        for duty in range(100): # Duty from 0 to 100 %
            pwm_pin.duty(int(duty/100*1024))
            time.sleep_ms(50)

# Sweep på frekvens
if do_pwm3:
    for freq in range(20,10000): # Frekvens fra 20 to 10kHz
            pwm_pin.freq(freq)
            time.sleep_ms(15)

# PWM melodi
if do_pwm4:
    melodi = [262,262,294,262,392,349,262,262,294,262,
              392,349,262,262,524,440,349,330,294,466,
              466,440,349,392,349]
    node = [1,1,2,2,2,3,1,1,2,2,2,3,1,1,2,2,2,2,
            2,1,1,2,2,2,3]

    pwm_pin.duty(512)
    for n in range(len(melodi)):
        pwm_pin.freq(melodi[n])
        time.sleep_ms(node[n]*300)
pwm_pin.deinit()

# Trekantlyd
#              ___
#   /\    /\    |
#  /  \  /  \   | amplitude
# /    \/    \ _|_
# <------->
#  frekvens
# Trekant vil opleves som lidt mere 'blød' i forhold til firkant.
# Her kan vi ikke bruge hardwaren til at generere signalet
if do_tri1:
    dac1 = DAC(25)
    buf_sz = 440
    buf = bytearray(buf_sz)
    for i in range(buf_sz/2):
        buf[i] = i % int(len(buf)/2+1)
    for i in range(buf_sz/2):
        buf[int(i+buf_sz/2)] = buf[int(buf_sz/2-i)]
    buf[220] = 220

    for i in range(buf_sz):
        print(i, buf[i])

    while True:
        for i in range(len(buf)):
            dac1.write(buf[i])
            time.sleep_ms(1)

# Sinuslyd
# "Den naturlige lyd".  Al lyd  kan komponeres af sinus.
if do_sin1:
    dac1 = DAC(25)
    buf = bytearray(440)
    for i in range(len(buf)):
        buf[i] = 128 + int(127 * math.sin(2 * math.pi * i / len(buf)))

    while True:
        for i in range(len(buf)):
            dac1.write(buf[i])
            time.sleep_ms(1)
