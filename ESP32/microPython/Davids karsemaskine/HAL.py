import ssd1306
from machine import Pin, SoftI2C

class HAL:
    """
    Abstraction of the hardware layer.
    Very simple as it does not do much to wrap drivers.

    In a professional setting the HAL layer would wrap the lower level drivers
    exposing just the functions necessary for the application.  This means
    the underlying hardware can be exchanged and only the HAL needs update.
    This is an ESP32 project with known hardware, so there is no need.
    """
    def __init__(self):
        self.button_1 = Pin(32, Pin.IN, Pin.PULL_UP)
        self.button_2 = Pin(33, Pin.IN, Pin.PULL_UP)
        self.gron = Pin(27, Pin.OUT)
        self.bla = Pin(19, Pin.OUT)
        self.rod = Pin(23, Pin.OUT)
        self.i2c = SoftI2C(Pin(22), Pin(21))
        self.display = ssd1306.SSD1306_I2C(128, 32, self.i2c)
        self.display.rotate(True) # screen rotation

