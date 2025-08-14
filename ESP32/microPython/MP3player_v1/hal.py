import ssd1306
from dfplayermini import Player
from machine import Pin, SoftI2C


# Definer funktioner på IO porte
music = Player(pin_TX=25, pin_RX=26)
SelectBTN = Pin(32, Pin.IN, Pin.PULL_UP)
ValueBTN = Pin(33, Pin.IN, Pin.PULL_UP)
i2c = SoftI2C(Pin(22), Pin(21))
display = ssd1306.SSD1306_I2C(128, 32, i2c)
