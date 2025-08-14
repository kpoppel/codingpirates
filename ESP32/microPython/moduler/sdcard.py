# SDCARD på SPI
# https://docs.micropython.org/en/latest/library/machine.SDCard.html
#
# kortholder set bagfra, dvs. de to smalle pins til venstre,
# og den lidt løftede pin til højre:
#
# - MISO GND SCLK 3V3 GND MOSI CS -
#
# slot 2:
#   19        18           23  5
# slot 3:
#   12        14           13  15
#
# machine.SDCard(slot=1, width=1, cd=None, wp=None,
#                sck=None, miso=None,
#                mosi=None, cs=None, freq=20000000)
import machine
import os

sdcard = machine.SDCard(slot=2, freq=10000)

os.mount(sdcard, "/sd")
print(os.getcwd())
print(os.listdir())
os.chdir("/sd")
print(os.getcwd())
print(os.listdir())
print(os.statvfs('/'))

# Output from the program:
# /
# ['sd', 'boot.py', 'lib']
# /sd
# ['System Volume Information', 'Hej_ESP32.txt']