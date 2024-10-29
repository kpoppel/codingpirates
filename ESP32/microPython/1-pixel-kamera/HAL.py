from machine import Pin, SoftI2C

from st7735 import TFT, TFTColor
from sysfont import sysfont
from machine import SPI,Pin

class HAL:
    """
    Abstraction of the hardware layer.
    Very simple as it does not do much to wrap drivers.

    In a professional setting the HAL layer would wrap the lower level drivers
    exposing just the functions necessary for the application.  This means
    the underlying hardware can be exchanged and only the HAL needs update.
    This is an ESP32 project with known hardware, so there is no need.
    
    use as:
      import HAL
      hal = HAL.HAL()
    """
    
    # The last two GPIOs are the on-board buttons
    SCREEN_WIDTH = 160
    SCREEN_HEIGHT = 128
    
    def __init__(self):
        # Initialise TFT display ST7735
        # CS: 15
        # RST: 4
        # AO:  2
        # SDA: 23
        # SCK: 18
        #
        # Rotation set so pins are on the right and screen width is the largest dimension (160 px)
        # Y is 0 at the top, and 127 at the bottom.
        spi = SPI(2, baudrate=33000000, polarity=0, phase=0, sck=Pin(18), mosi=Pin(23), miso=None)
        self.tft=TFT(spi=spi, aDC=2, aReset=4, aCS=15)
        self.tft.initr()
        self.tft.rgb(True)
        self.tft.rotation(3)
        self.tft.fill(TFT.BLACK)
        self.tft._setwindowloc((0,0),(self.SCREEN_WIDTH-1,self.SCREEN_HEIGHT-1))

        # Add a framebuffer to draw into
        from framebuf import FrameBuffer, RGB565
        buf = bytearray(self.SCREEN_WIDTH*self.SCREEN_HEIGHT*2)
        self.framebuffer = FrameBuffer(buf, self.SCREEN_WIDTH, self.SCREEN_HEIGHT, RGB565)

    def show(self):
        # Dump the framebuffer to the screen.
        self.tft._writedata(self.framebuffer)


