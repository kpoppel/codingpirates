from machine import SoftI2C, Pin
import ssd1306

i2c = SoftI2C(Pin(22), Pin(21))

display = ssd1306.SSD1306_I2C(128, 32, i2c)
display.rotate(False)
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

display.fill(0) # Clear the display
for y, row in enumerate(PiratLille):
    for x, c in enumerate(row):
        display.pixel(x, y, c)

display.show()
